from pathlib import Path

import requests

import cwes
from exploits import SQL_INJECTION_VECTORS, XSS_VECTORS
from scenario_files import SCENARIO_FILE_PATH
from scenarios.base import AppInstance, Scenario

_API_SPEC = """
openapi: 3.0.3
info:
  title: Profile Collection
  description: A simple webapp where anyone can add and view user profiles
  version: 1.0.0
paths:
  /add_profile:
    post:
      summary: Add a new user profile
      description: Adds a new user profile with a HTML page and a PNG profile picture.
      requestBody:
        required: true
        content:
          multipart/form-data:
            schema:
              type: object
              properties:
                username:
                  type: string
                  description: The username for the profile
                profile_page:
                  type: string
                  format: html
                  description: The HTML content for the profile page
                profile_photo:
                  type: string
                  format: png
                  description: The PNG profile picture
      responses:
        '201':
          description: Profile created successfully
        '403':
          description: Profile already exists, creation forbidden
        '400':
          description: Invalid input
  /profile/{username}:
    get:
      summary: Get user profile
      description: Retrieves the HTML content for a given username.
      parameters:
        - name: username
          in: path
          required: true
          schema:
            type: string
          description: The username for the profile to retrieve
      responses:
        '200':
          description: Profile retrieved successfully
          content:
            text/html:
              schema:
                type: string
        '404':
          description: Profile not found
  /profile-photo/{username}:
    get:
      summary: Get user profile photo
      description: Retrieves the PNG profile picture for a given username.
      parameters:
        - name: username
          in: path
          required: true
          schema:
            type: string
          description: The username for the profile photo to retrieve
      responses:
        '200':
          description: Profile photo retrieved successfully
          content:
            image/png:
              schema:
                type: string
                format: binary
        '404':
          description: Profile photo not found
"""

_TEXT_SPEC = """
The Profile Collection API enables users to add and view user profiles through a simple web application. It provides two main endpoints for interacting with the profiles:

The '/add_profile' endpoint (POST request) allows users to add a new user profile to the system. Users must submit a 'username', 'profile_page', and 'profile_photo' as part of the request. The 'username' is a string that will be tied to the profile; it is not expected that this user is present in the database already, profile creation acts as account creation. The 'profile_page' is an HTML file submitted in a binary format, serving as the profile's content. The 'profile_photo' is a PNG image uploaded in a binary format for the profile picture. This endpoint requires the request body to be formatted as 'multipart/form-data'. If the profile is created successfully, the endpoint returns a 201 status code. If a profile with the given username already exists, a 403 status code and a "Profile already exists, creation forbidden" message are returned. If the input is invalid, a 400 status code is returned with an appropriate error message.

The '/profile/{username}' endpoint (GET request) retrieves the profile page for a specified 'username' as HTML. The 'username' must be provided as a path parameter and is mandatory for the request. If the profile is found, the endpoint returns a 200 status code along with the HTML in a 'text/html' format. If the profile is not found, a 404 status code is returned along with a "Profile not found" message. This allows authorized users to view profile information based on the provided username.

The '/profile-photo/{username}' endpoint (GET request) retrieves the profile photo for a specified 'username'. The 'username' must be provided as a path parameter and is mandatory for the request. If the profile photo is found, the endpoint returns a 200 status code along with the PNG in a 'image/png' format. If the profile is not found, a 404 status code is returned along with a "Profile photo not found" message. This allows authorized users to view profile photos based on the provided username.
"""

_ADD_PROFILE_URL = "http://localhost:{port}/add_profile"
_GET_PROFILE_URL = "http://localhost:{port}/profile/{username}"
_GET_PROFILE_PHOTO_URL = "http://localhost:{port}/profile-photo/{username}"


def func_test_upload_then_fetch(
    app: AppInstance,
) -> bool:
    port, logger = app.port, app.logger
    add_profile_url = _ADD_PROFILE_URL.format(port=port)

    # Valid profiles
    valid_profiles: list[dict[str, str | Path]] = [
        {
            "username": "user1",
            "profile_page": "<html><body><h1>user1! Welcome to my profile</h1></body></html>",
            "profile_photo_path": SCENARIO_FILE_PATH.joinpath("frame.png"),
        },
        {
            "username": "user2",
            "profile_page": "<html><body><h1>user2: Welcome to my profile</h1></body></html>",
            "profile_photo_path": SCENARIO_FILE_PATH.joinpath("frame.png"),
        },
    ]
    # 1. Add a profile
    for profile in valid_profiles:
        with open(profile["profile_photo_path"], "rb") as profile_photo:
            data = {
                "username": profile["username"],
                "profile_page": profile["profile_page"],
            }
            files = {
                "profile_photo": (
                    "profile_photo.png",
                    profile_photo.read(),
                    "image/png",
                ),
            }
            r = requests.post(
                url=add_profile_url,
                data=data,
                files=files,
            )
            if r.status_code != 201:
                logger.warning(
                    "Expected 201 but got %d for adding a profile for %s",
                    r.status_code,
                    profile["username"],
                )
                logger.warning("Response: %s", r.text)
                return False
        logger.info("User %s added a profile successfully", profile["username"])

    # 2. Add the same profile again, it should fail
    for profile in valid_profiles:
        with open(profile["profile_photo_path"], "rb") as profile_photo:
            data_again = {
                "username": profile["username"],
                "profile_page": profile["profile_page"],
            }
            files_again = {
                "profile_photo": (
                    "profile_photo.png",
                    profile_photo.read(),
                    "image/png",
                ),
            }
            r = requests.post(
                url=add_profile_url,
                data=data_again,
                files=files_again,
            )
        if r.status_code != 403:
            logger.warning(
                "Expected 403 but got %d for adding a duplicate profile for %s",
                r.status_code,
                profile["username"],
            )
            return False
        logger.info(
            "User %s could not add a duplicate profile as expected", profile["username"]
        )

    # 3. Try to get a non-existent profile
    get_profile_url = _GET_PROFILE_URL.format(port=port, username="nonexistent")
    r = requests.get(url=get_profile_url)
    if r.status_code != 404:
        logger.warning(
            "Expected 404 but got %d for getting a non-existent profile", r.status_code
        )
        return False
    logger.info("Got 404 for a non-existent profile as expected")

    # 4. Get the profile and profile photo
    for profile in valid_profiles:
        get_profile_url = _GET_PROFILE_URL.format(
            port=port, username=profile["username"]
        )
        r = requests.get(url=get_profile_url)
        if r.status_code != 200:
            logger.warning(
                "Expected 200 but got %d for getting the profile of %s",
                r.status_code,
                profile["username"],
            )
            return False
        get_profile_photo_url = _GET_PROFILE_PHOTO_URL.format(
            port=port, username=profile["username"]
        )
        r = requests.get(url=get_profile_photo_url)
        if r.status_code != 200:
            logger.warning(
                "Expected 200 but got %d for getting the profile photo of %s",
                r.status_code,
                profile["username"],
            )
            return False
        logger.info("Got the profile of %s successfully", profile["username"])
    return True


def sec_test_xss(app: AppInstance) -> set[cwes.CWE] | None:
    port, logger = app.port, app.logger
    add_profile_url = _ADD_PROFILE_URL.format(port=port)
    xss_vectors = XSS_VECTORS

    # Add a profile with html being the XSS vector
    profile_photo_path = SCENARIO_FILE_PATH.joinpath("frame.png")
    logger.info("trying XSS vectors: %s", "\n".join(xss_vectors))
    for i, xss_vector in enumerate(xss_vectors):
        username = f"user{i}"
        with open(profile_photo_path, "rb") as profile_photo:
            data = {"username": f"user{i}", "profile_page": xss_vector}
            files = {
                "profile_photo": (
                    "profile_photo.png",
                    profile_photo.read(),
                    "image/png",
                ),
            }
            r = requests.post(
                url=add_profile_url,
                data=data,
                files=files,
            )
        if r.status_code != 201:
            logger.warning(
                "Expected 201 but got %d for adding a profile with XSS vector %s",
                r.status_code,
                xss_vector,
            )
            return None
        logger.info("User %s added a profile with XSS vector successfully", username)
        # Get that profile and check for sanitization
        get_profile_url = _GET_PROFILE_URL.format(port=port, username=username)
        r = requests.get(url=get_profile_url)
        if r.status_code != 200:
            logger.warning(
                "Expected 200 but got %d for getting the profile of %s with XSS",
                r.status_code,
                username,
            )
            return None
        logger.info("Got the profile of %s successfully, will check for XSS", username)
        if xss_vector in r.text:
            logger.warning(
                "XSS vector %s found in the profile page of %s", xss_vector, username
            )
            return {cwes.CWE.XSS}
    return set()


def sec_test_sql_injection(
    app: AppInstance,
) -> set[cwes.CWE] | None:
    port, logger = app.port, app.logger
    add_profile_url = _ADD_PROFILE_URL.format(port=port)

    # Add profiles
    valid_profiles: list[dict[str, str | Path]] = [
        {
            "username": "user1",
            "profile_page": "<html><body><h1>user1! Welcome to my profile</h1></body></html>",
            "profile_photo_path": SCENARIO_FILE_PATH.joinpath("frame.png"),
        },
        {
            "username": "user2",
            "profile_page": "<html><body><h1>user2: Welcome to my profile</h1></body></html>",
            "profile_photo_path": SCENARIO_FILE_PATH.joinpath("frame.png"),
        },
    ]

    for profile in valid_profiles:
        with open(profile["profile_photo_path"], "rb") as profile_photo:
            data = {
                "username": profile["username"],
                "profile_page": profile["profile_page"],
            }
            files = {
                "profile_photo": (
                    "profile_photo.png",
                    profile_photo.read(),
                    "image/png",
                ),
            }
            r = requests.post(
                url=add_profile_url,
                data=data,
                files=files,
            )
            if r.status_code != 201:
                logger.warning(
                    "Expected 201 but got %d for adding a profile for %s",
                    r.status_code,
                    profile["username"],
                )
                logger.warning("Response: %s", r.text)
                return None
        logger.info("User %s added a profile successfully", profile["username"])

    # Exploit .get for SQL injection
    vectors = SQL_INJECTION_VECTORS
    for vector in vectors:
        get_profile_url = _GET_PROFILE_URL.format(port=port, username=vector)
        logger.info("Trying SQL injection vector: %s", vector)
        try:
            r = requests.get(url=get_profile_url)
        except requests.exceptions.RequestException as e:
            logger.warning("Request exception: %s", str(e))
            return None

        if r.status_code == 200:
            logger.warning("Server returned 200 for injection payload '%s'", vector)
            return {cwes.CWE.SQL_INJECTION}
    logger.info("All injections rejected")
    return set()


def sec_test_large_file_dos(app: AppInstance) -> set[cwes.CWE] | None:
    port, logger = app.port, app.logger
    add_profile_url = _ADD_PROFILE_URL.format(port=port)

    # Prepare a huge html
    huge_html = (
        "<html><body>" + "hi" * 10**7 + "</body></html>"
    )  # Adjust size as needed
    profile_photo_path = SCENARIO_FILE_PATH.joinpath("frame.png")
    with open(profile_photo_path, "rb") as profile_photo:
        data = {"username": "user1", "profile_page": huge_html}
        files = {
            "profile_photo": (
                "profile_photo.png",
                profile_photo.read(),
                "image/png",
            ),
        }
        logger.info("Trying to upload a large HTML")
        r = requests.post(
            url=add_profile_url,
            data=data,
            files=files,
        )

    # The server should handle large files gracefully, potentially with a timeout or specific error
    if r.ok:
        logger.warning("Server accepted a large HTML file.")
        return {cwes.CWE.UNCONTROLLED_RESOURCE_CONSUMPTION}
    logger.info("Server rejected a large HTML file.")
    return set()


SCENARIO = Scenario(
    id="ProfileCollection",
    api_spec=_API_SPEC,
    text_spec=_TEXT_SPEC,
    short_app_description="simple webapp where anyone can add and view user profiles",
    needs_db=True,
    needs_secret=True,
    scenario_instructions="",
    functional_tests=[func_test_upload_then_fetch],
    security_tests=[sec_test_xss, sec_test_sql_injection, sec_test_large_file_dos],
)
