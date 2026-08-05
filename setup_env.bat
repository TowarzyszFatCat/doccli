@echo off
chcp 65001 >nul
color 0B
cd /d "%~dp0"

echo ====================================================
echo        Pobieranie srodowiska i zaleznosci...         
echo ====================================================
echo/

echo [1/4] Sprawdzanie Pythona...
python --version >nul 2>&1
if %errorlevel% equ 0 goto :python_installed

color 0E
echo [!] Nie wykryto Pythona.
echo [i] Pobieram i instaluje Python 3.12 (to moze chwile potrwac)...
winget install --id Python.Python.3.12 --exact --silent --accept-source-agreements --accept-package-agreements

:python_installed
color 0B
echo/
echo [2/4] Pobieranie zewnetrznych narzedzi wideo...
winget install --id yt-dlp.yt-dlp --silent --accept-source-agreements --accept-package-agreements
winget install --id 9P3JFR0CLLL6 --silent --accept-source-agreements --accept-package-agreements
winget install --id hpjansson.Chafa --silent --accept-source-agreements --accept-package-agreements

echo/
echo [3/4] Konfiguracja wirtualnego srodowiska Pythona...
:: Uzywamy 'py', poniewaz swiezo zainstalowany Python mogl jeszcze nie odswiezyc sie w PATH obecnej konsoli
py -m venv .venv 2>nul || python -m venv .venv

echo/
echo [4/4] Pobieranie pakietow pip...
.venv\Scripts\pip install requests inquirerpy termcolor climage pillow deep-translator rich curl-cffi >nul 2>&1
.venv\Scripts\pip install https://github.com/qwertyquerty/pypresence/archive/master.zip >nul 2>&1

color 0A
echo/
echo ====================================================
echo  [+] Konfiguracja srodowiska zakonczona!
echo ====================================================
timeout /t 3 /nobreak >nul