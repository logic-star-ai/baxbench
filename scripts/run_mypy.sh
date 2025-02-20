#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/.."
pipenv run mypy .

