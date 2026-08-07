#define MyAppVersion "2.40.0"

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
SolidCompression=yes
; Instalator modyfikuje zmienne środowiskowe
ChangesEnvironment=yes 
WizardSmallImageFile=icon_1.png

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"; LicenseFile: "eula_en.txt"
Name: "polish"; MessagesFile: "compiler:Languages\Polish.isl"; LicenseFile: "eula_pl.txt"

[CustomMessages]
en.TaskDesktop=Create a desktop shortcut
en.TaskStartMenu=Create a Start Menu shortcut
en.GroupShortcuts=Shortcuts:
en.TaskAutostart=Run Doccli automatically after installation
en.GroupOther=Other options:
en.RunDoccli=Launch Doccli
en.StatusPython=Installing Python 3.12 (in background)...
en.StatusYtDlp=Installing yt-dlp tool...
en.StatusMpv=Installing MPV player...
en.StatusChafa=Installing Chafa...
en.StatusEnv=Configuring Python environment and downloading libraries...
en.UninstallPrompt=Do you also want to remove configuration files and watch history (AppData folder)?

pl.TaskDesktop=Utwórz skrót na pulpicie
pl.TaskStartMenu=Utwórz skrót w Menu Start
pl.GroupShortcuts=Skróty:
pl.TaskAutostart=Uruchom Doccli automatycznie po zakończeniu instalacji
pl.GroupOther=Inne opcje:
pl.RunDoccli=Uruchom Doccli
pl.StatusPython=Instalowanie Pythona 3.12 (w tle)...
pl.StatusYtDlp=Instalowanie narzędzia yt-dlp...
pl.StatusMpv=Instalowanie odtwarzacza MPV...
pl.StatusChafa=Instalowanie Chafa...
pl.StatusEnv=Konfigurowanie środowiska Python i pobieranie bibliotek...
pl.UninstallPrompt=Czy chcesz usunąć również pliki konfiguracji i historię programu (folder AppData)?

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
Filename: "{app}\run.bat"; Description: "{cm:RunDoccli}"; Flags: postinstall shellexec; Tasks: autostart

[Tasks]
Name: "desktopicon"; Description: "{cm:TaskDesktop}"; GroupDescription: "{cm:GroupShortcuts}"
Name: "startmenuicon"; Description: "{cm:TaskStartMenu}"; GroupDescription: "{cm:GroupShortcuts}"
Name: "autostart"; Description: "{cm:TaskAutostart}"; GroupDescription: "{cm:GroupOther}"

[Code]
function SetEnvironmentVariable(lpName: string; lpValue: string): BOOL;
  external 'SetEnvironmentVariableW@kernel32.dll stdcall';

function ExpandEnvironmentStrings(lpSrc: string; lpDst: string; nSize: DWORD): DWORD;
  external 'ExpandEnvironmentStringsW@kernel32.dll stdcall';

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

function ExpandEnvVars(const Input: string): string;
var
  Buf: string;
  ReqSize: DWORD;
begin
  if Input = '' then
  begin
    Result := '';
    Exit;
  end;
  
  ReqSize := ExpandEnvironmentStrings(Input, '', 0);
  if ReqSize > 0 then
  begin
    SetLength(Buf, ReqSize);
    ExpandEnvironmentStrings(Input, Buf, ReqSize);
    Result := Copy(Buf, 1, ReqSize - 1);
  end
  else
    Result := Input;
end;

procedure RefreshEnvironment;
var
  SysPath: string;
  UserPath: string;
  NewPath: string;
begin
  if not RegQueryStringValue(HKEY_LOCAL_MACHINE, 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 'Path', SysPath) then SysPath := '';
  if not RegQueryStringValue(HKEY_CURRENT_USER, 'Environment', 'Path', UserPath) then UserPath := '';

  SysPath := ExpandEnvVars(SysPath);
  UserPath := ExpandEnvVars(UserPath);

  NewPath := SysPath;
  if (NewPath <> '') and (UserPath <> '') and (NewPath[Length(NewPath)] <> ';') then
    NewPath := NewPath + ';';
  NewPath := NewPath + UserPath;

  SetEnvironmentVariable('PATH', NewPath);
end;

procedure CreateSettingsJSON;
var
  SettingsDir, SettingsFile, JsonContent: string;
begin
  SettingsDir := ExpandConstant('{userappdata}\doccli');
  SettingsFile := SettingsDir + '\settings.json';
  
  ForceDirectories(SettingsDir);
  
  if not FileExists(SettingsFile) then
  begin
    if ActiveLanguage = 'english' then
      JsonContent := '{'#13#10'    "language": "en"'#13#10'}'
    else
      JsonContent := '{'#13#10'    "language": "pl"'#13#10'}';
      
    SaveStringToFile(SettingsFile, JsonContent, False);
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  ResultCode: Integer;
begin
  if CurStep = ssPostInstall then
  begin
    WizardForm.ProgressGauge.Max := 5;
    
    if CheckWinget then
    begin
      WizardForm.StatusLabel.Caption := CustomMessage('StatusPython');
      WizardForm.ProgressGauge.Position := 1;
      Exec('winget', 'install --id Python.Python.3.12 --exact --silent --accept-source-agreements --accept-package-agreements --override "/quiet PrependPath=1 Include_test=0"', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);

      WizardForm.StatusLabel.Caption := CustomMessage('StatusYtDlp');
      WizardForm.ProgressGauge.Position := 2;
      Exec('winget', 'install --id yt-dlp.yt-dlp --silent --accept-source-agreements --accept-package-agreements', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);

      WizardForm.StatusLabel.Caption := CustomMessage('StatusMpv');
      WizardForm.ProgressGauge.Position := 3;
      Exec('winget', 'install --id 9P3JFR0CLLL6 --silent --accept-source-agreements --accept-package-agreements', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);

      WizardForm.StatusLabel.Caption := CustomMessage('StatusChafa');
      WizardForm.ProgressGauge.Position := 4;
      Exec('winget', 'install --id hpjansson.Chafa --silent --accept-source-agreements --accept-package-agreements', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
    end
    else
    begin
      WizardForm.ProgressGauge.Position := 4;
    end;

    CreateSettingsJSON;
    RefreshEnvironment;

    WizardForm.StatusLabel.Caption := CustomMessage('StatusEnv');
    WizardForm.ProgressGauge.Position := 5;
    Exec(ExpandConstant('{app}\setup_env.bat'), '', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usPostUninstall then
  begin
    if SuppressibleMsgBox(CustomMessage('UninstallPrompt'), mbConfirmation, MB_YESNO or MB_DEFBUTTON2, IDNO) = IDYES then
    begin
      DelTree(ExpandConstant('{userappdata}\doccli'), True, True, True);
    end;
  end;
end;

