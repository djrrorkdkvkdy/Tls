@echo off
chcp 65001 >nul
cd /d "%~dp0"

where python >nul 2>&1
if %errorlevel%==0 (
    python deploy.py
) else (
    py -3 deploy.py
)

if errorlevel 1 pause
