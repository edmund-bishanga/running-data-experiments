#!/bin/bash

# run this in script dir: repo root dir
cd "$(dirname "$0")"

# find which .py files have changed, lint them, output feedback
git diff --name-only | grep -iE '\.py' | xargs python -m pylint --rcfile=.pylintrc
