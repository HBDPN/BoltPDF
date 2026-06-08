; ==========================================================================
;  BoltPDF — Inno Setup installer script
;  Produces a single BoltPDFSetup.exe that the user double-clicks to:
;     * install BoltPDF into %ProgramFiles%\BoltPDF
;     * create a Desktop shortcut
;     * create a Start Menu shortcut
;     * register an uninstaller
;     * register BoltPDF as a .pdf handler (so it shows up in Open With)
;
;  Build with:    ISCC BoltPDF.iss
;  (or let build.bat run it for you automatically.)
; ==========================================================================

#define MyAppName      "BoltPDF"
#define MyAppVersion   "1.0.4"
#define MyAppPublisher "BoltPDF"
#define MyAppURL       "https://boltpdf.co.uk"
#define MyAppExeName   "BoltPDF.exe"

[Setup]
; A unique GUID that identifies this application to Windows for upgrades and
; uninstall.  Do NOT change this value once you've shipped a release — Windows
; will treat it as a different product if you do.
AppId={{5E3C9F82-8A7D-4B21-9F6E-4C3B2A1D8E77}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; BoltPDF is free software under the GNU Affero GPL v3.  Show the full
; licence text on a page the user must accept before installing, and
; record the copyright/licence in Add-or-Remove-Programs.
AppCopyright=Copyright (C) 2026 BoltPDF - GNU AGPL v3 - source: https://github.com/HBDPN/BoltPDF
LicenseFile=LICENSE

; Install into %ProgramFiles%\BoltPDF (64-bit).
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
DefaultGroupName={#MyAppName}

; Require admin so we can write to Program Files and the machine-wide
; registry for the PDF association.
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog

; Build a 64-bit installer targeting modern Windows.
; (x64compatible covers x64 + ARM64-in-x64-emulation; preferred over the
; legacy "x64" identifier which Inno Setup 6.3+ flags as deprecated.)
ArchitecturesInstallIn64BitMode=x64compatible
ArchitecturesAllowed=x64compatible

; Installer output.
OutputDir=dist
OutputBaseFilename=BoltPDFSetup
SetupIconFile=boltpdf_icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern

; Cosmetic.
ShowLanguageDialog=no
DisableWelcomePage=no
DisableReadyPage=no

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; \
    Description: "{cm:CreateDesktopIcon}"; \
    GroupDescription: "{cm:AdditionalIcons}"; \
    Flags: checkedonce

[Files]
; Recursively ship every file from the PyInstaller onedir bundle.
Source: "dist\BoltPDF\*"; DestDir: "{app}"; \
    Flags: ignoreversion recursesubdirs createallsubdirs
; AGPL-3.0 obligation: the licence and the third-party notices must
; accompany the binary.  Place them prominently in the install root.
Source: "LICENSE"; DestDir: "{app}"; \
    DestName: "LICENSE.txt"; Flags: ignoreversion
Source: "THIRD_PARTY_LICENSES.txt"; DestDir: "{app}"; \
    Flags: ignoreversion

[Icons]
; Start Menu shortcut (always created).
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
; Desktop shortcut (only if the user keeps the task ticked).
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; \
    Tasks: desktopicon
; Uninstaller shortcut in Start Menu.
Name: "{autoprograms}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"

[Run]
; Offer to launch BoltPDF at the end of the installer (post-install).
Filename: "{app}\{#MyAppExeName}"; \
    Description: "Launch {#MyAppName}"; \
    Flags: nowait postinstall skipifsilent

[Registry]
; -- Register the BoltPDF ProgID ----------------------------------------
Root: HKLM; Subkey: "Software\Classes\BoltPDF.Document"; \
    ValueType: string; ValueName: ""; ValueData: "BoltPDF Document"; \
    Flags: uninsdeletekey
Root: HKLM; Subkey: "Software\Classes\BoltPDF.Document\DefaultIcon"; \
    ValueType: string; ValueName: ""; \
    ValueData: "{app}\{#MyAppExeName},0"
Root: HKLM; Subkey: "Software\Classes\BoltPDF.Document\shell\open\command"; \
    ValueType: string; ValueName: ""; \
    ValueData: """{app}\{#MyAppExeName}"" ""%1"""

; -- Register BoltPDF as a handler application for Open With ------------
Root: HKLM; \
    Subkey: "Software\Classes\Applications\{#MyAppExeName}\shell\open\command"; \
    ValueType: string; ValueName: ""; \
    ValueData: """{app}\{#MyAppExeName}"" ""%1"""; \
    Flags: uninsdeletekey
Root: HKLM; \
    Subkey: "Software\Classes\Applications\{#MyAppExeName}\SupportedTypes"; \
    ValueType: string; ValueName: ".pdf"; ValueData: ""

; -- Advertise support for .pdf without stealing it as default ----------
; Windows will show BoltPDF in the "Open With" list and the user can
; choose to make it the default via their own Windows settings.
Root: HKLM; Subkey: "Software\Classes\.pdf\OpenWithProgids"; \
    ValueType: string; ValueName: "BoltPDF.Document"; ValueData: ""; \
    Flags: uninsdeletevalue
