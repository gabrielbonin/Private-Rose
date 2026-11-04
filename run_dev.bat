@echo off
rem Runs Rose 1.5.0 from source (this worktree) with administrator rights.
net session >nul 2>&1
if %errorlevel% neq 0 (
    powershell -NoProfile -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)
cd /d "%~dp0"
".venv\Scripts\python.exe" main.py
echo.
echo Rose exited with code %errorlevel%.
pause
