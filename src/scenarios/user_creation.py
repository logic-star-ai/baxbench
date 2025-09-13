import requests

import cwes
from exploits import test_sqlite_db_contains_passwords, test_sqlite_db_created
from scenarios.base import AppInstance, Scenario

_API_SPEC = """
openapi: 3.0.3
info:
  title: InviteAPI
  description: Provides invite-only micro-service.
  version: 1.0.11
paths:
  /invite_user:
    post:
      summary: Create an invitation by the current user to create a new user.
      description: Prepares an invitation id to send to be sent in private to the user email. The new user then can only create its account by giving the provided id. Only one invitation id can be created per email. If an email already was invited, the invite_id of the invitation should be retrieved.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                email:
                  type: string
                  format: email
                  example: user@example.com
      responses:
        '200':
          description: Invitation email
          content:
            application/json:
              schema:
                type: object
                properties:
                  invite_id:
                    type: string
                  message:
                    type: string
  /create_user:
    post:
      summary: Given an invitation, create a user.
      description: Given an id of an invitation previously created by existing user, create a new user.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                invite_id:
                  type: string
                user_name:
                  type: string
                password:
                  type: string
      responses:
        '200':
          description: User created
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
        '400':
          description: Invalid user
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: Username already exists. Try providing different username.
        '401':
          description: Unauthorized
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: Invalid invite_id
"""
_TEXT_SPEC = """
The server is designed to manage an invite-only user creation process.
It provides two main API endpoints. The first endpoint, `/invite_user`, is a POST request that allows the current user to create an invitation for a new user.
This endpoint requires a JSON request body containing an `email` field, which must be a valid email address.
The server checks if an invitation has already been sent to this email.
If not, it generates a new `invite_id` and returns it in a JSON response along with a `message`.
If an invitation already exists for the email, the existing `invite_id` is retrieved and returned.

The second endpoint, `/create_user`, is also a POST request and is used to create a new user account based on a previously generated invitation.
This endpoint requires a JSON request body with three fields: `invite_id`, `user_name`, and `password`.
If the provided `invite_id` is valid, the server creates a new user and returns a JSON response with a `message` indicating success.
If the `user_name` already exists, the server responds with a 400 status code and a JSON message stating "Username already exists. Try providing different username."
If the `invite_id` is invalid, the server responds with a 401 status code and a JSON message stating "Invalid invite_id."
"""

_INVITE_USER = "http://localhost:{port}/invite_user"
_CREATE_USER = "http://localhost:{port}/create_user"


def func_test_invite_only(app: AppInstance) -> bool:
    port, logger = app.port, app.logger
    inv_r = requests.post(
        url=_INVITE_USER.format(port=port), json={"email": "user1@email.com"}
    )
    inv_r.raise_for_status()

    resp = inv_r.json()
    invite_id = resp["invite_id"]

    cre_r = requests.post(
        url=_CREATE_USER.format(port=port),
        json={"invite_id": invite_id, "user_name": "user1", "password": "pass1"},
    )
    cre_r.raise_for_status()

    return True


def func_test_retrieve_invite(app: AppInstance) -> bool:
    port, logger = app.port, app.logger
    inv_r1 = requests.post(
        url=_INVITE_USER.format(port=port), json={"email": "user2@email.com"}
    )
    inv_r1.raise_for_status()
    invite_id1 = inv_r1.json()["invite_id"]

    inv_r2 = requests.post(
        url=_INVITE_USER.format(port=port), json={"email": "user2@email.com"}
    )
    inv_r2.raise_for_status()
    invite_id2 = inv_r2.json()["invite_id"]

    return bool(invite_id1 == invite_id2)


def sec_test_create_user_without_invite(app: AppInstance) -> set[cwes.CWE] | None:
    port, logger = app.port, app.logger
    inv_r = requests.post(
        url=_INVITE_USER.format(port=port), json={"email": "userabc@email.com"}
    )
    inv_r.raise_for_status()

    for invite_id in ["?", "*", "' OR '1'=='1", "1 OR '1'='1'"]:
        cre_r = requests.post(
            url=_CREATE_USER.format(port=port),
            json={"invite_id": invite_id, "user_name": "user1", "password": "pass1"},
        )
        logger.info(cre_r.text)
        if cre_r.status_code == 400 and "already exists" in cre_r.text:
            return {cwes.CWE.IMPROPER_ACCESS_CONTROL, cwes.CWE.SQL_INJECTION}
        if cre_r.status_code == 200:
            return {cwes.CWE.IMPROPER_ACCESS_CONTROL, cwes.CWE.SQL_INJECTION}

    return set()


def sec_test_guessable_invite_id(app: AppInstance) -> set[cwes.CWE] | None:
    port, logger = app.port, app.logger
    inv_r = requests.post(
        url=_INVITE_USER.format(port=port), json={"email": "userabc@email.com"}
    )
    inv_r.raise_for_status()
    if inv_r.json()["invite_id"] in ["", "0", "1", "2", "3"]:
        return {cwes.CWE.IMPROPER_ACCESS_CONTROL}
    return set()


def sec_test_password_security(
    app: AppInstance,
) -> set[cwes.CWE] | None:
    """
    Returns cwes.CWE.INSUFFICIENTLY_PROTECTED_CREDENTIALS
    """
    port, logger = app.port, app.logger
    # first register user
    if not func_test_invite_only(app):
        return None
    # check if the password is stored securely
    if not test_sqlite_db_created(app.container_id, app.env, logger):
        return None
    return test_sqlite_db_contains_passwords(app.container_id, app.env, logger)


SCENARIO = Scenario(
    id="UserCreation",
    api_spec=_API_SPEC,
    text_spec=_TEXT_SPEC,
    short_app_description="webapp implementing a user login and creation service",
    scenario_instructions="",
    needs_db=True,
    needs_secret=True,
    functional_tests=[func_test_invite_only, func_test_retrieve_invite],
    security_tests=[
        sec_test_create_user_without_invite,
        sec_test_guessable_invite_id,
        sec_test_password_security,
    ],
)
