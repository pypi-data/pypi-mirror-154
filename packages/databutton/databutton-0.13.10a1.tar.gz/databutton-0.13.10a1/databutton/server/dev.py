import asyncio
import hashlib
import logging
import os
import platform
import shutil
import signal
from asyncio.subprocess import Process
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Optional, Sequence, Union

import click
import psutil
from watchfiles import Change, DefaultFilter, arun_process, awatch

from databutton.decorators.apps.streamlit import StreamlitApp
from databutton.decorators.jobs.schedule import Scheduler
from databutton.utils import get_databutton_components_path
from databutton.utils.build import generate_components, read_artifacts_json

logger = logging.getLogger("databutton.start")
awatch_logger = logging.getLogger("watchfiles.main")
awatch_logger.setLevel(logging.CRITICAL)


class DatabuttonFilter(DefaultFilter):
    def __init__(
        self,
        *,
        ignore_paths: Optional[Sequence[Union[str, Path]]] = None,
        extra_extensions: Sequence[str] = (),
        include_artifacts_json: bool = False,
    ) -> None:
        """
        Args:
            ignore_paths: The paths to ignore, see [`BaseFilter`][watchfiles.BaseFilter].
            extra_extensions: extra extensions to ignore.

        `ignore_paths` and `extra_extensions` can be passed as arguments partly to support [CLI](../cli.md) usage where
        `--ignore-paths` and `--extensions` can be passed as arguments.
        """
        self.extensions = (".py", ".pyx", ".pyd", ".pyc") + tuple(extra_extensions)
        self.include_artifacts_json = include_artifacts_json
        super().__init__(
            ignore_paths=ignore_paths,
            ignore_dirs=self.ignore_dirs + tuple([".databutton"]),
        )

    def __call__(self, change: "Change", path: str) -> bool:
        ret = (
            path.endswith(self.extensions)
            and super().__call__(change, path)
            and not path.endswith("artifacts.json")
        )
        if self.include_artifacts_json:
            ret = ret or path.endswith("artifacts.json")

        return ret


def get_components_hash():
    p = get_databutton_components_path()
    if not p.exists():
        return False
    md5 = hashlib.md5()
    with open(p, "r") as f:
        md5.update(f.read().encode("utf-8"))
    return md5.hexdigest()


class ComponentsJsonFilter(DefaultFilter):
    def __init__(self, starting_hash: str = None) -> None:
        super().__init__()
        self.prev_hash: Optional[str] = starting_hash

    def __call__(self, change: "Change", path: str) -> bool:
        should_call = super().__call__(change, path) and path.endswith("artifacts.json")
        if should_call:
            if not Path(path).exists():
                # Ignore if the file doesn't exist
                return False
            # Check hash extra check
            digest = get_components_hash()
            if digest == self.prev_hash:
                return False
            self.prev_hash = digest
            return True


class StreamlitWatcher:
    def __init__(self, apps: List[StreamlitApp] = []):
        self.apps: Dict[str, StreamlitApp] = {app.uid: app for app in apps}
        self.processes: Dict[str, Process] = {}
        if platform.system() == "Windows":
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    def cancel(self):
        for app in self.apps.values():
            self.stop_process(app)

    async def start_process(self, app: StreamlitApp) -> Process:
        cmd = f"""streamlit run {app.filename} \
                    --server.port={app.port} \
                    --server.headless=true \
                    --browser.gatherUsageStats=false \
                    --global.dataFrameSerialization=arrow \
                    --server.runOnSave=true \
                """
        # Set environment and force PYTHONPATH
        current_env = os.environ.copy()
        current_env["PYTHONPATH"] = "."
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=current_env,
        )
        self.processes[app.uid] = process
        return process

    def stop_process(self, app: StreamlitApp):
        process: Optional[Process] = self.processes.get(app.uid)
        if process is not None:
            try:
                process.kill()
            except:  # noqa
                logger.debug(f"Could not terminate process {process.pid}.")
                # Ignore terminations, we'll nuke them all down below anyway
        # Streamlit has dangling processes, so let's find them and killem
        for psprocess in psutil.process_iter():
            try:
                try:
                    cmdline = psprocess.cmdline()
                except (psutil.AccessDenied, psutil.NoSuchProcess, ProcessLookupError):
                    continue
                if app.filename in cmdline:
                    psprocess.kill()
            except:  # noqa
                logger.debug(
                    f"Could not terminate psutil.process {psprocess.pid}. "
                    + f"{psprocess}",
                )

    async def update_processes_from_apps(
        self, apps: List[StreamlitApp]
    ) -> List[asyncio.Task]:
        apps_map: Dict[str, StreamlitApp] = {app.uid: app for app in apps}
        previous = self.apps.values()
        previous_apps_map = self.apps.copy()
        self.apps = apps_map
        old, new = set(app.uid for app in previous), set(app.uid for app in apps)
        new_apps = list(new - old)
        deleted_apps = list(old - new)

        for new_uid in new_apps:
            await self.start_process(apps_map.get(new_uid))

        for deleted_uid in deleted_apps:
            self.stop_process(previous_apps_map.get(deleted_uid))

        for running_uid in new & old:
            new_app = apps_map.get(running_uid)
            old_app = previous_apps_map.get(running_uid)
            if old_app.uid != new_app.uid:
                # This has a new port, we should restart it.
                self.stop_process(old_app)
                await self.start_process(new_app)

        return len(new_apps) > 0 or len(deleted_apps) > 0


@dataclass
class DatabuttonConfig:
    port: int = os.environ.get("PORT", 8000)
    log_level: str = os.environ.get("LOG_LEVEL", "critical")


class GracefulExit(SystemExit):
    code = 1


class DatabuttonRunner:
    def __init__(self, root_dir=Path.cwd(), **config):
        self.root_dir = root_dir
        self.config = DatabuttonConfig(**config)
        self.initial_hash: str = None
        self.cancels: List[Callable] = []

    async def create_webwatcher(self):
        args = [("port", self.config.port), ("log-level", self.config.log_level)]
        args_string = " ".join([f"--{arg}={value}" for arg, value in args])
        target_str = f"uvicorn {args_string} databutton.server.prod:app"
        return await arun_process(
            self.root_dir,
            target=target_str,
            target_type="command",
            watch_filter=ComponentsJsonFilter(starting_hash=self.initial_hash),
            callback=lambda _: click.secho("Restarting webserver..."),
        )

    async def create_streamlit_watcher(self):
        streamlit_watcher = StreamlitWatcher()
        self.cancels.append(streamlit_watcher.cancel)
        components = read_artifacts_json()
        await streamlit_watcher.update_processes_from_apps(components.streamlit_apps)
        async for _ in awatch(
            self.root_dir,
            watch_filter=ComponentsJsonFilter(starting_hash=self.initial_hash),
        ):
            new_components = read_artifacts_json()
            await streamlit_watcher.update_processes_from_apps(
                new_components.streamlit_apps
            )

    async def create_scheduler_watcher(self):
        return await arun_process(
            self.root_dir,
            watch_filter=DatabuttonFilter(include_artifacts_json=True),
            target=Scheduler.create,
            callback=lambda _: click.secho("Restarting scheduler..."),
        )

    async def create_components_watcher(self):
        return await arun_process(
            self.root_dir,
            watch_filter=DatabuttonFilter(),
            target=generate_components,
        )

    def shutdown(self, *args):
        click.secho("\nstopping...", fg="cyan")
        for cancel in self.cancels:
            cancel()
        for task in asyncio.all_tasks():
            task.cancel()
        raise GracefulExit()

    async def run(self):
        shutil.rmtree(Path(".databutton"), ignore_errors=True)
        generate_components()
        self.initial_hash = get_components_hash()
        signal.signal(signal.SIGINT, self.shutdown)
        await self.run_tasks()

    async def run_tasks(self) -> List[asyncio.Task]:
        components_generator_task = asyncio.create_task(
            self.create_components_watcher(), name="components"
        )

        streamlit_task = asyncio.create_task(
            self.create_streamlit_watcher(), name="streamlit"
        )

        web_task = asyncio.create_task(self.create_webwatcher(), name="uvicorn")

        scheduler_task = asyncio.create_task(
            self.create_scheduler_watcher(), name="scheduler"
        )
        return await asyncio.gather(
            *[
                components_generator_task,
                streamlit_task,
                web_task,
                scheduler_task,
            ]
        )
