#define MyAppVersion "2.33.1"

[Setup]
; Info
AppName=Doccli
AppVersion={#MyAppVersion}
AppPublisher=TFC
DefaultDirName={localappdata}\Doccli
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
OutputBaseFilename=InstallDoccli_v{#MyAppVersion}
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\icon.ico
Compression=lzma2
LicenseFile=eula.txt
SolidCompression=yes
; Instalator modyfikuje zmienne środowiskowe
ChangesEnvironment=yes 
WizardSmallImageFile=icon_1.png

[Languages]
Name: "polish"; MessagesFile: "compiler:Languages\Polish.isl"

[Files]
; Pakuje pliki i foldery
Source: "*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "*.iss"

[Icons]
Name: "{autodesktop}\Doccli"; Filename: "{app}\run.bat"; IconFilename: "{app}\icon.ico"; Tasks: desktopicon
Name: "{userprograms}\Doccli"; Filename: "{app}\run.bat"; IconFilename: "{app}\icon.ico"; Tasks: startmenuicon

[Registry]
; Dodawanie doccli do zmiennej środowiskowej PATH użytkownika
Root: HKCU; Subkey: "Environment"; ValueType: expandsz; ValueName: "Path"; ValueData: "{olddata};{app}"; Check: NeedsAddPath(ExpandConstant('{app}'))

[Run]
Filename: "{app}\run.bat"; Description: "Uruchom Doccli"; Flags: postinstall shellexec; Tasks: autostart

[Tasks]
Name: "desktopicon"; Description: "Utwórz skrót na pulpicie"; GroupDescription: "Skróty:"
Name: "startmenuicon"; Description: "Utwórz skrót w Menu Start"; GroupDescription: "Skróty:"
Name: "autostart"; Description: "Uruchom Doccli automatycznie po zakończeniu instalacji"; GroupDescription: "Inne opcje:"

[Code]
function CheckWinget: boolean;
var
  ResultCode: Integer;
begin
  Result := Exec('cmd.exe', '/c winget --version >nul 2>&1', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) and (ResultCode = 0);
end;

function NeedsAddPath(Param: string): boolean;
var
  OrigPath: string;
begin
  if not RegQueryStringValue(HKEY_CURRENT_USER, 'Environment', 'Path', OrigPath)
  then begin
    Result := True;
    exit;
  end;
  Result := Pos(';' + Param + ';', ';' + OrigPath + ';') = 0;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  ResultCode: Integer;
begin
  if CurStep = ssInstall then
  begin
    WizardForm.ProgressGauge.Max := 5;
    
    if CheckWinget then
    begin
      WizardForm.StatusLabel.Caption := 'Instalowanie Pythona 3.12 (w tle)...';
      WizardForm.ProgressGauge.Position := 1;
      Exec('winget', 'install --id Python.Python.3.12 --exact --silent --accept-source-agreements --accept-package-agreements', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);

      WizardForm.StatusLabel.Caption := 'Instalowanie narzędzia yt-dlp...';
      WizardForm.ProgressGauge.Position := 2;
      Exec('winget', 'install --id yt-dlp.yt-dlp --silent --accept-source-agreements --accept-package-agreements', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);

      WizardForm.StatusLabel.Caption := 'Instalowanie odtwarzacza MPV...';
      WizardForm.ProgressGauge.Position := 3;
      Exec('winget', 'install --id 9P3JFR0CLLL6 --silent --accept-source-agreements --accept-package-agreements', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);

      WizardForm.StatusLabel.Caption := 'Instalowanie Chafa...';
      WizardForm.ProgressGauge.Position := 4;
      Exec('winget', 'install --id hpjansson.Chafa --silent --accept-source-agreements --accept-package-agreements', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
    end
    else
    begin
      WizardForm.ProgressGauge.Position := 4;
    end;

    WizardForm.StatusLabel.Caption := 'Konfigurowanie środowiska Python i pobieranie bibliotek...';
    WizardForm.ProgressGauge.Position := 5;
    Exec(ExpandConstant('{app}\setup_env.bat'), '', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usPostUninstall then
  begin
    if SuppressibleMsgBox('Czy chcesz usunąć również pliki konfiguracji i historię programu (folder AppData)?', mbConfirmation, MB_YESNO, IDNO) = IDYES then
    begin
      // Usuwanie folderu AppData\doccli
      DelTree(ExpandConstant('{userappdata}\doccli'), True, True, True);
    end;
  end;
end;