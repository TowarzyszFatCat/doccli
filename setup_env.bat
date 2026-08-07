@echo off
chcp 65001 >nul
color 0B
cd /d "%~dp0"

echo ====================================================
echo   Configuring environment and Python packages...
echo ====================================================
echo/

echo [1/2] Creating virtual environment (.venv)...
"%LOCALAPPDATA%\Programs\Python\Python312\python.exe" -m venv .venv 2>nul || python -m venv .venv

echo/
echo [2/2] Downloading required pip packages...
.venv\Scripts\pip install requests inquirerpy termcolor climage pillow deep-translator rich curl-cffi >nul 2>&1
.venv\Scripts\pip install https://github.com/qwertyquerty/pypresence/archive/master.zip >nul 2>&1

color 0A
echo/
echo ====================================================
echo  [+] All done! Configuration completed.
echo ====================================================
timeout /t 1 /nobreak >nul