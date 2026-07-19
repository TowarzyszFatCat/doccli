@echo off
color 0B
echo ====================================================
echo          Rozpoczynam instalacje Doccli...          
echo ====================================================
echo.

:: SPRAWDZANIE PYTHONA
echo [0/6] Sprawdzanie obecnosci Pythona w systemie...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0E
    echo [!] Nie wykryto Pythona (lub nie jest w systemowym PATH).
    echo [i] Rozpoczynam automatyczna instalacje Pythona 3.12...
    winget install --id Python.Python.3.12 --exact --accept-source-agreements --accept-package-agreements
    echo.
    color 0C
    echo ====================================================
    echo  [!] UWAGA: Python zostal wlasnie zainstalowany!
    echo  [!] Aby instalator zadzialal poprawnie, musisz
    echo      zamknac to okno i uruchomic install.bat PONOWNIE.
    echo ====================================================
    pause
    exit
)

set "ORIG_DIR=%~dp0"
set "TARGET_DIR=%LOCALAPPDATA%\Doccli"

echo [1/6] Kopiowanie plikow aplikacji do systemu...
xcopy /E /I /Y "%ORIG_DIR%*" "%TARGET_DIR%\" >nul
cd /d "%TARGET_DIR%"
echo.

echo [2/6] Generowanie pliku startowego (run.bat)...
:: Tworzy plik run.bat bezpośrednio w folderze docelowym.
(
echo @echo off
echo cd /d "%%~dp0"
echo .venv\Scripts\python.exe run.py
) > run.bat
echo.

echo [3/6] Sprawdzam i instaluje narzedzia (mpv, yt-dlp)...
winget install --id yt-dlp.yt-dlp --accept-source-agreements --accept-package-agreements
winget install --id mpv.mpv --accept-source-agreements --accept-package-agreements
echo.

echo [4/6] Konfiguruje srodowisko wirtualne Pythona...
python -m venv .venv
echo.

echo [5/6] Instaluje wymagane biblioteki...
.venv\Scripts\pip install requests inquirerpy termcolor climage pillow
.venv\Scripts\pip install https://github.com/qwertyquerty/pypresence/archive/master.zip
echo.

echo [6/6] Tworze skroty z ikona na Pulpicie i w Menu Start...
powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%USERPROFILE%\Desktop\Doccli.lnk');$s.TargetPath='%TARGET_DIR%\run.bat';$s.WorkingDirectory='%TARGET_DIR%';$s.IconLocation='%TARGET_DIR%\icon.ico';$s.Save()"
powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%APPDATA%\Microsoft\Windows\Start Menu\Programs\Doccli.lnk');$s.TargetPath='%TARGET_DIR%\run.bat';$s.WorkingDirectory='%TARGET_DIR%';$s.IconLocation='%TARGET_DIR%\icon.ico';$s.Save()"
echo.

color 0A
echo ====================================================
echo  [+] Instalacja zakonczona sukcesem!
echo  [i] Aplikacja Doccli zostala w pelni zainstalowana.
echo  [!] Za chwile to okno sie zamknie, a ten folder 
echo      instalacyjny usunie sie automatycznie.
echo ====================================================
pause

:: samoznisczenie xD
start /b "" cmd /c "ping localhost -n 2 >nul & rmdir /s /q ""%ORIG_DIR%"""
exit