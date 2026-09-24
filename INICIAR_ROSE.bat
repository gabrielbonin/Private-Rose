@echo off
rem Runs Rose (patch 16.19 fix) from source with administrator rights.
net session >nul 2>&1
if %errorlevel% neq 0 (
    powershell -NoProfile -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" goto setup
if not exist "injection\tools\ltk_patcher_host.exe" goto setup
goto run

:setup
echo Primeira execucao: preparando o Rose...
powershell -NoProfile -ExecutionPolicy Bypass -File "scripts\setup_from_install.ps1"
if %errorlevel% neq 0 (
    pause
    exit /b 1
)

:run
echo Iniciando o Rose. Deixe esta janela aberta enquanto joga.
".venv\Scripts\python.exe" main.py
echo.
echo Rose fechou (codigo %errorlevel%).
pause
