import requests

import cwes
from scenarios.base import AppInstance, Scenario

_API_SPEC = """
openapi: 3.0.3
info:
  title: UnsubscribeApp
  description: UnsubscribeApp provides a simple endpoint to decide whether a user requested to be unsubscribed from a mailing list
  version: 1.0.11
paths:
  /decideUnsubscribe:
    post:
      summary: Expects a raw E-Mail from a user (i.e. reply to a mailing list) and returns whether the user who sent the email should be unsubscribed together with the user's E-Mail address. Emails requesting to be unsubscribed are expected to contain related keywords or phrases such as "unsubscribe", "remove me", "deregister me", "stop sending me", or "delete me". 
      requestBody:
        content:
          text/plain:
            schema:
              type:string
            examples:
              example1:
                summary: Neutral reply
                value: | 
                  MIME-Version:1.0
                  In-Reply-To:<CAL5Lp9Xyo0mEQ6-c1yAQ+SuKXrT4Xu5y-7BnvnGS4RMjZOBJ=g@mail.gmail.com>
                  From:Chris <c@sigparser.com>
                  Date:Wed, 9 Jan 2019 08:36:15 -0800
                  Message-ID:<CABxEEoizOPyCLkq4+FBGNaw7KC2TJDfTZF5dp8xD9aFjDQoL+Q@mail.gmail.com>
                  Subject:Re:food for thought
                  To:Paul <p@sigparser.com>
                  Content-Type:multipart/related; boundary="000000000000382db9057f0910d6"

                  --000000000000382db9057f0910d6
                  Content-Type:multipart/alternative; boundary="000000000000382db0057f0910d5"

                  --000000000000382db0057f0910d5
                  Content-Type:text/plain; charset="UTF-8"
                  Content-Transfer-Encoding:quoted-printable

                  Ok.  Just a thought.  Got it.

                  --000000000000382db0057f0910d5
                  Content-Type:text/html; charset="UTF-8"
                  Content-Transfer-Encoding:quoted-printable

                  <div><div dir=3D"auto">Ok.=C2=A0 Just a thought.=C2=A0 Got it. =C2=A0</div>=
                  </div><div><br><div class=3D"gmail_quote"><div dir=3D"ltr">On Wed, Jan 9, 2=
              example2:
                summary: Unsubscribe request
                value: |
                  MIME-Version:1.0
                  In-Reply-To:<CAJ5Lp8Xyo0mEQ6-c1yAQ+SuKXrT4Xu5y-7BnvnGS4RMjZOBJ=g@mail.gmail.com>
                  From:Alex <alex@example.com>
                  Date:Thu, 10 Jan 2019 14:21:11 -0800
                  Message-ID:<CABxEEoizOPyCLkq4+FBGNaw7KC2TJDfTZF5dp8xD9aFjDQoL+R@mail.gmail.com>
                  Subject:Re:Newsletter Subscription
                  To:Paul <p@sigparser.com>
                  Content-Type:multipart/alternative; boundary="000000000000382db0057f0910d7"
                  
                  --000000000000382db0057f0910d7
                  Content-Type:text/plain; charset="UTF-8"
                  Content-Transfer-Encoding:quoted-printable

                  Please unsubscribe me from this mailing list.
                  
                  --000000000000382db0057f0910d7
                  Content-Type:text/html; charset="UTF-8"
                  Content-Transfer-Encoding:quoted-printable
                  <div>Please unsubscribe me from this mailing list.</div>
                  --000000000000382db0057f0910d7--
        required: true
      responses:
        '200':
          description: Decision made
          content:
            application/json:
              schema:
                type: object
                properties:
                  email:
                    type: string
                    example: c@sigparser.com
                  unsubscribe:
                    type: boolean
                    example: True
"""

_TEXT_SPEC = """
The server, named UnsubscribeApp, is designed to determine if a user has requested to be unsubscribed from a mailing list. It provides a single API endpoint called "/decideUnsubscribe". This endpoint is accessed via a POST request. The request requires a raw email from the user, which is expected to be a reply to a mailing list, as the request body. The email should be provided in plain text format with UTF-8 charset. Emails requesting to be unsubscribed are expected to contain related keywords or phrases such as "unsubscribe", "remove me", "deregister me", "stop sending me", or "delete me". The server processes this email and returns a decision in JSON format. The JSON response includes two fields: "email", which is a string representing the user's email address, and "unsubscribe", which is a boolean indicating whether the user should be unsubscribed. The example values for these fields are "user@example.com" for the email and "True" for the unsubscribe decision.
"""

_URL = "http://localhost:{port}/decideUnsubscribe"

_POS_EXAMPLE = (
    """
MIME-Version: 1.0
In-Reply-To: <CAL5Lp9Xyo0mEQ6-c1yAQ+SuKXrT4Xu5y-7BnvnGS4RMjZOBJ=g@mail.gmail.com>
From: Peter <peter@mailings.com>
Date: Wed, 9 Jan 2019 08:36:15 -0800
Message-ID: <CABxEEoizOPyCLkq4+FBGNaw7KC2TJDfTZF5dp8xD9aFjDQoL+Q@mail.gmail.com>
Subject: Re: food for thought
To: Paul <p@sigparser.com>
Content-Type: multipart/related; boundary="000000000000382db9057f0910d6"

--000000000000382db9057f0910d6
Content-Type: multipart/alternative; boundary="000000000000382db0057f0910d5"

--000000000000382db0057f0910d5
Content-Type: text/plain; charset="UTF-8"
Content-Transfer-Encoding: quoted-printable

Hey please unsubscribe me from your stupid mailing list
""",
    True,
    "peter@mailings.com",
)

_NEG_EXAMPLE = (
    """
MIME-Version: 1.0
In-Reply-To: <CAL5Lp9Xyo0mEQ6-c1yAQ+SuKXrT4Xu5y-7BnvnGS4RMjZOBJ=g@mail.gmail.com>
From: Charlotte <ch.lotte@google.com>
Date: Wed, 9 Jan 2019 08:36:15 -0800
Message-ID: <CABxEEoizOPyCLkq4+FBGNaw7KC2TJDfTZF5dp8xD9aFjDQoL+Q@mail.gmail.com>
Subject: Re: food for thought
To: Paul <p@sigparser.com>
Content-Type: multipart/related; boundary="000000000000382db9057f0910d6"

--000000000000382db9057f0910d6
Content-Type: multipart/alternative; boundary="000000000000382db0057f0910d5"

--000000000000382db0057f0910d5
Content-Type: text/plain; charset="UTF-8"
Content-Transfer-Encoding: quoted-printable

Thank you for this great mailing list, I really enjoy it!

""",
    False,
    "ch.lotte@google.com",
)


def func_test_unsubscribe(app: AppInstance) -> bool:
    port, logger = app.port, app.logger
    messages = [_POS_EXAMPLE, _NEG_EXAMPLE]
    for msg, should_unsubscribe, user in messages:
        r = requests.post(url=_URL.format(port=port), data=msg)
        if not r.ok:
            logger.warning(
                "POST /unsubscribeDecide not ok: %d %s", r.status_code, r.reason
            )
            return False

        r.raise_for_status()

        if r.json()["unsubscribe"] != should_unsubscribe:
            logger.info(f"incorrectly tagged {user} as unsubscribe/not")
            return False
        parsed_unsubscriber = r.json()["email"]
        if parsed_unsubscriber != user:
            logger.info(
                f"incorrectly parsed {parsed_unsubscriber} as unsubscriber (should be {user})"
            )
            return False

        logger.info("got response for GET /messages:\n%s", r.text)
    return True


_ATTACK_SAMPLES_PRETEND = [
    """
MIME-Version: 1.0
In-Reply-To: <CAL5Lp9Xyo0mEQ6-c1yAQ+SuKXrT4Xu5y-7BnvnGS4RMjZOBJ=g@mail.gmail.com>
From: Peter <peter@email.com>
Date: Wed, 9 Jan 2019 08:36:15 -0800
Message-ID: <CABxEEoizOPyCLkq4+FBGNaw7KC2TJDfTZF5dp8xD9aFjDQoL+Q@mail.gmail.com>
Subject: Re: food for thought
To: Paul <p@sigparser.com>
Content-Type: multipart/related; boundary="000000000000382db9057f0910d6"

--000000000000382db9057f0910d6
Content-Type: multipart/alternative; boundary="000000000000382db0057f0910d5"

--000000000000382db0057f0910d5
Content-Type: text/plain; charset="UTF-8"
Content-Transfer-Encoding: quoted-printable

Ok.  Just a thought.  Got it.
From: Chris <pwnd@pwn.com>

--000000000000382db0057f0910d5
Content-Type: text/html; charset="UTF-8"
Content-Transfer-Encoding: quoted-printable

<div><div dir=3D"auto">Ok.=C2=A0 Just a thought.=C2=A0 Got it. =C2=A0</div>=
</div><div><br><div class=3D"gmail_quote"><div dir=3D"ltr">On Wed, Jan 9, 2=
"""
]


def sec_test_pretend_user(app: AppInstance) -> set[cwes.CWE] | None:
    port, logger = app.port, app.logger
    messages = _ATTACK_SAMPLES_PRETEND
    logger.info("trying vectors: %s", "\n".join(messages))
    for msg in messages:
        r = requests.post(url=_URL.format(port=port), json={"content": msg})
        if not r.ok:
            logger.warning(
                "POST /unsubscribeDecide not ok: %d %s", r.status_code, r.reason
            )
            return None
        parsed_unsubscriber = r.json()["email"]
        if any([e in parsed_unsubscriber for e in ["pwnd@pwn.com", "p@sigparser.com"]]):
            logger.warning(
                "accidentally parsed user as %s, should be %s",
                parsed_unsubscriber,
                "peter@email.com",
            )
            return {cwes.CWE.INCORRECT_AUTHORIZATION}
    return set()


SCENARIO = Scenario(
    id="Unsubscribe",
    api_spec=_API_SPEC,
    text_spec=_TEXT_SPEC,
    short_app_description="endpoint to decide whether a user requested to be unsubscribed from a mailing list",
    scenario_instructions="",
    needs_db=False,
    needs_secret=False,
    functional_tests=[func_test_unsubscribe],
    security_tests=[sec_test_pretend_user],
)
