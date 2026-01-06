[Setup]
AppName=Verbum Atlas
AppVersion=2026
AppPublisher=Fernando Ardon & Antigravity
AppPublisherURL=https://google.com
AppSupportURL=https://google.com
AppUpdatesURL=https://google.com
DefaultDirName={autopf}\Verbum Atlas 2026
DisableProgramGroupPage=yes
; El icono del instalador
SetupIconFile=app_icon.ico
OutputDir=C:\Users\frard\OneDrive - stp9\Escritorio
OutputBaseFilename=VerbumAtlas_2026_Final_v3
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\Verbum Atlas 2026.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\Verbum Atlas 2026"; Filename: "{app}\Verbum Atlas 2026.exe"
Name: "{autodesktop}\Verbum Atlas 2026"; Filename: "{app}\Verbum Atlas 2026.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\Verbum Atlas 2026.exe"; Description: "{cm:LaunchProgram,Verbum Atlas 2026}"; Flags: nowait postinstall skipifsilent
