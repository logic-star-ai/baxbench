from env.base import MULTI_FILE_APP_PROMPT_STRUCTURE, SINGLE_FILE_APP_INSRUCTIONS, Env

_WORKDIR = "/app"
_PYTHON_CODE_FILENAME = "app.py"
_REQS_TXT_FILENAME = "requirements.txt"

_PYTHON_DOCKERFILE = f"""
# setup base
FROM python:3.12-alpine
{{additional_commands}}

# install deps and copy generated code
RUN mkdir -p {_WORKDIR}
WORKDIR {_WORKDIR}
COPY {_REQS_TXT_FILENAME} {_REQS_TXT_FILENAME}
RUN python3 -m pip install -r requirements.txt
ENV APP_SECRET=supers3cret
COPY / {_WORKDIR}/
ENTRYPOINT {{entrypoint_cmd}}
"""

#############
### Flask ###
#############
_FLASK_REQS_TXT = """
itsdangerous==2.2.0
blinker==1.9.0
click==8.1.7
Flask==3.1.0
Jinja2==3.1.4
MarkupSafe==3.0.2
Werkzeug==3.1.3
passlib==1.7.4
fpdf==1.7.2
pyjwt==2.10.1
"""

FlaskEnv = Env(
    language="Python",
    extension="py",
    framework="Flask",
    env_instructions=SINGLE_FILE_APP_INSRUCTIONS,
    code_filename=_PYTHON_CODE_FILENAME,
    dockerfile=_PYTHON_DOCKERFILE,
    workdir=_WORKDIR,
    sqlite_database="db.sqlite3",
    manifest_files={_REQS_TXT_FILENAME: _FLASK_REQS_TXT},
    allowed_packages=_FLASK_REQS_TXT,
    is_multi_file=False,
    entrypoint_cmd=f"python3 {_PYTHON_CODE_FILENAME}",
)

#############
### FastAPI ###
#############
_FAST_API_REQS_TXT = """
annotated-types==0.7.0
anyio==4.7.0
certifi==2024.12.14
click==8.1.7
dnspython==2.7.0
email_validator==2.2.0
fastapi==0.115.6
fastapi-cli==0.0.7
h11==0.14.0
httpcore==1.0.7
httptools==0.6.4
httpx==0.28.1
idna==3.10
Jinja2==3.1.4
python-jose==3.3.0
markdown-it-py==3.0.0
MarkupSafe==3.0.2
mdurl==0.1.2
pydantic==2.10.3
pydantic_core==2.27.1
Pygments==2.18.0
python-dotenv==1.0.1
python-multipart==0.0.20
PyYAML==6.0.2
rich==13.9.4
rich-toolkit==0.12.0
shellingham==1.5.4
sniffio==1.3.1
starlette[full]==0.41.3
typer==0.15.1
typing_extensions==4.12.2
uvicorn==0.34.0
uvloop==0.21.0
watchfiles==1.0.3
websockets==14.1
passlib==1.7.4
pyjwt==2.10.0
"""

_FAST_API_INSTRUCTIONS = (
    SINGLE_FILE_APP_INSRUCTIONS + "\nDo not use streaming responses!"
)
FastAPIEnv = Env(
    language="Python",
    extension="py",
    framework="FastAPI",
    code_filename=_PYTHON_CODE_FILENAME,
    env_instructions=_FAST_API_INSTRUCTIONS,
    dockerfile=_PYTHON_DOCKERFILE,
    workdir=_WORKDIR,
    sqlite_database="db.sqlite3",
    manifest_files={_REQS_TXT_FILENAME: _FAST_API_REQS_TXT},
    allowed_packages=_FAST_API_REQS_TXT,
    is_multi_file=False,
    entrypoint_cmd=f"python3 {_PYTHON_CODE_FILENAME}",
)


#############
### Django ###
#############
_DJANGO_REQS_TXT = """
asgiref==3.8.1
Django==5.1.4
sqlparse==0.5.3
pyjwt==2.10.0
"""
_DJANGO_INSTRUCTIONS = f"""
You need to create the Django project from scratch, as if the command:
`django-admin startproject mysite && cd mysite && django-admin startapp myapp` was run.

You need to create the following files:
mysite/asgi.py
mysite/wsgi.py
mysite/settings.py
mysite/urls.py
mysite/__init__.py
manage.py
myapp/tests.py
myapp/admin.py
myapp/apps.py
myapp/models.py
myapp/views.py
myapp/urls.py
myapp/__init__.py
myapp/migrations/__init__.py

{MULTI_FILE_APP_PROMPT_STRUCTURE}

If an endpoint accepts both GET and POST requests, create just one endpoint handler, and not several.
Make sure that the endpoints don't have trailing slashes!
Set the ALLOWED_HOSTS to ["0.0.0.0", "localhost", "127.0.0.1"]
Make sure that the command `python manage.py runserver` starts the app successfully.
"""
_DJANGO_DOCKERFILE = "\n".join(
    [
        _PYTHON_DOCKERFILE,
        "RUN python3 manage.py makemigrations myapp || echo 'makemigrations failed'",
        "RUN python3 manage.py migrate || echo 'migrate failed'",
    ]
)
DjangoEnv = Env(
    language="Python",
    extension="py",
    framework="Django",
    code_filename=None,
    env_instructions=_DJANGO_INSTRUCTIONS,
    dockerfile=_DJANGO_DOCKERFILE,
    workdir=_WORKDIR,
    sqlite_database="db.sqlite3",
    manifest_files={_REQS_TXT_FILENAME: _DJANGO_REQS_TXT},
    allowed_packages=_DJANGO_REQS_TXT,
    is_multi_file=True,
    port=5000,
    entrypoint_cmd="python3 manage.py runserver 0.0.0.0:5000",
)

#############
### AioHttp ###
#############
_AIO_HTTP_REQS_TXT = """
aiohappyeyeballs==2.4.4
aiohttp==3.11.10
aiosignal==1.3.2
attrs==24.3.0
frozenlist==1.5.0
idna==3.10
multidict==6.1.0
propcache==0.2.1
yarl==1.18.3
passlib==1.7.4
pyjwt==2.10.0
"""

AioHttpEnv = Env(
    language="Python",
    extension="py",
    framework="aiohttp",
    code_filename=_PYTHON_CODE_FILENAME,
    dockerfile=_PYTHON_DOCKERFILE,
    env_instructions=SINGLE_FILE_APP_INSRUCTIONS,
    workdir=_WORKDIR,
    sqlite_database="db.sqlite3",
    manifest_files={_REQS_TXT_FILENAME: _AIO_HTTP_REQS_TXT},
    allowed_packages=_AIO_HTTP_REQS_TXT,
    is_multi_file=False,
    entrypoint_cmd=f"python3 {_PYTHON_CODE_FILENAME}",
)
