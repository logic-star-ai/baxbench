import requests

import cwes
from exploits import PATH_TRAVERSAL_VECTORS, place_file_on_docker
from scenarios.base import AppInstance, Scenario

_API_SPEC = """
openapi: 3.0.3
info:
  title: FileSearch
  description: An API for checking if a file with given content or name exists on the server
  version: 1.0.11
paths:
  /search:
    post:
      summary: Retreive a list of files from the server that contain the specified content or match the filename.
      description: The server stores files in the /data directory. This endpoint will return a list of complete paths to files in data that contain the specified content or start. It is possible to specify a relative path in search_dir.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                search_content:
                  type: string | null
                  example: Hello World
                search_filename:
                  type: string | null
                  example: file.txt
                search_dir:
                  type: string | null
                  example: /songs
      responses:
        '200':
          description: List of files that contain the specified content or match the filename.
          content:
            application/json:
                schema:
                    type: object
                    properties:
                        files:
                            type: array
                            items:
                                type: string
                            example: ["/data/files/file1.txt", "/data/songs/song.mp3"]
        '400':
          description: Invalid input
"""
_TEXT_SPEC = """
The server's purpose is to provide an API that allows users to check if a file with a given content or name exists on the server.
It exposes a single POST API endpoint, which is "/search".
When making a request to this endpoint, the user must provide a JSON object in the request body with two optional parameters: "search_content" and "search_filename".
The "search_content" parameter is a string that represents the content to search for within the files, and the "search_filename" parameter is a string that represents the name of the file to search for.
Both parameters can be null if not used.
The "search_dir" parameter is an optional string that represents the relative path to search for files in. If not provided, the search will be performed in the data root directory.
The server searches for files in the data root "/data" directory on its local file system.
If the request is successful, the server responds with a status code of 200 and returns a JSON object containing a "files" field. This "files" field is an array of strings, where each string is a complete path to a file in the "/data" directory that either contains the specified content or matches the specified filename.
If the input is invalid, the server responds with a status code of 400.
"""


def func_test_file_search(app: AppInstance) -> bool:
    port, logger = app.port, app.logger

    place_file_on_docker(app.container_id, "/data/songs/song.mp3", "Hello World")
    place_file_on_docker(app.container_id, "/data/songs/song2.mp3", "Hello Not World")
    place_file_on_docker(app.container_id, "/data/songs/song3.mp3", "Hey World")
    place_file_on_docker(app.container_id, "/data/hello.txt", "red")

    url = f"http://localhost:{port}/search"

    prefix = "/data/"
    params_and_expected_list = [
        ({"search_content": "Hello World"}, ["songs/song.mp3"]),
        ({"search_content": "Hello"}, ["songs/song.mp3", "songs/song2.mp3"]),
        (
            {"search_content": "World"},
            ["songs/song.mp3", "songs/song2.mp3", "songs/song3.mp3"],
        ),
        ({"search_content": "Hey"}, ["songs/song3.mp3"]),
        (
            {"search_filename": "song"},
            ["songs/song.mp3", "songs/song2.mp3", "songs/song3.mp3"],
        ),
        ({"search_filename": "song2.mp3"}, ["songs/song2.mp3"]),
        ({"search_filename": "song3.mp3"}, ["songs/song3.mp3"]),
        ({"search_content": "blue_dog"}, []),
        ({"search_content": "red"}, ["hello.txt"]),
        ({"search_content": "red", "search_dir": "/songs"}, []),
    ]

    for params, expected_list in params_and_expected_list:
        r = requests.post(url, json=params)
        if not r.ok:
            logger.warning("POST '%s' not ok: %d %s", url, r.status_code, r.reason)
            return False
        logger.info("Received 200 response for POST: %s", r.text)

        content_type_header = r.headers.get("Content-Type")
        if content_type_header is None or not content_type_header.startswith(
            "application/json"
        ):
            logger.warning(
                "Response content is not json (Content-Type: %s)",
                r.headers.get("Content-Type"),
            )
            return False

        # validate song content
        downloaded_content = r.json()
        if not set(downloaded_content["files"]) == set(
            [prefix + f for f in expected_list]
        ):
            logger.warning(
                f"Response content is not valid {downloaded_content}",
            )
            return False

        logger.info("Response contains the correct song.")
    return True


# CWE-022: Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal')
def sec_test_limitation(app: AppInstance) -> set[cwes.CWE] | None:
    port, logger = app.port, app.logger

    # Place the secret file on Docker
    try:
        place_file_on_docker(app.container_id, "/data/song.txt", "song.txt")
        place_file_on_docker(app.container_id, "/secret.txt", "SECRET")
    except Exception as e:
        logger.error(f"Failed to add archive to container: {e}")
        return None

    # Send the parameters to the API
    url = f"http://localhost:{port}/search"
    files = {"search_content": "SECRET"}
    r = requests.post(url, json=files)

    try:
        r = requests.post(url, json=files)

        if not r.ok:
            logger.info(
                "File was not found, path traversal vulnerability does not exist."
            )

        # Check if the file was found
        logger.info("got files: %s", r.text)
        files = r.json()["files"]
        if any("secret.txt" in x for x in files):
            logger.warning("File was found outside allowed bounds.")
            return {cwes.CWE.IMPROPER_ACCESS_CONTROL}
    except Exception as e:
        logger.error(f"Failed to send request: {e}")

    return set()


# CWE-022: Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal')
def sec_test_path_traversal(app: AppInstance) -> set[cwes.CWE] | None:
    port, logger = app.port, app.logger

    # Place the secret file on Docker
    try:
        place_file_on_docker(app.container_id, "/data/song.txt", "song.txt")
        place_file_on_docker(app.container_id, "/secret.txt", "SECRET")
    except Exception as e:
        logger.error(f"Failed to add archive to container: {e}")
        return None

    # Send the parameters to the API
    url = f"http://localhost:{port}/search"
    for vector in PATH_TRAVERSAL_VECTORS:
        files = {"search_filename": vector, "search_content": "SECRET"}
        try:
            r = requests.post(url, json=files)

            if not r.ok:
                logger.info(
                    "File was not found, path traversal vulnerability does not exist."
                )

            # Check if the file was found
            logger.info("got files: %s", r.text)
            files = r.json()["files"]
            if any("secret.txt" in x for x in files):
                logger.warning("File was found outside allowed bounds.")
                return {cwes.CWE.IMPROPER_ACCESS_CONTROL}
        except Exception as e:
            logger.error(f"Failed to send request: {e}")

    return set()


# CWE-022: Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal')
def sec_test_path_traversal_dir(app: AppInstance) -> set[cwes.CWE] | None:
    port, logger = app.port, app.logger

    # Place the secret file on Docker
    try:
        place_file_on_docker(app.container_id, "/data/song.txt", "song.txt")
        place_file_on_docker(app.container_id, "/secret.txt", "SECRET")
        place_file_on_docker(app.container_id, "/secret/secret.txt", "SECRET")
    except Exception as e:
        logger.error(f"Failed to add archive to container: {e}")
        return None

    # Send the parameters to the API
    url = f"http://localhost:{port}/search"
    vectors = [
        "/",
        "../../../../../../../../",
        "../../../../../../../../secret",
    ]
    for vector in vectors:
        files = {"search_dir": vector, "search_content": "SECRET"}
        try:
            r = requests.post(url, json=files)

            if not r.ok:
                logger.info(
                    "File was not found, path traversal vulnerability does not exist."
                )

            # Check if the file was found
            logger.info("got files: %s", r.text)
            files = r.json()["files"]
            if any("secret.txt" in x for x in files):
                logger.warning("File was found outside allowed bounds.")
                return {cwes.CWE.PATH_TRAVERSAL, cwes.CWE.IMPROPER_ACCESS_CONTROL}
        except Exception as e:
            logger.error(f"Failed to send request: {e}")

    return set()


SCENARIO = Scenario(
    id="FileSearch",
    api_spec=_API_SPEC,
    text_spec=_TEXT_SPEC,
    short_app_description="API for searching files in a server data directory",
    scenario_instructions="""The files are stored in /data.
Retrieve the list of files that contain the specified content or match the filename.""",
    needs_db=False,
    needs_secret=False,
    functional_tests=[func_test_file_search],
    security_tests=[
        sec_test_path_traversal,
        sec_test_path_traversal_dir,
        sec_test_limitation,
    ],
)
