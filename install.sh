#!/usr/bin/env bash

# download & install poetry
curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

# pyenv command
pyenv install 3.8.1
pyenv local 3.8.1

# local poetry config command
poetry config --local virtualenvs.in-project true

# install packages accordingly to pyproject.toml
poetry install
