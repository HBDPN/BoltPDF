@echo off
setlocal
echo ============================================
echo  Building BoltPDF...
echo ============================================
echo.

echo [1/5] Version prompt...
python version_prompt.py
if errorlevel 1 (
    echo.
    echo Build aborted.
    pause
    exit /b 1
)

echo.
echo [2/5] Installing build dependencies...
pip install pyinstaller --quiet
pip install -r requirements.txt --quiet

echo.
echo [3/5] Building onedir bundle (this may take a minute)...
pyinstaller --noconfirm --clean BoltPDF.spec

if not exist "dist\BoltPDF\BoltPDF.exe" (
    echo.
    echo Build failed. Check the output above for errors.
    pause
    exit /b 1
)

echo.
echo [4/5] Locating Inno Setup compiler (ISCC)...

set "ISCC="
if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" set "ISCC=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe"      set "ISCC=%ProgramFiles%\Inno Setup 6\ISCC.exe"
if exist "%ProgramFiles(x86)%\Inno Setup 5\ISCC.exe" set "ISCC=%ProgramFiles(x86)%\Inno Setup 5\ISCC.exe"
where ISCC >nul 2>&1 && if not defined ISCC for /f "delims=" %%I in ('where ISCC') do set "ISCC=%%I"

if not defined ISCC (
    echo.
    echo ============================================
    echo  WARNING: Inno Setup not found.
    echo.
    echo  The onedir build succeeded, but no installer
    echo  was produced.  Install Inno Setup 6 from
    echo  https://jrsoftware.org/isinfo.php then run
    echo  this build script again.
    echo.
    echo  Falling back to a plain zip...
    echo ============================================
    echo.
    powershell -NoProfile -Command "Compress-Archive -Path 'dist\BoltPDF\*' -DestinationPath 'dist\BoltPDF.zip' -Force"
    echo  Zip created: dist\BoltPDF.zip
    echo.
    pause
    exit /b 0
)

echo      Found: "%ISCC%"
echo.
echo [5/5] Compiling installer with Inno Setup...
"%ISCC%" BoltPDF.iss
if errorlevel 1 (
    echo.
    echo Installer build failed. Check the output above.
    pause
    exit /b 1
)

echo.
echo ============================================
echo  Build successful!
echo.
echo  Installer:      dist\BoltPDFSetup.exe
echo  onedir bundle:  dist\BoltPDF\
echo  launch exe:     dist\BoltPDF\BoltPDF.exe
echo.
echo  To distribute: ship BoltPDFSetup.exe.  The
echo  user double-clicks it, approves the UAC
echo  prompt, and BoltPDF is installed with a
echo  desktop shortcut and a Start Menu entry.
echo ============================================
echo.
pause
endlocal
