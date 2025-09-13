from env.base import SINGLE_FILE_APP_INSRUCTIONS, Env

_WORKDIR = "/app"
_SRC_FILENAME = "main.rs"
_CARGO_TOML = "Cargo.toml"

_EMPTY_BRACKETS = "{{ App::new(); }}"
_RUST_DOCKERFILE = f"""
#setup base
FROM rust:1.83.0-alpine3.20
{{additional_commands}}

# prebuild/prefetch deps
RUN apk add imagemagick musl-dev sqlite-dev build-base git
RUN mkdir -p {_WORKDIR} {_WORKDIR}/src
WORKDIR {_WORKDIR}
COPY {_CARGO_TOML} {_CARGO_TOML}
ENV RUST_BACKTRACE=1
RUN mkdir -p {_WORKDIR}/src
RUN echo "use actix_web::App; fn main() {_EMPTY_BRACKETS}" > src/{_SRC_FILENAME}
RUN cargo build || echo "Build failed"

# build the generated code
COPY {_SRC_FILENAME} src/{_SRC_FILENAME}
RUN sed -i '1i#![allow(warnings, unused)]' src/{_SRC_FILENAME}
ENV APP_SECRET=supers3cret
RUN cargo build || echo "Build failed"
ENTRYPOINT {{entrypoint_cmd}}
"""

_CARGO_ACTIX = """
[package]
name = "server"
version = "0.1.0"
edition = "2021"

[dependencies]
actix-web = { version = "4.9.0" }
actix-multipart = { version = "0.7.2" }
clap = { version = "4", features = ["derive"] }
tempdir = "0.3"
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
tokio = { version = "1", features = ["full","macros", "rt-multi-thread"] }
current_platform = "*"
chrono = "*"
nix = { version = "0.29.0", features = ["signal"]}
rusqlite = { version = "0.33.0", features = ["bundled", "modern-full"] }
env_logger = "0.11.6"
uuid = { version = "1.11.0", features = ["v4", "fast-rng", "macro-diagnostics"] }
"""

RustActixEnv = Env(
    language="Rust",
    extension="rs",
    framework="Actix",
    env_instructions=SINGLE_FILE_APP_INSRUCTIONS,
    code_filename=_SRC_FILENAME,
    dockerfile=_RUST_DOCKERFILE,
    workdir=_WORKDIR,
    sqlite_database="db.sqlite3",
    manifest_files={_CARGO_TOML: _CARGO_ACTIX},
    allowed_packages=_CARGO_ACTIX,
    is_multi_file=False,
    entrypoint_cmd="cargo run",
)
