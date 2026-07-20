@echo off
chcp 65001 >nul
color 0B

echo ====================================================
echo        Rozpoczynam instalacje Doccli...          
echo ====================================================
echo/

:: Winget win 10 masakra
echo [1/9] Sprawdzanie menedzera pakietow winget...
winget --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [!] Nie wykryto narzedzia 'winget' w systemie!
    echo [i] Na Windows 10 musisz zainstalowac/zaktualizowac "Instalator aplikacji" ze sklepu Microsoft.
    echo [i] Za chwile otworzy sie strona sklepu. Kliknij 'Pobierz', a nastepnie uruchom instalator PONOWNIE.
    pause
    start ms-windows-store://pdp/?ProductId=9nblggh4nns1
    exit
)
color 0B

:: python jest?
echo [2/9] Sprawdzanie obecnosci Pythona w systemie...
python --version >nul 2>&1
if %errorlevel% equ 0 goto :python_installed

color 0E
echo [!] Nie wykryto Pythona (lub nie jest w systemowym PATH).
echo [i] Rozpoczynam automatyczna instalacje Pythona 3.12...
winget install --id Python.Python.3.12 --exact --accept-source-agreements --accept-package-agreements
color 0C
echo/
echo ====================================================
echo  [!] UWAGA: Python zostal wlasnie zainstalowany!
echo  [!] Aby system zadzialal poprawnie, musisz
echo      zamknac to okno i uruchomic install.bat PONOWNIE.
echo ====================================================
pause
exit

:python_installed
color 0B
set "ORIG_DIR=%~dp0"
set "ORIG_DIR_CLEAN=%ORIG_DIR:~0,-1%"
set "TARGET_DIR=%LOCALAPPDATA%\Doccli"

echo [3/9] Kopiowanie plikow aplikacji do systemu...
if /I "%ORIG_DIR_CLEAN%"=="%TARGET_DIR%" goto :skip_copy
xcopy /E /I /Y "%ORIG_DIR_CLEAN%\*" "%TARGET_DIR%\" >nul
:skip_copy
cd /d "%TARGET_DIR%"
echo/

echo [4/9] Generowanie pliku startowego (run.bat)...
echo @echo off> run.bat
echo setlocal>> run.bat
echo cd /d "%%~dp0">> run.bat
echo .venv\Scripts\python.exe run.py %%*>> run.bat
echo endlocal>> run.bat
echo/

echo [5/9] Sprawdzam i instaluje narzedzia (mpv, yt-dlp)...
winget install --id yt-dlp.yt-dlp --accept-source-agreements --accept-package-agreements
color 0B

winget install --id 9P3JFR0CLLL6 --accept-source-agreements --accept-package-agreements
color 0B
echo/

winget install --id hpjansson.Chafa --accept-source-agreements --accept-package-agreements
color 0B
echo/

echo [6/9] Konfiguruje srodowisko wirtualne Pythona...
python -m venv .venv
echo/

echo [7/9] Instaluje wymagane biblioteki...
.venv\Scripts\pip install requests inquirerpy termcolor climage pillow deep-translator rich
color 0B
.venv\Scripts\pip install https://github.com/qwertyquerty/pypresence/archive/master.zip
color 0B
echo/

echo [8/9] Dodawanie programu do zmiennej PATH...
echo @echo off> doccli.bat
echo call "%%~dp0run.bat" %%*>> doccli.bat
powershell -NoProfile -ExecutionPolicy Bypass -Command "$path = [Environment]::GetEnvironmentVariable('Path', 'User'); if ($path -notmatch [regex]::Escape('%TARGET_DIR%')) { [Environment]::SetEnvironmentVariable('Path', $path + ';%TARGET_DIR%', 'User') }"
echo/

echo [9/9] Tworze skroty z ikona na Pulpicie i w Menu Start...
powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%USERPROFILE%\Desktop\Doccli.lnk');$s.TargetPath='%TARGET_DIR%\run.bat';$s.WorkingDirectory='%TARGET_DIR%';$s.IconLocation='%TARGET_DIR%\icon.ico';$s.Save()"
powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%APPDATA%\Microsoft\Windows\Start Menu\Programs\Doccli.lnk');$s.TargetPath='%TARGET_DIR%\run.bat';$s.WorkingDirectory='%TARGET_DIR%';$s.IconLocation='%TARGET_DIR%\icon.ico';$s.Save()"
echo/

color 0A
echo ====================================================
echo  [+] Instalacja zakonczona sukcesem!
echo  [i] Aplikacja Doccli zostala w pelni zainstalowana.
echo  [i] Mozesz teraz uruchamiac ja skrotami lub wpisujac
echo      'doccli' w nowym oknie CMD / PowerShell.
echo ====================================================
echo/
echo  [!] Folder instalacyjny usunie sie automatycznie.
echo  [i] Wcisnij ENTER, aby bezpiecznie opuscic instalator...
pause >nul

:: SAMOZNISZCZENIE
cd /d "%USERPROFILE%\Desktop"
start /b "" cmd /c "ping localhost -n 3 >nul & rmdir /s /q "%ORIG_DIR_CLEAN%""
exit