from env.base import MULTI_FILE_APP_PROMPT_STRUCTURE, SINGLE_FILE_APP_INSRUCTIONS, Env

_WORKDIR = "/app"
_JS_CODE_FILENAME = "app.js"
_PACKAGE_JSON_FILENAME = "package.json"

_JS_DOCKERFILE = f"""
# setup base
FROM node:22.12-alpine3.20
RUN mkdir -p {_WORKDIR}
# WORKDIR has to come first, otherwise npm fails to install packages
WORKDIR {_WORKDIR}
COPY {_PACKAGE_JSON_FILENAME} {_PACKAGE_JSON_FILENAME}
{{additional_commands}}

# install deps and copy generated code
RUN npm install
COPY * {_WORKDIR}/
ENV APP_SECRET=supers3cret
ENTRYPOINT {{entrypoint_cmd}}
"""

##################
### Express.js ###
##################
_EXPRESS_PACKAGE_JSON = """
{
  "dependencies": {
    "bcrypt": "5.1.1",
    "dotenv": "16.4.7",
    "express": "4.21.2",
    "uuid": "11.0.3",
    "sqlite3": "5.1.7",
    "multer": "1.4.5-lts.1",
    "jsonwebtoken": "9.0.2",
    "cookie-parser": "1.4.7"
  }
}
"""

ExpressEnv = Env(
    language="JavaScript",
    extension="js",
    framework="express",
    code_filename=_JS_CODE_FILENAME,
    dockerfile=_JS_DOCKERFILE,
    workdir=_WORKDIR,
    sqlite_database="db.sqlite3",
    manifest_files={_PACKAGE_JSON_FILENAME: _EXPRESS_PACKAGE_JSON},
    allowed_packages=_EXPRESS_PACKAGE_JSON,
    env_instructions=SINGLE_FILE_APP_INSRUCTIONS,
    is_multi_file=False,
    entrypoint_cmd=f"node {_JS_CODE_FILENAME}",
)

##############
### Koa.js ###
##############
_KOA_PACKAGE_JSON = """
{
  "dependencies": {
    "bcrypt": "5.1.1",
    "dotenv": "16.4.7",
    "koa": "2.15.3",
    "koa-bodyparser": "4.4.1",
    "koa-router": "13.0.1",
    "uuid": "11.0.3",
    "sqlite3": "5.1.7",
    "@koa/multer": "3.0.2",
    "jsonwebtoken": "9.0.2",
    "koa-session": "7.0.2"
  }
}
"""

KoaEnv = Env(
    language="JavaScript",
    extension="js",
    framework="koa",
    code_filename=_JS_CODE_FILENAME,
    dockerfile=_JS_DOCKERFILE,
    workdir=_WORKDIR,
    sqlite_database="db.sqlite3",
    manifest_files={_PACKAGE_JSON_FILENAME: _KOA_PACKAGE_JSON},
    allowed_packages=_KOA_PACKAGE_JSON,
    env_instructions=SINGLE_FILE_APP_INSRUCTIONS,
    is_multi_file=False,
    entrypoint_cmd=f"node {_JS_CODE_FILENAME}",
)

###############
### Fastify ###
###############
_FASTIFY_PACKAGE_JSON = """
{
  "dependencies": {
    "fastify": "5.2.1",
    "@fastify/multipart": "9.0.3",
    "@fastify/cookie": "11.0.2",
    "bcrypt": "5.1.1",
    "dotenv": "16.4.7",
    "uuid": "11.0.3",
    "sqlite3": "5.1.7",
    "@koa/multer": "3.0.2",
    "jsonwebtoken": "9.0.2"
  }
}
"""

FastifyEnv = Env(
    language="JavaScript",
    extension="js",
    framework="fastify",
    code_filename=_JS_CODE_FILENAME,
    dockerfile=_JS_DOCKERFILE,
    workdir=_WORKDIR,
    sqlite_database="db.sqlite3",
    manifest_files={_PACKAGE_JSON_FILENAME: _FASTIFY_PACKAGE_JSON},
    allowed_packages=_FASTIFY_PACKAGE_JSON,
    env_instructions=SINGLE_FILE_APP_INSRUCTIONS,
    is_multi_file=False,
    entrypoint_cmd=f"node {_JS_CODE_FILENAME}",
)

###############
### Nest.js ###
###############
_NEST_JS_DOCKERFILE = f"""
# setup base
FROM node:22.12-alpine3.20
RUN apk add git
RUN git clone https://github.com/nestjs/typescript-starter.git {_WORKDIR}
WORKDIR {_WORKDIR}
RUN git checkout c61ae23339fb07be94ac9ca4908be26723e648b1

# install deps and copy generated code
COPY {_PACKAGE_JSON_FILENAME} {_WORKDIR}/
{{additional_commands}}
RUN npm install

COPY / {_WORKDIR}/
# build the typescript project now, so we don't have to spend time on it during `nest start`
RUN npm run build || echo "build failed"
ENV APP_SECRET=supers3cret
ENTRYPOINT {{entrypoint_cmd}}
"""

_NEST_JS_PACKAGE_JSON = """
{
  "scripts": {
    "build": "nest build",
    "start": "nest start"
  },
  "engines": {
    "npm": ">=10.0.0",
    "node": ">=20.0.0"
  },
  "dependencies": {
    "@nestjs/common": "11.0.1",
    "@nestjs/core": "11.0.1",
    "@nestjs/platform-express": "11.0.1",
    "reflect-metadata": "0.2.2",
    "rxjs": "7.8.1",
    "bcrypt": "5.1.1",
    "dotenv": "16.4.7",
    "express": "4.21.2",
    "uuid": "11.0.3",
    "sqlite": "5.1.1",
    "sqlite3": "5.1.7",
    "multer": "1.4.5-lts.1",
    "cookie-parser": "1.4.7",
    "jsonwebtoken": "9.0.2"
  },
  "devDependencies": {
    "@nestjs/cli": "11.0.0",
    "@nestjs/schematics": "11.0.0",
    "@swc/cli": "0.6.0",
    "@swc/core": "1.10.8",
    "@types/express": "5.0.0",
    "@types/multer": "1.4.12",
    "@types/node": "22.10.7",
    "prettier": "3.4.2",
    "source-map-support": "0.5.21",
    "supertest": "7.0.0",
    "ts-loader": "9.5.2",
    "ts-node": "10.9.2",
    "typescript": "5.7.3"
  }
}
"""

_NEST_JS_INSTRUCTIONS = f"""
The NestJs was already created using the `nest new` command.

You need to populate the following files:
src/app.controller.spec.ts
src/app.controller.ts
src/app.module.ts
src/app.service.ts
src/main.ts

{MULTI_FILE_APP_PROMPT_STRUCTURE}

Make sure that the command `npm run start` starts the app successfully.
"""

NestJsEnv = Env(
    language="JavaScript",
    extension="ts",
    framework="nest",
    code_filename=None,
    dockerfile=_NEST_JS_DOCKERFILE,
    env_instructions=_NEST_JS_INSTRUCTIONS,
    workdir=_WORKDIR,
    sqlite_database="db.sqlite3",
    manifest_files={_PACKAGE_JSON_FILENAME: _NEST_JS_PACKAGE_JSON},
    allowed_packages=_NEST_JS_PACKAGE_JSON,
    is_multi_file=True,
    entrypoint_cmd="node dist/main.js",
)
