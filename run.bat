@echo off
setlocal
cd /d "%~dp0"
.venv\Scripts\python.exe run.py %*
endlocal