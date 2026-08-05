@echo off
chcp 65001 >nul
color 0B
cd /d "%~dp0"

echo ====================================================
echo      Konfiguracja srodowiska i pakietow Pythona...   
echo ====================================================
echo/

echo [1/2] Tworzenie wirtualnego srodowiska (.venv)...
"%LOCALAPPDATA%\Programs\Python\Python312\python.exe" -m venv .venv 2>nul || python -m venv .venv

echo/
echo [2/2] Pobieranie wymaganych pakietow pip...
.venv\Scripts\pip install requests inquirerpy termcolor climage pillow deep-translator rich curl-cffi >nul 2>&1
.venv\Scripts\pip install https://github.com/qwertyquerty/pypresence/archive/master.zip >nul 2>&1

color 0A
echo/
echo ====================================================
echo  [+] Wszystko gotowe! Konfiguracja zakonczona.
echo ====================================================
timeout /t 1 /nobreak >nul