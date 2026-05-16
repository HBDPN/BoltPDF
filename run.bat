@echo off
echo ============================================
echo  BoltPDF Launcher
echo ============================================
echo.
echo Installing dependencies...
pip install -r requirements.txt --quiet
echo.
echo Starting BoltPDF...
python pdf_reader.py %*
pause
