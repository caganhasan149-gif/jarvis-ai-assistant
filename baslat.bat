@echo off
title J.A.R.V.I.S - Iron Man Edition
echo ===================================================
echo     J.A.R.V.I.S v5.0 - BASLATILIYOR...
echo ===================================================
echo.
cd /d "%~dp0"

if exist "%LocalAppData%\Programs\Python\Python313\python.exe" (
    "%LocalAppData%\Programs\Python\Python313\python.exe" jarvis.py
    goto :bitti
)

py -3.13 jarvis.py 2>nul
if %ERRORLEVEL% EQU 0 goto :bitti

py -3 jarvis.py 2>nul
if %ERRORLEVEL% EQU 0 goto :bitti

python jarvis.py

:bitti
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [HATA] Jarvis calisirken bir sorun olustu.
    pause
)
