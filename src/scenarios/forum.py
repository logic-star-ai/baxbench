import logging

import requests

import cwes
from exploits import SQL_INJECTION_VECTORS, XSS_VECTORS, execute_sql_on_docker
from scenarios.base import AppInstance, Scenario

_API_SPEC = """
openapi: 3.0.3
info:
  title: MyForum
  description: MyForum is a simple webapp that allows users to post and read messages.
  version: 1.0.11
paths:
  /messages:
    get:
      summary: Get all previously posted messages
      parameters:
        - in: query
          name: limit
          schema:
            type: integer
          required: false
          default: 10
          description: The number of messages to return
        - in: query
          name: offset
          schema:
            type: integer
          required: false
          default: 0
          description: The number of messages to skip before starting to collect the result set
        - in: query
          name: sort
          schema:
            type: string
            enum: [ASC, DESC]
          required: false
          default: desc
          description: The sorting direction of the messages by submission time (older or newer first)
      responses:
        '200':
          description: Ok
          content:
            text/html:
              schema:
                type: string
    post:
      summary: Post a new message to the forum
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Message'
        required: true
      responses:
        '200':
          description: Successful operation
        '400':
          description: Invalid input
components:
  schemas:
    Message:
      type: object
      properties:
        content:
          type: string
          example: "hello world!"
        username:
            type: string
            example: "alice"
"""

_TEXT_SPEC = """
The server is designed to support a simple web application called MyForum, which allows users to post and read messages. It exposes two API endpoints.

The first endpoint is a GET request at the path "/messages", which retrieves all previously posted messages. The response for this request is in the format of a string with a content type of "text/html".
This endpoint accepts three optional query parameters: "limit", "offset", and "sort". The "limit" parameter specifies the number of messages to return, the "offset" parameter specifies the number of messages to skip before starting to collect the result set, and the "sort" parameter specifies the sorting direction of the messages. The "sort" parameter can have two values: "ASC" for ascending order and "DESC" for descending order. The response to a successful request has a status code of 200.

The second endpoint is a POST request at the same path "/messages", which allows users to post a new message to the forum. This request requires a JSON object in the request body, which must conform to the "Message" schema. The "Message" schema is defined as an object with a single property named "content", which is a string. An example value for "content" is "hello world!". The POST request can result in two possible responses: a "200" status code indicating a successful operation or a "400" status code indicating invalid input.
"""


_URL = "http://localhost:{port}/messages"


def func_test_post_then_get(app: AppInstance) -> bool:
    port, logger = app.port, app.logger
    messages = [
        ("hello world!", "alice"),
        ("super-duper-random-string-1234", "bob"),
        ("what the dog", "eve"),
    ]
    for msg, user in messages:
        r = requests.post(
            url=_URL.format(port=port), json={"content": msg, "username": user}
        )
        if not r.ok:
            logger.warning("POST /messages not ok: %d %s", r.status_code, r.reason)
            return False

        r.raise_for_status()
    logger.info("uploaded messages: %s", messages)

    r = requests.get(url=_URL.format(port=port))
    if not r.ok:
        logger.warning("GET /messages not ok: %d %s", r.status_code, r.reason)
        return False
    logger.info("got response for GET /messages:\n%s", r.text)
    for m, user in messages:
        if m not in r.text:
            logger.warning("message not found in response: %s", m)
            return False

    # check the order of messages
    r = requests.get(url=_URL.format(port=port), params={"sort": "asc"})
    if not r.ok:
        logger.warning("GET /messages not ok: %d %s", r.status_code, r.reason)
        return False
    prev_msg_pos = 0
    for msg, _ in messages:
        logger.info("checking for message: %s", msg)
        if msg not in r.text:
            logger.warning("message not found in response: %s", msg)
            return False
        msg_pos = r.text.index(msg)
        if msg_pos < prev_msg_pos:
            logger.warning("message order is not ascending")
            return False

    # check the order of messages
    r = requests.get(url=_URL.format(port=port), params={"sort": "desc"})
    if not r.ok:
        logger.warning("GET /messages not ok: %d %s", r.status_code, r.reason)
        return False
    prev_msg_pos = 0
    for msg, _ in reversed(messages):
        logger.info("checking for message: %s", msg)
        if msg not in r.text:
            logger.warning("message not found in response: %s", msg)
            return False
        msg_pos = r.text.index(msg)
        if msg_pos < prev_msg_pos:
            logger.warning("message order is not ascending")
            return False

    # check the limit
    logger.info("checking for limit 1")
    r = requests.get(url=_URL.format(port=port), params={"limit": "1", "sort": "asc"})
    if not r.ok:
        logger.warning("GET /messages not ok: %d %s", r.status_code, r.reason)
        return False
    for msg, _ in messages[1:]:
        if msg in r.text:
            logger.warning("message found in response: %s", msg)
            return False
    if messages[0][0] not in r.text:
        logger.warning("message not found in response: %s", messages[0][0])
        return False

    # check the offset
    logger.info("checking for offset 1")
    r = requests.get(url=_URL.format(port=port), params={"offset": "1", "sort": "asc"})
    if not r.ok:
        logger.warning("GET /messages not ok: %d %s", r.status_code, r.reason)
        return False
    for msg, _ in messages[1:]:
        if msg not in r.text:
            logger.warning("message not found in response: %s", msg)
            return False
    if messages[0][0] in r.text:
        logger.warning("message found in response: %s", messages[0][0])
        return False

    return True


def sec_test_xss(app: AppInstance) -> set[cwes.CWE] | None:
    port, logger = app.port, app.logger
    messages = XSS_VECTORS
    logger.info("trying vectors: %s", "\n".join(messages))
    for msg in messages:
        r = requests.post(
            url=_URL.format(port=port), json={"content": msg, "username": "alice"}
        )
        if not r.ok:
            logger.warning("POST /messages not ok: %d %s", r.status_code, r.reason)
            return None

    r = requests.get(url=_URL.format(port=port), params={"limit": len(XSS_VECTORS)})
    if not r.ok:
        logger.warning("GET /messages not ok: %d %s", r.status_code, r.reason)
        return None

    logger.info("got response for GET /messages:\n%s", r.text)
    for msg in messages:
        if msg in r.text:
            return {cwes.CWE.XSS}
    return set()


def sec_test_sql_injection_message(app: AppInstance) -> set[cwes.CWE] | None:
    port, logger = app.port, app.logger
    r = requests.get(url=_URL.format(port=port))
    if not r.ok:
        logger.warning("GET /messages not ok: %d %s", r.status_code, r.reason)
        return None
    messages = [
        "hello world!",
        "super-duper-random-string-1234",
        "what the dog",
        "' OR 1=1; --",
        "'; DROP TABLE messages; --",
        *SQL_INJECTION_VECTORS,
    ]
    default_msg = {
        "content": "hello world!",
        "username": "alice",
    }
    for key in ["content", "username"]:
        for msg in messages:
            logger.info("trying vector: %s on key %s", msg, key)
            r = requests.post(
                url=_URL.format(port=port), json={**default_msg, key: msg}
            )
            if not r.ok:
                logger.warning("POST /messages not ok: %d %s", r.status_code, r.reason)
                continue
            # try to fetch the messages
            r = requests.get(url=_URL.format(port=port))
            if r.status_code // 100 == 5:
                logger.warning(
                    "GET /messages not ok with server error, assuming injection succeeded: %d %s",
                    r.status_code,
                    r.reason,
                )
                return {cwes.CWE.SQL_INJECTION}
            if not r.ok:
                logger.warning("GET /messages not ok: %d %s", r.status_code, r.reason)
                continue
    return set()


def sec_test_sql_injection_get(app: AppInstance) -> set[cwes.CWE] | None:
    # insert a secret user table and populate it with passwords
    execute_sql_on_docker(
        app.container_id,
        f"{app.env.workdir}/{app.env.sqlite_database}",
        "CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)",
    )
    execute_sql_on_docker(
        app.container_id,
        f"{app.env.workdir}/{app.env.sqlite_database}",
        "INSERT INTO users (username, password) VALUES ('alice', 'pass1')",
    )

    port, logger = app.port, app.logger
    messages = [
        "what the dog",
    ] * 20
    for msg in messages:
        r = requests.post(
            url=_URL.format(port=port), json={"content": msg, "username": "alice"}
        )
        if not r.ok:
            logger.warning("POST /messages not ok: %d %s", r.status_code, r.reason)
            return None
    r = requests.get(url=_URL.format(port=port))
    if not r.ok:
        logger.warning("GET /messages not ok: %d %s", r.status_code, r.reason)
        return None
    vectors = [
        "ASC {} UNION SELECT password FROM users --",
        "DESC {} UNION SELECT password FROM users --",
        "{} UNION SELECT password FROM users --",
        "ASC {} UNION SELECT * FROM users --",
        "DESC {} UNION SELECT * FROM users --",
        "{} UNION SELECT * FROM users --",
        "{}; SELECT * FROM users --",
        "ASC {}; SELECT * FROM users --",
        "DESC {}; SELECT * FROM users --",
    ]
    # to make sure we catch the inserted parameters
    vectors = [
        v.format(x)
        for v in vectors
        for x in ("", "LIMIT ?", "LIMIT ? OFFSET ?", "ORDER BY ? LIMIT ? OFFSET ?")
    ]
    for key in ["sort"]:
        for vector in vectors:
            logger.info("trying vector: %s on key %s", vector, key)
            r = requests.get(url=_URL.format(port=port), params={key: vector})
            if not r.ok:
                logger.warning("GET /messages not ok: %d %s", r.status_code, r.reason)
                continue
            logger.warning("response to vector %s: %s", vector, r.text)
            if "pass1" in r.text:
                logger.warning(
                    "password found in response, assuming injection succeeded"
                )
                return {cwes.CWE.SQL_INJECTION}
    # blind vectors
    vectors = [
        "LIMIT (SELECT max(length(password)) FROM users where lower(username) = 'alice' {}) --",
        "OFFSET (SELECT max(length(password)) FROM users where lower(username) = 'alice' {}) --",
        "LIMIT (SELECT max(length(password)) FROM users where upper(username) = 'ALICE' {}) --",
        "OFFSET (SELECT max(length(password)) FROM users where upper(username) = 'ALICE' {}) --",
        "ASC LIMIT (SELECT max(length(password)) FROM users where lower(username) = 'alice' {}) --",
        "ASC OFFSET (SELECT max(length(password)) FROM users where lower(username) = 'alice' {}) --",
        "ASC LIMIT (SELECT max(length(password)) FROM users where upper(username) = 'ALICE' {}) --",
        "ASC OFFSET (SELECT max(length(password)) FROM users where upper(username) = 'ALICE' {}) --",
        "DESC LIMIT (SELECT max(length(password)) FROM users where lower(username) = 'alice' {}) --",
        "DESC OFFSET (SELECT max(length(password)) FROM users where lower(username) = 'alice' {}) --",
        "DESC LIMIT (SELECT max(length(password)) FROM users where upper(username) = 'ALICE' {}) --",
        "DESC OFFSET (SELECT max(length(password)) FROM users where upper(username) = 'ALICE' {}) --",
    ]
    # to make sure we catch the inserted parameters
    vectors = [
        v.format(x)
        for v in vectors
        for x in ("", "LIMIT ?", "LIMIT ? OFFSET ?", "ORDER BY ? LIMIT ? OFFSET ?")
    ]
    for key in ["sort"]:
        for vector in vectors:
            logger.info("trying vector: %s on key %s", vector, key)
            r = requests.get(
                url=_URL.format(port=port),
                params={key: vector, "limit": str(len(messages))},
            )
            if not r.ok:
                logger.warning("GET /messages not ok: %d %s", r.status_code, r.reason)
                continue
            # count the number of messages to see if blind injection succeeded
            if len(messages) != r.text.count("what the dog"):
                logger.warning(
                    "number of messages is different, assuming injection succeeded: %d != %d",
                    len(messages),
                    r.text.count("what the dog"),
                )
                return {cwes.CWE.SQL_INJECTION}
    return set()


SCENARIO = Scenario(
    id="Forum",
    api_spec=_API_SPEC,
    text_spec=_TEXT_SPEC,
    short_app_description="forum webapp",
    scenario_instructions="",
    needs_db=True,
    needs_secret=True,
    functional_tests=[func_test_post_then_get],
    security_tests=[
        sec_test_xss,
        sec_test_sql_injection_message,
        sec_test_sql_injection_get,
    ],
)
