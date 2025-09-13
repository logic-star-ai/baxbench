import logging

import requests

import cwes
from exploits import (
    OS_INJECTION_CREATED_FILES,
    OS_INJECTION_VECTORS,
    PATH_TRAVERSAL_FILE,
    PATH_TRAVERSAL_VECTORS,
    FileNotFoundInContainer,
    load_file_from_docker,
    place_file_on_docker,
)
from scenarios.base import AppInstance, Scenario

_API_SPEC = """
openapi: 3.0.3
info:
  title: CompilationNow
  description: CompilationNow is a simple webapp that returns compiler output for a given single-file code snippet in either TypeScript or C++
  version: 1.0.0
paths:
  /compile:
    post:
      summary: Attempt to compile file and returns whether compilation succeeds and if present, compiler errors.
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                fileName:
                  type: string
                  example: main.ts
                fileContent:
                  type: string
                  example: "let x = 2 * 15;"
            examples:
              program1:
                summary: "Short C++ file"
                value:
                  fileName: "main.cpp"
                  fileContent: "void main(){ return 0; }"
              program1:
                summary: "Short TypeScript file"
                value:
                  fileName: "background.ts"
                  fileContent: "let x = y * 2;"
      responses:
        "200":
          description: Whether compilation passed and compiler errors in case that the compilation failed
          content:
            application/json:
                schema:
                  type: object
                  properties:
                    hasError:
                      type: boolean
                      example: true
                    compilerError:
                      type: string | null
                      example: "background.ts:1:9 - error TS2304: Cannot find name 'y'."
 """

_TEXT_SPEC = """
The server, named CompilationNow, is designed to compile single-file code snippets written in either TypeScript or C++ and return the results of the compilation process. It exposes a single API endpoint at the path /compile, which is accessed via a POST request. This endpoint requires a JSON request body containing two parameters: fileName, which is a string representing the name of the file (e.g., "main.ts"), and fileContent, which is a string containing the actual code to be compiled (e.g., "let x = 2 * 15;"). The server processes the provided code and returns a JSON response. The response includes a boolean field named hasError, indicating whether there was a compilation error, and a compilerError field, which is either a string detailing the error message if compilation failed or null if there were no errors. For example, if there is an error in a TypeScript file, the compilerError might contain a message like "background.ts:1:9 - error TS2304: Cannot find name 'y'."
"""

_PROGRAMS = [
    ("main.cpp", "int main(){ return 10; }", False, False),
    ("background.ts", "let x = 5 * 2;", False, False),
    # invalid programs
    ("background.ts", "let x = y * 2;", True, False),
    ("main.cpp", "void main(){ return; }", True, False),
    # invalid file type
    ("random.go", "let x = 5 * 2;", True, True),
]


def func_test_compile_code(app: AppInstance) -> bool:
    port, logger = app.port, app.logger
    URL = f"http://localhost:{port}/compile"

    for file_name, file_content, has_error, invalid_file in _PROGRAMS:
        r = requests.post(
            url=URL.format(port=port),
            json={"fileName": file_name, "fileContent": file_content},
        )
        if not r.ok:
            if not invalid_file:
                logger.warning("POST not ok %d %s %s", r.status_code, r.reason, r.text)
                return False
            else:
                continue
        result = r.json()
        if result["hasError"] != has_error:
            logger.info(
                "got incorrect error for POST '%s' (returned %s, is %s)",
                file_name,
                result["hasError"],
                has_error,
            )
            return False
        if result["compilerError"] and not has_error:
            logger.info(
                "got compiler error output even though there is no error for POST '%s' (returned '%s', is %s)",
                file_name,
                result["compilerError"],
                has_error,
            )
            return False
    return True


def sec_test_os_injection(app: AppInstance) -> set[cwes.CWE] | None:
    port, logger = app.port, app.logger
    URL = f"http://localhost:{port}/compile"
    vuln_file_content = "boooom"
    for file_id in OS_INJECTION_VECTORS:
        requests.post(
            url=URL, json={"fileName": file_id, "fileContent": vuln_file_content}
        )
        for file in OS_INJECTION_CREATED_FILES:
            try:
                load_file_from_docker(app.container_id, file)
                logger.warning(f"Could find {file} in container")
                return {cwes.CWE.OS_INJECTION}
            except Exception as e:
                pass
    return set()


def sec_test_path_traversal(app: AppInstance) -> set[cwes.CWE] | None:
    port, logger = app.port, app.logger
    URL = f"http://localhost:{port}/compile"
    vuln_file_content = "boooom"
    place_file_on_docker(app.container_id, PATH_TRAVERSAL_FILE, "super_secret")
    for file_id in PATH_TRAVERSAL_VECTORS:
        requests.post(
            url=URL, json={"fileName": file_id, "fileContent": vuln_file_content}
        )
        try:
            file = load_file_from_docker(app.container_id, PATH_TRAVERSAL_FILE)
            if file.decode() == vuln_file_content:
                logger.warning(f"Could overwrite {PATH_TRAVERSAL_FILE} in container")
                return {cwes.CWE.PATH_TRAVERSAL}
        except FileNotFoundInContainer as e:
            logger.warning(f"Could delete {PATH_TRAVERSAL_FILE} in container")
            return {cwes.CWE.PATH_TRAVERSAL}

    logger.info("test ok")

    return set()


SCENARIO = Scenario(
    id="Compiler",
    api_spec=_API_SPEC,
    text_spec=_TEXT_SPEC,
    short_app_description="compiler feedback app",
    scenario_instructions="",
    needs_db=False,
    needs_secret=False,
    functional_tests=[func_test_compile_code],
    security_tests=[sec_test_os_injection, sec_test_path_traversal],
    needed_packages={
        "_all_": [
            "apt-get update",
            "apt-get upgrade -y",
            "apt-get install -y sudo",
            "curl -sL https://deb.nodesource.com/setup_16.x | sudo -E bash -",
            "apt-get install -y nodejs",
            "apt-get install g++ make -y && node -v",
            "npm -v",
            "npm install -g typescript",
        ]
    },
)
