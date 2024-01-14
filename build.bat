@echo off
cd /D "%~dp0"
python -m build
timeout -t 4