"""Exercise the C# environment with a fixed fixture, without model API calls.

Default: pipenv run python scripts/smoke_csharp.py
Local SDK: pipenv run python scripts/smoke_csharp.py --local-sdk /path/to/dotnet

Docker mode uses the benchmark's image builder, container runner, SQLite helper,
and ClickCount tests. Local mode verifies restore/publish and HTTP/package behavior
only; it cannot validate the Dockerfile or container process inspection.
"""

import argparse
import logging
import os
import socket
import sqlite3
import subprocess
import sys
import tempfile
import time
from contextlib import nullcontext
from pathlib import Path
from typing import TYPE_CHECKING, cast
from unittest.mock import patch

import requests

if TYPE_CHECKING:
    from env.base import Env
    from scenarios.base import AppInstance

_ROOT = Path(__file__).resolve().parent.parent
_FIXTURE = _ROOT / "scripts" / "fixtures" / "csharp" / "Program.cs"
sys.path.insert(0, str(_ROOT / "src"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def available_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def wait_for_server(port: int) -> None:
    deadline = time.monotonic() + 60
    while time.monotonic() < deadline:
        try:
            response = requests.get(f"http://localhost:{port}/", timeout=1)
            if response.status_code == 200 and response.json() == {"status": "ready"}:
                return
        except (requests.RequestException, ValueError):
            pass
        time.sleep(0.2)
    raise RuntimeError("The smoke fixture did not become ready within 60 seconds")


def check_http(app: "AppInstance") -> None:
    from scenarios.click_count import func_test_valid_click_count

    require(
        func_test_valid_click_count(app), "Existing ClickCount functional test failed"
    )
    response = requests.get(f"http://localhost:{app.port}/dependencies", timeout=10)
    response.raise_for_status()
    require(
        response.json() == {"bcrypt": True, "jwt": True, "runtimeMajor": 11},
        f"Package/runtime checks failed: {response.text}",
    )


def check_docker(env: "Env", temp: Path, logger: logging.Logger) -> None:
    from env.base import COMMON_DOCKER_RUN_COMMANDS
    from exploits import execute_sql_on_docker
    from scenarios.base import AppInstance
    from scenarios.click_count import sec_test_sql_injection

    image_id = env.build_docker_image(
        {Path("Program.cs"): _FIXTURE.read_text()},
        COMMON_DOCKER_RUN_COMMANDS,
        logger,
        no_cache=False,
    )
    port = available_port()
    container = env.run_docker_container(image_id, port)
    try:
        wait_for_server(port)
        require(
            env.process_still_running(container.id, logger),
            "The harness could not detect the running dotnet process",
        )
        app = AppInstance(port, temp / "click-count.log", container.id, env, logger)
        check_http(app)
        require(
            sec_test_sql_injection(app) == set(),
            "ClickCount SQL injection fixture check failed or could not execute",
        )
        result = execute_sql_on_docker(
            container.id,
            f"{env.workdir}/{env.sqlite_database}",
            "SELECT count(*) FROM clicks;",
        )
        require(result.output.decode().strip() == "6", "SQLite helper read failed")
        require(
            env.process_still_running(container.id, logger),
            "The fixture process stopped during the smoke checks",
        )
    except Exception:
        print(
            cast(bytes, container.logs(tail=60)).decode(errors="replace"),
            file=sys.stderr,
        )
        raise
    finally:
        container.remove(force=True)
    print(
        "Docker smoke passed: ClickCount, SQLite helper, bcrypt, JWT, process checks."
    )


def check_local(env: "Env", dotnet: Path, temp: Path, logger: logging.Logger) -> None:
    from scenarios.base import AppInstance

    project_dir = temp / "project"
    project_dir.mkdir()
    (project_dir / "Program.cs").write_text(_FIXTURE.read_text())
    for name, contents in env.manifest_files.items():
        (project_dir / name).write_text(contents)
    process_env = {
        **os.environ,
        "DOTNET_CLI_TELEMETRY_OPTOUT": "1",
        "DOTNET_NOLOGO": "1",
        "APP_SECRET": "supers3cret",
    }
    port = available_port()
    process_env["ASPNETCORE_URLS"] = f"http://127.0.0.1:{port}"
    output_dir = temp / "published"
    log_path = temp / "dotnet.log"
    try:
        with log_path.open("wb") as log:
            for command in (
                [str(dotnet), "restore", "Server.csproj", "--nologo"],
                [
                    str(dotnet),
                    "publish",
                    "Server.csproj",
                    "--configuration",
                    "Release",
                    "--no-restore",
                    "--output",
                    str(output_dir),
                    "--nologo",
                ],
            ):
                subprocess.run(
                    command,
                    cwd=project_dir,
                    env=process_env,
                    stdout=log,
                    stderr=subprocess.STDOUT,
                    check=True,
                    timeout=600,
                )
            process = subprocess.Popen(
                [str(dotnet), str(output_dir / "Server.dll")],
                cwd=project_dir,
                env=process_env,
                stdout=log,
                stderr=subprocess.STDOUT,
            )
            try:
                wait_for_server(port)
                check_http(
                    AppInstance(port, temp / "click-count.log", "local", env, logger)
                )
                with sqlite3.connect(project_dir / env.sqlite_database) as connection:
                    row = connection.execute("SELECT count(*) FROM clicks").fetchone()
                    require(row == (5,), "External SQLite read failed")
                require(
                    process.poll() is None, "The fixture process stopped unexpectedly"
                )
            finally:
                process.terminate()
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=10)
    except Exception:
        print(
            "\n".join(log_path.read_text(errors="replace").splitlines()[-60:]),
            file=sys.stderr,
        )
        raise
    print("Local SDK smoke passed: restore/publish, ClickCount, SQLite, bcrypt, JWT.")
    print("Docker build, SQLite CLI, and container process checks were not exercised.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--local-sdk", type=Path, metavar="DOTNET")
    args = parser.parse_args()

    # Env's module creates a Docker client at import time. Local mode never uses
    # Docker; bypass only that initialization, not any tested SDK/HTTP behavior.
    with (
        patch("docker.from_env", return_value=object())
        if args.local_sdk
        else nullcontext()
    ):
        from env.csharp import CSharpAspNetCoreEnv
        from scenarios import click_count  # noqa: F401

    with tempfile.TemporaryDirectory(prefix="baxbench-csharp-smoke-") as directory:
        temp = Path(directory)
        logger = logging.getLogger("baxbench-csharp-smoke")
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(temp / "harness.log")
        logger.addHandler(handler)
        try:
            if args.local_sdk:
                check_local(CSharpAspNetCoreEnv, args.local_sdk.resolve(), temp, logger)
            else:
                check_docker(CSharpAspNetCoreEnv, temp, logger)
        finally:
            logger.removeHandler(handler)
            handler.close()


if __name__ == "__main__":
    main()
