@echo off
title J.A.R.V.I.S v2.0 - Kurulum
echo.
echo  =============================================
echo     J.A.R.V.I.S v2.0 - KURULUM
echo  =============================================
echo.
echo  Gerekli kutuphaneler yukleniyor...
echo.
cd /d "%~dp0"

:: 1. Dogrudan Python 3.13 ile yukleme
if exist "%LocalAppData%\Programs\Python\Python313\python.exe" (
    "%LocalAppData%\Programs\Python\Python313\python.exe" -m pip install -r requirements.txt
    goto :bitti
)

:: 2. Python Launcher 3.13 ile yukleme
py -3.13 --version >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    py -3.13 -m pip install -r requirements.txt
    goto :bitti
)

:: 3. Python Launcher 3 ile yukleme
py -3 --version >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    py -3 -m pip install -r requirements.txt
    goto :bitti
)

:: 4. Genel PATH Python
python -m pip install -r requirements.txt

:bitti
echo.
echo  =============================================
echo     Kurulum tamamlandi!
echo     Baslatmak icin baslat.bat'i calistirin
echo  =============================================
echo.
pause
