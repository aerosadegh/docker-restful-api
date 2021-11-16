#!/usr/bin/env bash

set -e
set -x

find . -type f \( ! -iname "__version__.py" \) -not -path "./venv*/*"  -name "*.py" | xargs pylint
isort --multi-line=3 --trailing-comma --force-grid-wrap=0 --combine-as --check-only --df .
