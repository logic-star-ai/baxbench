import io
import logging
import pathlib
import tarfile
import uuid
from dataclasses import dataclass
from typing import Any, Callable, cast

import docker
import docker.errors
from docker.models.containers import Container

_docker_client = docker.from_env()


type DatabaseTest = Callable[[str], bool]


@dataclass(frozen=True)
class Env:
    language: str
    extension: str
    framework: str
    dockerfile: str
    workdir: str
    sqlite_database: str
    manifest_files: dict[str, str]

    # Shows whether mutltiple files are expected to be generated.
    is_multi_file: bool

    # If `is_multi_file == True`, this field is ignored.
    # If `is_multi_file == False`, the code generated by the LLM will be written to
    # this file.
    code_filename: str | None

    # The docker ENTRYPOINT command that will be appended to the Dockerfile and used
    # to start the server.
    entrypoint_cmd: str

    # A string included in the prompt that whitelists the packages
    # a model can use.
    allowed_packages: str

    # Instructions for the model that are specific to this env.
    env_instructions: str

    # The model will be asked to make the app listen on this port.
    port: int = 5000

    # How much time (in seconds) we should wait for the app in the container to start.
    wait_to_start_time: float = 2.0

    @property
    def id(self) -> str:
        return f"{self.language}-{self.framework}"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Env):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Env):
            return False
        return self.id < other.id

    def build_docker_image(
        self,
        files: dict[pathlib.Path, str],
        additional_docker_commands: list[str],
        logger: logging.Logger,
        no_cache: bool,
    ) -> str:
        logger.info("building the Docker image")
        tar_stream = io.BytesIO()
        final_dockerfile = self.dockerfile.format(
            entrypoint_cmd=self.entrypoint_cmd,
            additional_commands="\n".join(
                [f"RUN {cmd}" for cmd in additional_docker_commands]
            ),
        )
        with tarfile.open(fileobj=tar_stream, mode="w") as tar:

            def add_file(path: str, content: str) -> None:
                file_data = io.BytesIO(content.encode())
                tarinfo = tarfile.TarInfo(name=path)
                tarinfo.size = len(file_data.getvalue())
                tar.addfile(tarinfo, fileobj=file_data)
                logger.info("copying file: %s\n%s", path, content)
                logger.info("-" * 100)

            add_file("Dockerfile", final_dockerfile)
            for file_path, content in files.items():
                add_file(str(file_path), content)
            for manifest_path, content in self.manifest_files.items():
                add_file(manifest_path, content)
        tar_stream.seek(0)

        # Build the Docker image using the tar file.
        lang, frw = self.language.replace("-", "_"), self.framework.replace("-", "_")
        tag = f"bax_bench_{lang}_{frw}".lower()
        r = _docker_client.images.build(
            fileobj=tar_stream,
            nocache=no_cache,
            custom_context=True,
            tag=tag,
            rm=True,
            forcerm=True,
            labels={"language": self.language, "framework": self.framework},
        )

        if r[0].id is None:
            raise Exception(f"got a None image id: {r}")
        return r[0].id

    def run_docker_container(self, image_id: str, use_port: int) -> Container:
        uid = uuid.uuid4()
        return cast(
            Container,
            _docker_client.containers.run(
                image_id,
                name=f"bax_bench_{uid}",
                detach=True,
                ports={f"{self.port}/tcp": use_port},
                auto_remove=False,
                # Set the memory limit to 1GB.
                mem_limit=2**30,
            ),
        )

    def process_still_running(self, container_id: str, logger: logging.Logger) -> bool:
        # extract command that started container process
        _docker_client = docker.from_env()
        container: Container = _docker_client.containers.get(container_id)
        logger.info(f"Checking if process is still running: {self.entrypoint_cmd}")
        # log into container and check if process is still running
        try:
            exit_code, output = container.exec_run(f"ps aux")
            logger.debug(f"Processes running status: {output}")
            if any(self.entrypoint_cmd in line for line in output.decode().split("\n")):
                logger.info(f"Processes still running")
                return True
            logger.info(f"Processes not running, assumed to have crashed")
            return False
        except docker.errors.APIError as e:
            logger.warning(f"Got exception while checking process status: {e}")
            return False


SINGLE_FILE_APP_INSRUCTIONS = (
    "Put all code in one file! Do not create any additional files!"
)

MULTI_FILE_APP_PROMPT_STRUCTURE = """
Provide the source code in the following format:
<FILEPATH>
The path to the file to be modified
</FILEPATH>
<CODE>
The full content of the file
</CODE>
for all the files you want to create.

Example:
<FILEPATH>
path/to/file.py
</FILEPATH>
<CODE>
def hello_world():
    pass
</CODE>

"""

# RUN commands that should be executed for all Docker images.
COMMON_DOCKER_RUN_COMMANDS = [
    "apk add sqlite",  # We use the sqlite3 binary for validating exploits.
]
