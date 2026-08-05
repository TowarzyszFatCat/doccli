#define MyAppVersion "2.33"

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

[Files]
; Pakuje pliki i foldery
Source: "*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "*.iss"

[Icons]
; Skróty na pulpicie i w menu start
Name: "{autodesktop}\Doccli"; Filename: "{app}\run.bat"; IconFilename: "{app}\icon.ico"
Name: "{userprograms}\Doccli"; Filename: "{app}\run.bat"; IconFilename: "{app}\icon.ico"

[Registry]
; Dodawanie doccli do zmiennej środowiskowej PATH użytkownika
Root: HKCU; Subkey: "Environment"; ValueType: expandsz; ValueName: "Path"; ValueData: "{olddata};{app}"; Check: NeedsAddPath(ExpandConstant('{app}'))

[Run]
; Uruchamia skrypt aby doinstalować Pythona i moduły
Filename: "{app}\setup_env.bat"; Description: "Pobierz pakiety i skonfiguruj srodowisko (Wymagane)"; Flags: postinstall runascurrentuser waituntilterminated

[Code]
// Sprawdzenie path
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