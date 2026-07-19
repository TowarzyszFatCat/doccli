@echo off
color 0C
echo ====================================================
echo             Odinstalowywanie Doccli...          
echo ====================================================
echo.

:: Ostrzeżenie i prośba o potwierdzenie
echo Czy na pewno chcesz usunac Doccli z tego komputera?
pause
echo.

:: Definiujemy ścieżkę, w której zainstalowany jest program
set "TARGET_DIR=%LOCALAPPDATA%\Doccli"

echo [1/3] Usuwanie skrotu z Pulpitu...
if exist "%USERPROFILE%\Desktop\Doccli.lnk" (
    del /Q "%USERPROFILE%\Desktop\Doccli.lnk"
)

echo [2/3] Usuwanie skrotu z Menu Start...
if exist "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Doccli.lnk" (
    del /Q "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Doccli.lnk"
)

echo [3/3] Usuwanie folderu systemowego aplikacji...
:: Upewniamy się, że terminal nie jest "wewnątrz" folderu, bo zablokuje to jego usunięcie
cd /d "%~dp0"
if exist "%TARGET_DIR%" (
    rmdir /S /Q "%TARGET_DIR%"
)
echo.

color 0A
echo ====================================================
echo  [-] Doccli zostalo pomyslnie usuniete z systemu.
echo  [i] Uwaga: mpv oraz yt-dlp nie zostaly usuniete, 
echo      poniewaz moga byc uzywane przez inne programy.
echo ====================================================
pause