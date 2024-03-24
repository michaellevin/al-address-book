#!/bin/bash
cd "$(dirname "$BASH_SOURCE")" || exit
sphinx-apidoc -o docs/source address_app
cd docs || exit
make clean
make html
xdg-open _build/html/index.html