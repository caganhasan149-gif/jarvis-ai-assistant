@echo off
echo ============================================
echo   J.A.R.V.I.S - Otomatik Kurulum Basliyor
echo ============================================
echo.

echo [1/3] Python kontrol ediliyor...
py -3.13 --version
if errorlevel 1 (
    echo HATA: Python 3.13 bulunamadi!
    echo Lutfen python.org'dan Python 3.13'u yukle.
    pause
    exit /b
)

echo.
echo [2/3] Kutuphaneler yukleniyor (Bu 2-3 dakika surebilir)...
echo.
py -3.13 -m pip install --upgrade pip
py -3.13 -m pip install -r requirements.txt

echo.
echo [3/3] Kurulum tamamlandi!
echo.
echo Simdi "baslat.bat" dosyasina cift tiklayarak Jarvis'i calistirabilirsin.
echo.
pause