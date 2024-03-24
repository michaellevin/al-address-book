@echo off
cd /d %~dp0
call sphinx-apidoc -o docs/source address_app
cd docs
call make clean
call make html
start "" "%cd%\_build\html\index.html"