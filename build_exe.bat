@echo off
echo Building Auto Clicker executable...
echo.

REM Create the executable with PyInstaller
python -m PyInstaller --onefile --windowed --name "AutoClicker" --exclude-module PyQt5 auto_clicker.py

echo.
echo Build complete! Check the 'dist' folder for AutoClicker.exe
echo.
pause