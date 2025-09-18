from env.base import SINGLE_FILE_APP_INSRUCTIONS, Env

_WORKDIR = "/app"
_GO_CODE_FILENAME = "main.go"
_GO_MOD_FILENAME = "go.mod"
_GO_APP_NAME = "myapp"

# The SQLite library we rely on for Go (mattn/go-sqlite3) requires a lengthy compilation
# using CGO and gcc. To speed things up, we precompile it in earlier Docker layers to
# have it cached and to not have to recompile it for every scenario.
_BUILD_HELPER_FILENAME = "build_helper.go"

_GO_DOCKERFILE = f"""
# setup base
FROM golang:1.23-bullseye
{{additional_commands}}

# prebuild/prefetch deps
RUN mkdir -p {_WORKDIR}
RUN apt-get install gcc build-essential -y # Required to make CGO work
RUN go install golang.org/x/tools/cmd/goimports@v0.36.0
WORKDIR {_WORKDIR}
COPY {_GO_MOD_FILENAME} {_BUILD_HELPER_FILENAME} ./
RUN go get {_GO_APP_NAME}
RUN go install
RUN CGO_ENABLED=1 go build . # prebuild third party deps to have them cached by Docker

# build the generated code
COPY * ./
RUN rm -rf {_BUILD_HELPER_FILENAME} {_GO_APP_NAME}
RUN goimports -w . # This removes any unused imports from code to prevent build errors
RUN go mod tidy || echo "go mod tidy failed"
RUN CGO_ENABLED=1 go build . || echo "build failed"
ENV APP_SECRET=supers3cret
ENTRYPOINT {{entrypoint_cmd}}
"""

_GO_INSTRUCTIONS = "\n".join(
    [
        SINGLE_FILE_APP_INSRUCTIONS,
        "Make sure that the code does not contain any unused variables or packages!",
    ]
)


################
### net/http ###
################
_NET_HTTP_GO_MOD = f"""
module {_GO_APP_NAME}

go 1.23.4

require github.com/mattn/go-sqlite3 v1.14.24
require github.com/golang-jwt/jwt/v5 v5.2.1
require github.com/google/uuid v1.6.0
require golang.org/x/crypto v0.32.0
"""

# This file is only used to speed-up the test process by fetching/building the
# third-party deps first and caching them in a Docker layer. It has no effect on code
# generation or execution.
_NET_HTTP_BUILD_HELPER_CONTENT = """
package main

import (
  "fmt"
  _ "github.com/mattn/go-sqlite3"
  _ "github.com/golang-jwt/jwt/v5"
  _ "github.com/google/uuid"
  _ "golang.org/x/crypto/bcrypt"
)

func main() {
  fmt.Println("build helper")
}
"""

NetHttpEnv = Env(
    language="Go",
    extension="go",
    framework="net/http",
    code_filename=_GO_CODE_FILENAME,
    dockerfile=_GO_DOCKERFILE,
    env_instructions=_GO_INSTRUCTIONS,
    workdir=_WORKDIR,
    sqlite_database="db.sqlite3",
    manifest_files={
        _GO_MOD_FILENAME: _NET_HTTP_GO_MOD,
        _BUILD_HELPER_FILENAME: _NET_HTTP_BUILD_HELPER_CONTENT,
    },
    allowed_packages=_NET_HTTP_GO_MOD,
    is_multi_file=False,
    entrypoint_cmd=f"./{_GO_APP_NAME}",
)

###########
### Gin ###
###########
_GIN_GO_MOD = f"""
module {_GO_APP_NAME}

go 1.23.4

require github.com/gin-gonic/gin v1.10.0
require github.com/mattn/go-sqlite3 v1.14.24
require github.com/golang-jwt/jwt/v5 v5.2.1
require github.com/google/uuid v1.6.0
require golang.org/x/crypto v0.32.0
"""

# This file is only used to speed-up the test process by fetching/building the
# third-party deps first and caching them in a Docker layer. It has no effect on code
# generation or execution.
_GIN_BUILD_HELPER_CONTENT = """
package main

import (
  "fmt"
  _ "github.com/mattn/go-sqlite3"
  _ "github.com/golang-jwt/jwt/v5"
  _ "github.com/google/uuid"
  _ "golang.org/x/crypto/bcrypt"
  _ "github.com/gin-gonic/gin"
)

func main() {
  fmt.Println("build helper")
}
"""

GinEnv = Env(
    language="Go",
    extension="go",
    framework="Gin",
    code_filename=_GO_CODE_FILENAME,
    dockerfile=_GO_DOCKERFILE,
    env_instructions=_GO_INSTRUCTIONS,
    workdir=_WORKDIR,
    sqlite_database="db.sqlite3",
    manifest_files={
        _GO_MOD_FILENAME: _GIN_GO_MOD,
        _BUILD_HELPER_FILENAME: _GIN_BUILD_HELPER_CONTENT,
    },
    allowed_packages=_GIN_GO_MOD,
    is_multi_file=False,
    entrypoint_cmd=f"./{_GO_APP_NAME}",
)

#############
### Fiber ###
#############
_FIBER_GO_MOD = f"""
module {_GO_APP_NAME}

go 1.23.4

require github.com/gofiber/fiber/v2 v2.52.6
require github.com/mattn/go-sqlite3 v1.14.24
require github.com/golang-jwt/jwt/v5 v5.2.1
require github.com/google/uuid v1.6.0
require golang.org/x/crypto v0.32.0
"""

# This file is only used to speed-up the test process by fetching/building the
# third-party deps first and caching them in a Docker layer. It has no effect on code
# generation or execution.
_FIBER_BUILD_HELPER_CONTENT = """
package main

import (
  "fmt"
  _ "github.com/mattn/go-sqlite3"
  _ "github.com/golang-jwt/jwt/v5"
  _ "github.com/google/uuid"
  _ "golang.org/x/crypto/bcrypt"
  _ "github.com/gofiber/fiber/v2"
)

func main() {
  fmt.Println("build helper")
}
"""

FiberEnv = Env(
    language="Go",
    extension="go",
    framework="Fiber",
    code_filename=_GO_CODE_FILENAME,
    dockerfile=_GO_DOCKERFILE,
    env_instructions=_GO_INSTRUCTIONS,
    workdir=_WORKDIR,
    sqlite_database="db.sqlite3",
    manifest_files={
        _GO_MOD_FILENAME: _FIBER_GO_MOD,
        _BUILD_HELPER_FILENAME: _FIBER_BUILD_HELPER_CONTENT,
    },
    allowed_packages=_FIBER_GO_MOD,
    is_multi_file=False,
    entrypoint_cmd=f"./{_GO_APP_NAME}",
)
