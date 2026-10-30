@echo off
title J.A.R.V.I.S - Otomatik Kurulum
color 0b
echo ===================================================
echo     J.A.R.V.I.S - OTOMATIK SISTEM KURULUMU
echo ===================================================
echo.
cd /d "%~dp0"

:: 1. ADIM: Python Kontrolu
echo [*] Python kontrol ediliyor...
set PYTHON_EXE=

if exist "%LocalAppData%\Programs\Python\Python313\python.exe" (
    set "PYTHON_EXE=%LocalAppData%\Programs\Python\Python313\python.exe"
    goto :python_bulundu
)

py -3.13 --version >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    set "PYTHON_EXE=py -3.13"
    goto :python_bulundu
)

py -3 --version >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    set "PYTHON_EXE=py -3"
    goto :python_bulundu
)

python --version >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    set "PYTHON_EXE=python"
    goto :python_bulundu
)

:: 2. ADIM: Python Bulunamadi - Otomatik Python 3.13 Kurulumu
echo.
echo [!] Bilgisayarda Python tespit edilemedi!
echo [*] Python 3.13 (64-bit) otomatik olarak indiriliyor ve kuruluyor...
echo [*] Lutfen bekleyin, bu islem 1-2 dakika surebilir...
echo.

where winget >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [*] Windows Paket Yoneticisi (winget) ile kuruluyor...
    winget install --id Python.Python.3.13 -e --source winget --accept-source-agreements --accept-package-agreements --silent
    timeout /t 5 >nul
) else (
    echo [*] Resmi Python 3.13 yukleyicisi indiriliyor...
    curl.exe -L -o "%TEMP%\python-3.13.0-amd64.exe" "https://www.python.org/ftp/python/3.13.0/python-3.13.0-amd64.exe"
    echo [*] Python kuruluyor...
    "%TEMP%\python-3.13.0-amd64.exe" /quiet InstallAllUsers=0 PrependPath=1 Include_pip=1
    del /f /q "%TEMP%\python-3.13.0-amd64.exe" 2>nul
    timeout /t 5 >nul
)

:: Yeniden kontrol
if exist "%LocalAppData%\Programs\Python\Python313\python.exe" (
    set "PYTHON_EXE=%LocalAppData%\Programs\Python\Python313\python.exe"
    goto :python_bulundu
)

py -3.13 --version >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    set "PYTHON_EXE=py -3.13"
    goto :python_bulundu
)

set "PYTHON_EXE=python"

:python_bulundu
echo.
echo [+] Python Hazir:
%PYTHON_EXE% --version
echo.

:: 3. ADIM: Kutuphanelerin Kurulumu
echo [*] J.A.R.V.I.S kutuphaneleri yukleniyor (requirements.txt)...
%PYTHON_EXE% -m pip install -r requirements.txt

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [!] Bazi kutuphaneler yuklenirken sorun olustu. Yeniden deneniyor...
    %PYTHON_EXE% -m pip install -r requirements.txt
)

echo.
echo ===================================================
echo     J.A.R.V.I.S Kurulumu Basariyla Tamamlandi!
echo     Baslatmak icin baslat.bat dosyasina tiklayin.
echo ===================================================
echo.
pause
