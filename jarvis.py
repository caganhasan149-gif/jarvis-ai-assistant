"""
╔══════════════════════════════════════════════════════════════════════════╗
║               J.A.R.V.I.S - IRON MAN HUD EDITION                        ║
║          Just A Rather Very Intelligent System - Mark V                  ║
║                                                                          ║
║  • 🔵 Fütüristik Ark Reaktörü HUD (Küre Modu & Genişletilmiş Konsol)     ║
║  • 🎤 Sürekli Sohbet Modu (Her seferinde 'Jarvis' demeden kesintisiz)     ║
║  • 🛑 Barge-in: Jarvis konuşurken sözünü kesebilme                       ║
║  • 🧠 Genişletilmiş Niyet Motoru & Eş Anlamlı Kelime Algılama            ║
║  • 💻 Sesle Tam PC & Medya Kontrolü + Groq Llama 3.1 70B AI             ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import re
import time
import math
import random
import datetime
import threading
import subprocess
import webbrowser
import urllib.parse
import ctypes
import secrets
import string
import sqlite3
import requests
import io
import wave
import struct
import shutil
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import tkinter as tk
from tkinter import simpledialog, Text
from difflib import SequenceMatcher

# =========================================================================
# 📦 OPSİYONEL KÜTÜPHANELER (GÜVENLİ VE DAYANIKLI İTHALAT)
# =========================================================================

try:
    import pygame
    pygame.mixer.init()
    PYGAME_VAR = True
except Exception:
    PYGAME_VAR = False

try:
    import speech_recognition as sr
    SR_VAR = True
except Exception:
    SR_VAR = False

try:
    import pyautogui
    PYAUTOGUI_VAR = True
except Exception:
    PYAUTOGUI_VAR = False

try:
    import pygetwindow as gw
    PYGETWINDOW_VAR = True
except Exception:
    PYGETWINDOW_VAR = False

try:
    import pyperclip
    PYPERCLIP_VAR = True
except Exception:
    PYPERCLIP_VAR = False

try:
    import psutil
    PSUTIL_VAR = True
except Exception:
    PSUTIL_VAR = False

try:
    import wikipedia
    WIKIPEDIA_VAR = True
except Exception:
    WIKIPEDIA_VAR = False

try:
    from plyer import notification
    PLYER_VAR = True
except Exception:
    PLYER_VAR = False

try:
    import screen_brightness_control as sbc
    PARLAKLIK_VAR = True
except Exception:
    sbc = None
    PARLAKLIK_VAR = False

try:
    from PIL import ImageGrab
    IMAGEGRAB_VAR = True
except Exception:
    IMAGEGRAB_VAR = False

try:
    from duckduckgo_search import DDGS
    DDGS_VAR = True
except Exception:
    DDGS_VAR = False

try:
    import feedparser
    FEEDPARSER_VAR = True
except Exception:
    FEEDPARSER_VAR = False

try:
    from groq import Groq
    GROQ_VAR = True
except Exception:
    GROQ_VAR = False

try:
    import PyPDF2
    PDF_VAR = True
except Exception:
    PDF_VAR = False

try:
    import docx
    DOCX_VAR = True
except Exception:
    DOCX_VAR = False

try:
    import speedtest
    SPEEDTEST_VAR = True
except Exception:
    SPEEDTEST_VAR = False

# =========================================================================
# ⚙️ KONFİGÜRASYON & BİLGİLER
# =========================================================================

API_KEY = os.environ.get("GROQ_API_KEY", "")
KULLANICI_ADI = "Efendim"
VALORANT_KULLANICI_ADI = ""
VALORANT_SIFRE = ""
SCRCPY_YOLU = r"C:\scrcpy\scrcpy.exe"

WHATSAPP_REHBERI = {
    "anne": "905XXXXXXXXX",
    "baba": "905XXXXXXXXX",
    "kardes": "905XXXXXXXXX",
    "arkadas": "905XXXXXXXXX",
    "sevgili": "905XXXXXXXXX",
}

# Groq istemcisi (Dinamik/Güvenli Yükleme)
groq_client = None

def get_groq_client():
    """Groq istemcisini yerel hafıza veya ortam değişkeninden güvenle başlatır"""
    global groq_client
    if groq_client is None and GROQ_VAR:
        key = os.environ.get("GROQ_API_KEY", "")
        if not key:
            key = ayar_getir("groq_api_key", API_KEY)
        if key and len(key) > 10:
            try:
                groq_client = Groq(api_key=key)
            except Exception:
                pass
    return groq_client

# =========================================================================
# 🎨 STARK INDUSTRIES TEMALARI
# =========================================================================

TEMALAR = {
    "varsayilan": {
        "ad": "Stark Arc (Cyan)",
        "ana": "#00d4ff",
        "ikincil": "#ffaa00",
        "arka": "#050816",
        "panel": "#0a0e27",
        "glow": "#33eeff",
        "metin": "#e0f7fa"
    },
    "mark_vii": {
        "ad": "Iron Man Mark VII (Kırmızı/Altın)",
        "ana": "#ff1a40",
        "ikincil": "#ffc107",
        "arka": "#1a0505",
        "panel": "#2d0a0a",
        "glow": "#ff4d6a",
        "metin": "#ffebee"
    },
    "stealth": {
        "ad": "Stealth Armor (Matrix)",
        "ana": "#00ff66",
        "ikincil": "#00aa44",
        "arka": "#020a04",
        "panel": "#051f0c",
        "glow": "#33ff88",
        "metin": "#e8f5e9"
    },
    "hulkbuster": {
        "ad": "Hulkbuster (Mor/Neon)",
        "ana": "#aa00ff",
        "ikincil": "#ff00aa",
        "arka": "#0d0417",
        "panel": "#1d0833",
        "glow": "#cc33ff",
        "metin": "#f3e5f5"
    },
    "midnight": {
        "ad": "Midnight Stealth (Lacivert)",
        "ana": "#58a6ff",
        "ikincil": "#f0883e",
        "arka": "#0d1117",
        "panel": "#161b22",
        "glow": "#79c0ff",
        "metin": "#c9d1d9"
    }
}
simdiki_tema = "varsayilan"

# =========================================================================
# 🎲 EĞLENCE & BİLGİ VERİLERİ
# =========================================================================

MOTIVASYON_SOZLERI = [
    "Kendi sınırlarını zorlamadan ne kadar ileri gidebileceğini bilemezsin.",
    "Bazen yürümeyi öğrenmeden önce koşmak gerekir. — Tony Stark",
    "Gelecek, onu bugünden inşa edenlere aittir.",
    "Büyük başarılar, pes etmeyenlerin eseridir.",
    "Zorluklar, yeteneklerinizi sergilemeniz için birer fırsattır.",
    "Disiplin, hedefler ile başarı arasındaki köprüdür."
]

FIKRALAR = [
    "Yazılımcı karısına 'Markete git, yumurta varsa 6 tane al' demiş. Yazılımcı 6 ekmek alıp dönmüş.",
    "Yazılımcı neden gözlük takar? Çünkü C# (see sharp) yapamaz!",
    "Bir gün 0 ile 1 karşılaşmış. 0 sormuş: 'Nasılsın?' 1: 'İyiyim, sen?' 0: 'Ben de boşum!'",
    "Dünyada 10 çeşit insan vardır: İkili sistemi bilenler ve bilmeyenler."
]

# =========================================================================
# 🧠 VERİTABANI YÖNETİMİ (OTOMATİK MİGRASYON & VERİ GÜVENLİĞİ)
# =========================================================================

DB_PATH_MASAUSTU = os.path.join(os.path.expanduser("~"), "Desktop", "jarvis_hafiza.db")
DB_PATH_YEREL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jarvis_hafiza.db")

def db_baglanti():
    """Masaüstü ve yerel fallback destekli veritabanı bağlantısı"""
    try:
        conn = sqlite3.connect(DB_PATH_MASAUSTU)
        return conn
    except Exception:
        return sqlite3.connect(DB_PATH_YEREL)

def veritabani_olustur():
    """Tabloları kurar ve eski veritabanı şemasını otomatik günceller"""
    conn = db_baglanti()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS hatirlatmalar (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        tarih TEXT, 
        mesaj TEXT, 
        tamamlandi INTEGER DEFAULT 0,
        olusturma_tarihi TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS gecmis (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        soru TEXT, 
        cevap TEXT, 
        tarih TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS notlar (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        baslik TEXT, 
        icerik TEXT, 
        kategori TEXT DEFAULT 'genel',
        tarih TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS ayarlar (
        anahtar TEXT PRIMARY KEY,
        deger TEXT
    )''')
    conn.commit()

    # Otomatik Şema Migrasyonu
    try:
        c.execute("PRAGMA table_info(hatirlatmalar)")
        kolonlar = [r[1] for r in c.fetchall()]
        if "tamamlandi" not in kolonlar:
            c.execute("ALTER TABLE hatirlatmalar ADD COLUMN tamamlandi INTEGER DEFAULT 0")
            conn.commit()
    except Exception:
        pass

    try:
        c.execute("PRAGMA table_info(notlar)")
        kolonlar_not = [r[1] for r in c.fetchall()]
        if "kategori" not in kolonlar_not:
            c.execute("ALTER TABLE notlar ADD COLUMN kategori TEXT DEFAULT 'genel'")
            conn.commit()
    except Exception:
        pass

    conn.close()

def hatirlatma_ekle(tarih, mesaj):
    conn = db_baglanti()
    c = conn.cursor()
    simdi = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    c.execute("INSERT INTO hatirlatmalar (tarih, mesaj, tamamlandi, olusturma_tarihi) VALUES (?, ?, 0, ?)", (tarih, mesaj, simdi))
    conn.commit()
    conn.close()

def hatirlatmalari_getir(tarih=None):
    conn = db_baglanti()
    c = conn.cursor()
    if tarih:
        c.execute("SELECT id, tarih, mesaj FROM hatirlatmalar WHERE tarih = ? AND tamamlandi = 0 ORDER BY id", (tarih,))
    else:
        c.execute("SELECT id, tarih, mesaj FROM hatirlatmalar WHERE tamamlandi = 0 ORDER BY tarih")
    sonuclar = c.fetchall()
    conn.close()
    return sonuclar

def not_ekle(baslik, icerik):
    conn = db_baglanti()
    c = conn.cursor()
    simdi = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    c.execute("INSERT INTO notlar (baslik, icerik, tarih) VALUES (?, ?, ?)", (baslik, icerik, simdi))
    conn.commit()
    conn.close()

def notlari_getir():
    conn = db_baglanti()
    c = conn.cursor()
    c.execute("SELECT baslik, icerik, tarih FROM notlar ORDER BY id DESC LIMIT 10")
    sonuclar = c.fetchall()
    conn.close()
    return sonuclar

def gecmis_kaydet(soru, cevap):
    conn = db_baglanti()
    c = conn.cursor()
    simdi = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    c.execute("INSERT INTO gecmis (soru, cevap, tarih) VALUES (?, ?, ?)", (soru, cevap, simdi))
    conn.commit()
    conn.close()

def hafizayi_temizle():
    conn = db_baglanti()
    c = conn.cursor()
    c.execute("DELETE FROM hatirlatmalar")
    c.execute("DELETE FROM notlar")
    c.execute("DELETE FROM gecmis")
    conn.commit()
    conn.close()

def ayar_kaydet(anahtar, deger):
    conn = db_baglanti()
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO ayarlar (anahtar, deger) VALUES (?, ?)", (anahtar, str(deger)))
    conn.commit()
    conn.close()

def ayar_getir(anahtar, varsayilan=""):
    conn = db_baglanti()
    c = conn.cursor()
    c.execute("SELECT deger FROM ayarlar WHERE anahtar = ?", (anahtar,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else varsayilan

# =========================================================================
# 🔊 FÜTÜRİSTİK SES EFEKTLERİ & REAKTÖR SESİ (SAF PYTHON SENTEZİ)
# =========================================================================

WAKE_SOUND = None

def _wake_sesi_hazirla():
    """Iron Man repulsor / HUD uyanma sesini saf Python wave ile bellekte sentezler"""
    global WAKE_SOUND
    if not PYGAME_VAR:
        return
    try:
        sample_rate = 44100
        duration = 0.28
        num_samples = int(sample_rate * duration)
        buf = io.BytesIO()
        with wave.open(buf, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            for i in range(num_samples):
                t = i / sample_rate
                # 480Hz -> 1350Hz yükselen fütüristik reaktör açılış tonu
                freq = 480 + (870 * (t / duration) ** 2)
                env = math.sin(math.pi * (t / duration)) ** 0.6
                val = env * (0.65 * math.sin(2 * math.pi * freq * t) + 0.35 * math.sin(4 * math.pi * freq * t))
                sample = int(val * 32767 * 0.45)
                wav_file.writeframesraw(struct.pack('<h', max(-32768, min(32767, sample))))
        WAKE_SOUND = pygame.mixer.Sound(io.BytesIO(buf.getvalue()))
        WAKE_SOUND.set_volume(0.5)
    except Exception:
        WAKE_SOUND = None

def ses_efekti_cal(tip="wake"):
    """Iron Man HUD uyanma ses efektini anında çalar"""
    try:
        global WAKE_SOUND
        if WAKE_SOUND is None and PYGAME_VAR:
            _wake_sesi_hazirla()
        if WAKE_SOUND:
            WAKE_SOUND.play()
    except Exception:
        pass

# =========================================================================
# 🎤 SES MOTORU & BARGE-IN (SÖZÜNÜ KESME DESTEĞİ)
# =========================================================================

ses_caliniyor = False
ses_durdurulsun_mu = False

def konusmayi_kes():
    """Jarvis konuşurken araya girildiğinde sesi anında susturur"""
    global ses_durdurulsun_mu, ses_caliniyor
    ses_durdurulsun_mu = True
    if PYGAME_VAR:
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
        except Exception:
            pass
    if os.name == 'nt':
        try:
            ctypes.windll.winmm.mciSendStringW('close all', None, 0, 0)
        except Exception:
            pass
    ses_caliniyor = False

def sesli_konus(mesaj):
    """Metni seslendirir (Barge-in / Sözünü kesme yeteneği ile)"""
    global ses_caliniyor, ses_durdurulsun_mu
    konusmayi_kes()
    ses_durdurulsun_mu = False
    ses_caliniyor = True

    log_mesaj(f"🤖 {mesaj}", "jarvis")
    durum_guncelle("KONUŞUYOR")

    # 1. Öncelik: Edge TTS (Doğal Türkçe İnsan Sesi)
    calindi = False
    try:
        import edge_tts
        import asyncio
        dosya = os.path.abspath(f"jarvis_tts_{int(time.time() * 1000)}.mp3")
        ses_adi = "tr-TR-AhmetNeural"  # Elit karizmatik asistan sesi
        communicate = edge_tts.Communicate(mesaj, ses_adi, rate="+15%")
        asyncio.run(communicate.save(dosya))

        if not ses_durdurulsun_mu and PYGAME_VAR:
            pygame.mixer.music.load(dosya)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() and not ses_durdurulsun_mu:
                time.sleep(0.05)
            pygame.mixer.music.unload()
            calindi = True

        if not calindi and not ses_durdurulsun_mu and os.name == 'nt':
            alias = f"mp3_{int(time.time() * 1000)}"
            winmm = ctypes.windll.winmm
            winmm.mciSendStringW(f'open "{dosya}" type mpegvideo alias {alias}', None, 0, 0)
            winmm.mciSendStringW(f'play {alias}', None, 0, 0)
            calindi = True

        try:
            if os.path.exists(dosya):
                os.remove(dosya)
        except Exception:
            pass
    except Exception:
        calindi = False

    # 2. Öncelik Fallback: gTTS
    if not calindi and not ses_durdurulsun_mu:
        try:
            from gtts import gTTS
            dosya = os.path.abspath(f"jarvis_gtts_{int(time.time() * 1000)}.mp3")
            gTTS(text=mesaj, lang='tr').save(dosya)
            if PYGAME_VAR:
                pygame.mixer.music.load(dosya)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy() and not ses_durdurulsun_mu:
                    time.sleep(0.05)
                pygame.mixer.music.unload()
            try:
                os.remove(dosya)
            except Exception:
                pass
        except Exception:
            pass

    # 3. Öncelik Fallback: Yerel pyttsx3 (Çevrimdışı / Tam Güvenilirlik)
    if not calindi and not ses_durdurulsun_mu:
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.say(mesaj)
            engine.runAndWait()
            calindi = True
        except Exception:
            pass

    ses_caliniyor = False
    durum_guncelle("BEKLEMEDE")

# =========================================================================
# 👂 SES TANIMA & DİNLEME
# =========================================================================

recognizer = sr.Recognizer() if SR_VAR else None
if recognizer:
    recognizer.energy_threshold = 250
    recognizer.dynamic_energy_threshold = True

def ses_dinle(timeout=8, limit=8):
    """Mikrofondan ses alır ve metne dönüştürür"""
    if not SR_VAR or not recognizer:
        return "anlasilamadi"
    
    with sr.Microphone() as source:
        durum_guncelle("DİNLİYOR")
        recognizer.adjust_for_ambient_noise(source, duration=0.4)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=limit)
            durum_guncelle("İŞLENİYOR")
            metin = recognizer.recognize_google(audio, language="tr-TR")
            log_mesaj(f"👤 {metin}", "user")
            return metin.lower().strip()
        except sr.WaitTimeoutError:
            return "zaman_asimi"
        except sr.UnknownValueError:
            return "anlasilamadi"
        except Exception:
            return "hata"
        finally:
            durum_guncelle("BEKLEMEDE")

def wake_word_kontrol(metin):
    """Gelişmiş Wake-Word Algılayıcı (Farklı telaffuzlar ve kökler)"""
    if not metin:
        return False
    tam_eslesmeler = [
        "jarvis", "carvis", "çarvis", "yarvis", "şarvis", "harvis", 
        "hey jarvis", "hey carvis", "heyjan", "heycan", "biz geldik", 
        "uyan jarvis", "asistan"
    ]
    if metin in tam_eslesmeler:
        return True
    kelimeler = metin.split()
    for k in kelimeler:
        if any(kok in k for kok in ["jarv", "carv", "çarv", "heyjan", "heycan", "yarv"]):
            return True
    return False

# =========================================================================
# 🧠 GENİŞLETİLMİŞ NİYET MOTORU (SEMANTİK EŞLEŞTİRME & EŞ ANLAMLILAR)
# =========================================================================

def niyet_kontrol(metin, kaliplar):
    """Gelişmiş bulanık ve anlamsal kalıp eşleştirici"""
    metin_lower = metin.lower()
    for kalip in kaliplar:
        kalip_lower = kalip.lower()
        # Tam alt dize kontrolü
        if kalip_lower in metin_lower:
            return True
        # Kalıptaki kelimelerin çoğu metinde geçiyor mu?
        kalip_kelimeleri = kalip_lower.split()
        if len(kalip_kelimeleri) > 1:
            eslesen_kelime = sum(1 for k in kalip_kelimeleri if k in metin_lower)
            if eslesen_kelime / len(kalip_kelimeleri) >= 0.7:
                return True
        # Fuzzy benzerlik oranı
        if SequenceMatcher(None, metin_lower, kalip_lower).ratio() > 0.75:
            return True
    return False

def yapay_zeka_sor(soru):
    """Groq AI ile öz, kısa ve doğrudan yanıt (Gereksiz gevezelik ve rol yapma engelli)"""
    client = get_groq_client()
    if not GROQ_VAR or not client:
        return "Efendim, yapay zeka modülü hazır değil fakat tüm sistem komutlarınızı yerine getirebilirim."
    
    sistem_promtu = (
        f"Sen J.A.R.V.I.S adında profesyonel, son derece akıllı, net ve pratik bir masaüstü yapay zeka asistanısın. "
        f"Kullanıcıya '{KULLANICI_ADI}' diye hitap et. "
        f"KESİN KURALLAR:\n"
        f"1. Kesinlikle Marvel, Iron Man, Tony Stark, süper kahraman evreni, kurgusal zırh veya reaktör muhabbeti yapma ve rol yapma.\n"
        f"2. Asla boş laf etme, lafı uzatma, gevezelik yapma, giriş-çıkış lafları söyleme.\n"
        f"3. Sorulan soruya doğrudan, net, öz ve en fazla 1-2 kısa cümle ile cevap ver. Türkçe konuş."
    )
    
    # Canlı testle doğrulanmış aktif modeller
    modeller = [
        "qwen/qwen3.8-27b",
        "openai/gpt-oss-120b",
        "openai/gpt-oss-20b"
    ]
    
    son_hata = ""
    for model_adi in modeller:
        try:
            chat = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": sistem_promtu},
                    {"role": "user", "content": soru}
                ],
                model=model_adi,
                max_tokens=90,
                temperature=0.4
            )
            return chat.choices[0].message.content.strip()
        except Exception as e:
            son_hata = str(e)
            continue
            
    return f"Sistemlerimde ufak bir dalgalanma oldu efendim: {son_hata[:70]}"

# =========================================================================
# 🛠️ PC VE SİSTEM YÖNETİMİ FONKSİYONLARI
# =========================================================================

def ses_ayarla(seviye_komutu):
    """Sistem sesini ayarlar veya yüzde verir"""
    try:
        user32 = ctypes.windll.user32
        VK_VOLUME_UP = 0xAF
        VK_VOLUME_DOWN = 0xAE
        VK_VOLUME_MUTE = 0xAD

        def tus_bas(vk):
            user32.keybd_event(vk, 0, 0, 0)
            user32.keybd_event(vk, 0, 2, 0)

        if any(k in seviye_komutu for k in ["kapat", "sessize al", "sustur", "mute"]):
            tus_bas(VK_VOLUME_MUTE)
            return "Ses kapatıldı efendim."
        elif any(k in seviye_komutu for k in ["aç", "yükselt", "kökle", "artır", "ses ver", "duyamıyorum"]):
            for _ in range(8):
                tus_bas(VK_VOLUME_UP)
            return "Ses seviyesi yükseltildi efendim."
        elif any(k in seviye_komutu for k in ["kıs", "alçalt", "kulağımı tırmalıyor", "biraz kıs"]):
            for _ in range(8):
                tus_bas(VK_VOLUME_DOWN)
            return "Ses seviyesi kısıldı efendim."
        return "Ses seviyesi güncellendi."
    except Exception as e:
        return f"Ses kontrol hatası: {e}"

def temizle_sarki_komutu(komut):
    """Komuttaki ekleri ve dolgu kelimelerini temizleyip net şarkı/sanatçı adını çıkarır"""
    metin = komut.lower()
    # Spotify ve türevleri + çekim ekleri
    metin = re.sub(r'\b(spotify|spotidy)(\'?(dan|den|da|de))?\b', ' ', metin)
    # Bağımsız ekler ve müzik/çalma kelimeleri
    metin = re.sub(r'\b(dan|den|da|de|bana|bize|bir|bi|parça|parca|şarkısını|sarkisini|şarkısı|sarkisi|şarkı|sarkı|sarki|müziğini|muzigini|müzik|muzik|çal|cal|aç|ac|patlat|oynat|dinlet)\b', ' ', metin)
    metin = re.sub(r'\s+', ' ', metin).strip()
    return metin

def spotify_pencere_odakla():
    """Spotify penceresini bulup güvenli şekilde öne getirir"""
    try:
        os.system("start spotify:")
        time.sleep(0.4)
    except Exception:
        pass

    if PYGETWINDOW_VAR:
        try:
            pencereler = [w for w in gw.getAllWindows() if w.title and ('spotify' in w.title.lower() or ' - ' in w.title)]
            if pencereler:
                pencereler[0].activate()
                return True
        except Exception:
            pass

    try:
        import win32gui
        user32 = ctypes.windll.user32
        found_hwnds = []
        def enum_cb(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                cls = win32gui.GetClassName(hwnd)
                if 'Chrome_WidgetWin_0' in cls or 'spotify' in title.lower():
                    found_hwnds.append(hwnd)
        win32gui.EnumWindows(enum_cb, None)
        if found_hwnds:
            hwnd = found_hwnds[0]
            user32.keybd_event(0x12, 0, 0, 0)
            user32.SetForegroundWindow(hwnd)
            user32.keybd_event(0x12, 0, 2, 0)
            return True
    except Exception:
        pass
    return False

def spotify_komut_isle(komut):
    """Spotify garantili kontrol (Hızlı Arama Ctrl+K, Doğal Oynatma, Web Player Fallback)"""
    try:
        user32 = ctypes.windll.user32
        VK_MEDIA_PLAY_PAUSE = 0xB3
        VK_MEDIA_NEXT_TRACK = 0xB0
        VK_MEDIA_PREV_TRACK = 0xB1
        VK_MEDIA_STOP = 0xB2

        def tus(vk):
            user32.keybd_event(vk, 0, 0, 0)
            user32.keybd_event(vk, 0, 2, 0)

        # Durdurma / Müzik Kapatma
        if any(k in komut for k in ["durdur", "pause", "beklet", "şarkıyı kapat", "müziği kapat", "kapat şarkıyı", "müziği sustur"]):
            tus(VK_MEDIA_PLAY_PAUSE)
            return "Müzik duraklatıldı efendim."
        elif any(k in komut for k in ["sonraki", "sıradaki", "geç", "başka şarkı", "değiştir"]):
            tus(VK_MEDIA_NEXT_TRACK)
            return "Sıradaki parçaya geçildi efendim."
        elif any(k in komut for k in ["önceki", "başa al"]):
            tus(VK_MEDIA_PREV_TRACK)
            return "Önceki parçaya dönüldü."

        sarki = temizle_sarki_komutu(komut)

        # Eğer spesifik bir şarkı adı kalmadıysa (sadece 'spotify aç', 'şarkı çal', 'müzik çal' vb. denmişse)
        if not sarki:
            os.system("start spotify:")
            time.sleep(0.5)
            tus(VK_MEDIA_PLAY_PAUSE)
            return "Spotify başlatıldı ve müzik devam ettiriliyor efendim."

        # Belirli bir şarkı adı varsa: Spotify Hızlı Arama (Ctrl+K) ile doğrudan başlat
        def garantili_cal():
            calindi = False
            try:
                # 1. Spotify'ı öne getir
                spotify_pencere_odakla()
                time.sleep(0.6)

                if PYAUTOGUI_VAR:
                    # Spotify Hızlı Arama (Quick Search): Ctrl + K
                    pyautogui.hotkey('ctrl', 'k')
                    time.sleep(0.4)

                    # Türkçe karakter kaybını önlemek için panodan yapıştır
                    if PYPERCLIP_VAR:
                        pyperclip.copy(sarki)
                        pyautogui.hotkey('ctrl', 'v')
                    else:
                        pyautogui.write(sarki, interval=0.03)

                    # Arama sonuçlarının yüklenmesi için bekle
                    time.sleep(1.0)

                    # İlk sonucu başlat
                    pyautogui.press('enter')
                    time.sleep(0.4)
                    pyautogui.press('enter')
                    calindi = True
            except Exception:
                calindi = False

            # Eğer masaüstü uygulaması açılamazsa Spotify Web Player'da aç
            if not calindi:
                webbrowser.open_new_tab(f"https://open.spotify.com/search/{urllib.parse.quote(sarki)}")

        threading.Thread(target=garantili_cal, daemon=True).start()
        return f"'{sarki}' parçası Spotify'da aranıyor ve çalınıyor efendim."

    except Exception as e:
        return f"Spotify işlemi gerçekleştirilemedi: {e}"

# =========================================================================
# 🌐 CHROME & WEB GEZİNTİ YÖNETİMİ
# =========================================================================

def chrome_arama_yap(sorgu):
    """Google'da veya Chrome'da arama yapar"""
    temiz = sorgu
    for k in ["google'da ara", "googleda ara", "google'da", "google", "chrome'da ara", "internette ara", "arama yap", "ara"]:
        temiz = temiz.replace(k, "")
    arama_terimi = temiz.strip()
    if arama_terimi:
        url = f"https://www.google.com/search?q={urllib.parse.quote(arama_terimi)}"
        webbrowser.open_new_tab(url)
        return f"Google'da '{arama_terimi}' aranıyor efendim."
    else:
        webbrowser.open_new_tab("https://www.google.com")
        return "Google açılıyor efendim."

def chrome_yeni_sekme(url=None):
    """Chrome'da yeni sekme veya web sayfası açar"""
    if url:
        if not url.startswith("http"):
            url = f"https://{url}"
        webbrowser.open_new_tab(url)
        return f"{url} yeni sekmede açıldı efendim."
    else:
        webbrowser.open_new_tab("https://www.google.com")
        return "Chrome'da yeni sekme açıldı efendim."

def chrome_sekme_kapat():
    """Mevcut sekmeyi kapatır (Ctrl+W)"""
    if PYAUTOGUI_VAR:
        pyautogui.hotkey('ctrl', 'w')
        return "Sekme kapatıldı efendim."
    return "Sekme kapatılamadı."

# =========================================================================
# 📋 PANO, WIKIPEDIA, ZAMANLAYICI VE EKSTRA ELİT FONKSİYONLAR
# =========================================================================

def panoya_kopyala(metin):
    """Metni Windows panosuna kopyalar"""
    try:
        if root:
            root.clipboard_clear()
            root.clipboard_append(metin)
            root.update()
            return True
    except Exception:
        pass
    return False

def panoyu_oku():
    """Windows panosundaki metni alır ve okur"""
    try:
        if root:
            metin = root.clipboard_get()
            if metin and metin.strip():
                kisa = metin.strip()[:300]
                return f"Panodaki metin: {kisa}"
            return "Panonuz boş efendim."
    except Exception:
        return "Panodaki metin okunamadı efendim."
    return "Pano boş."

def wikipedia_ozet_al(konu):
    """Wikipedia REST API üzerinden konu özeti çeker"""
    temiz = konu
    for k in ["wikipedia'da ara", "wikipediada ara", "wikipedia", "vikipedi", "kimdir", "nedir", "hakkında bilgi ver", "bilgi ver"]:
        temiz = temiz.replace(k, "")
    arama = temiz.strip()
    if not arama:
        return "Hangi konuyu araştırmamı istersiniz efendim?"
    
    try:
        headers = {'User-Agent': 'JarvisAssistant/2.0 (stark@jarvis.ai)'}
        url = f"https://tr.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(arama)}"
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code == 200:
            veri = res.json()
            ozet = veri.get('extract', '')
            if ozet:
                # Çok uzunsa ilk 2 cümleyi al
                cumleler = ozet.split('. ')
                return f"{arama} hakkında Wikipedia bilgisi: {'. '.join(cumleler[:2])}."
        # Wikipedia bulamazsa yapay zekaya sor
        return yapay_zeka_sor(f"{arama} kimdir/nedir? 2 cümlede özetle.")
    except Exception:
        return yapay_zeka_sor(f"{arama} kimdir/nedir? 2 cümlede özetle.")

def parlaklik_ayarla(komut):
    """Ekran parlaklığını ayarlar"""
    if not PARLAKLIK_VAR:
        return "Monitör parlaklık kontrolü desteklenmiyor efendim."
    try:
        import screen_brightness_control as sbc
        mevcut = sbc.get_brightness(display=0)
        if isinstance(mevcut, list): mevcut = mevcut[0]

        if "yüzde" in komut:
            # Sayıyı bul
            for kelime in komut.split():
                if kelime.isdigit():
                    hedef = min(100, max(10, int(kelime)))
                    sbc.set_brightness(hedef, display=0)
                    return f"Ekran parlaklığı yüzde {hedef} olarak ayarlandı efendim."
        
        if any(k in komut for k in ["fulle", "en yüksek", "maksimum", "artır", "yükselt"]):
            sbc.set_brightness(90, display=0)
            return "Ekran parlaklığı artırıldı efendim."
        elif any(k in komut for k in ["kıs", "düşür", "azalt", "gözümü alıyor", "karart"]):
            sbc.set_brightness(30, display=0)
            return "Ekran parlaklığı düşürüldü efendim."
        return f"Mevcut ekran parlaklığı yüzde {mevcut} efendim."
    except Exception as e:
        return f"Parlaklık ayarlanamadı: {e}"

def zamanlayici_baslat(sure_saniye, etiket="Sayaç"):
    """Dinamik zamanlayıcı başlatır"""
    def say():
        time.sleep(sure_saniye)
        sesli_konus(f"Efendim! {etiket} süreniz doldu.")
        if PLYER_VAR:
            notification.notify(title=f"⏰ {etiket} Bitti", message=f"{sure_saniye} saniyelik zaman doldu!", app_name="J.A.R.V.I.S")
    threading.Thread(target=say, daemon=True).start()
    dk = sure_saniye // 60
    sn = sure_saniye % 60
    sure_metin = f"{dk} dakika " if dk > 0 else ""
    sure_metin += f"{sn} saniye" if sn > 0 else ""
    return f"{sure_metin} için zamanlayıcı kuruldu efendim."

def ekran_goruntusu_al():
    """Ekran görüntüsü alıp masaüstüne kaydeder"""
    if not IMAGEGRAB_VAR:
        return "Ekran görüntüsü modülü hazır değil."
    try:
        dosya = os.path.join(os.path.expanduser("~"), "Desktop", f"jarvis_snap_{int(time.time())}.png")
        ImageGrab.grab().save(dosya)
        if PLYER_VAR:
            notification.notify(title="📸 Ekran Yakalandı", message=dosya, app_name="J.A.R.V.I.S", timeout=5)
        return "Ekran görüntüsü masaüstünüze kaydedildi efendim."
    except Exception as e:
        return f"Ekran görüntüsü alınamadı: {e}"

def sistem_durumu():
    """Canlı sistem kaynaklarını raporlar"""
    if not PSUTIL_VAR:
        return "Sistem izleme modülü bulunamadı."
    try:
        cpu = psutil.cpu_percent(interval=0.3)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('C:\\')
        pil_metni = ""
        pil = psutil.sensors_battery()
        if pil:
            durum = "Şarj Oluyor" if pil.power_plugged else "Pilde"
            pil_metni = f", Pil: %{pil.percent} ({durum})"
        return f"CPU: %{cpu}, Bellek Kullanımı: %{ram.percent}, Disk: %{disk.percent}{pil_metni} efendim."
    except Exception:
        return "Sistem verilerine erişilemedi."

def pencereleri_simge_yap():
    """Tüm pencereleri küçültüp masaüstünü açar"""
    if PYAUTOGUI_VAR:
        pyautogui.hotkey('win', 'd')
        return "Masaüstü gösteriliyor efendim."
    return "İşlem gerçekleştirilemedi."

def valorant_otomatik_giris():
    """Valorant'ı açar ve 12 saniye sonra şifreyi girer"""
    try:
        os.system("start riotclient://launch?launchProduct=VALORANT&launchPatchline=Live")
        def giris():
            time.sleep(12)
            if PYAUTOGUI_VAR and PYGETWINDOW_VAR:
                pencereler = gw.getWindowsWithTitle('Riot Client') or gw.getWindowsWithTitle('VALORANT')
                if pencereler:
                    p = pencereler[0]
                    try: p.activate()
                    except: pass
                    time.sleep(1)
                    pyautogui.press('esc')
                    time.sleep(0.5)
                    kadi = ayar_getir("valorant_kullanici", VALORANT_KULLANICI_ADI)
                    sifre = ayar_getir("valorant_sifre", VALORANT_SIFRE)
                    pyautogui.write(kadi, interval=0.08)
                    time.sleep(0.4)
                    pyautogui.press('tab')
                    time.sleep(0.4)
                    pyautogui.write(sifre, interval=0.08)
                    time.sleep(0.4)
                    pyautogui.press('enter')
        threading.Thread(target=giris, daemon=True).start()
        return "Valorant açılıyor efendim. 12 saniye sonra otomatik giriş sağlanacak."
    except Exception as e:
        return f"Valorant açılamadı: {e}"

def doviz_durumu():
    """Canlı döviz ve kripto fiyatlarını çeker"""
    try:
        res = requests.get("https://open.er-api.com/v6/latest/USD", timeout=4).json()
        usd = res['rates']['TRY']
        eur = usd / res['rates']['EUR']
        crypto = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd", timeout=4).json()
        btc = crypto.get('bitcoin', {}).get('usd', 'N/A')
        return f"Dolar: {usd:.2f} TL, Euro: {eur:.2f} TL, Bitcoin: ${btc:,} efendim."
    except Exception:
        return "Finansal verileri çekemedim efendim."

def hava_durumu_al(sehir="Istanbul"):
    """Canlı hava durumunu getirir"""
    try:
        res = requests.get(f"https://wttr.in/{sehir}?format=%C+%t+%w&lang=tr", timeout=4)
        if res.status_code == 200:
            return f"{sehir} için hava durumu: {res.text.strip()} efendim."
        return "Hava durumu verisi alınamadı."
    except Exception:
        return "Hava durumu servisine bağlanamadım."

# =========================================================================
# 📄 YEREL DOSYA OKUMA & ÖZETLEME (PDF, DOCX, TXT + GROQ AI)
# =========================================================================

def dosya_oku_ve_ozetle(komut):
    """Masaüstü, İndirilenler veya Belgeler klasöründeki dosyayı bulur, okur ve AI ile özetler"""
    temiz = komut.lower()
    for atilacak in ["dosyasını oku ve özetle", "dosyasını özetle", "dosyasını oku", "belgesini özetle", "belgesini oku", "oku ve özetle", "özetle", "oku"]:
        temiz = temiz.replace(atilacak, " ")
    
    # Dosya adını veya uzantısını ayıkla
    dosya_adi_eslesme = re.search(r'([a-zA-Z0-9_\-\.\sçğıöşüÇĞİÖŞÜ]+\.(?:pdf|docx|doc|txt|md))', komut, re.IGNORECASE)
    aranan_ad = dosya_adi_eslesme.group(1).strip() if dosya_adi_eslesme else temiz.strip()

    arama_dizinleri = [
        os.path.join(os.path.expanduser("~"), "Desktop"),
        os.path.join(os.path.expanduser("~"), "Downloads"),
        os.path.join(os.path.expanduser("~"), "Documents"),
        os.path.dirname(os.path.abspath(__file__))
    ]
    
    hedef_dosya = None
    if aranan_ad:
        for dizin in arama_dizinleri:
            if not os.path.exists(dizin):
                continue
            tam_yol = os.path.join(dizin, aranan_ad)
            if os.path.exists(tam_yol) and os.path.isfile(tam_yol):
                hedef_dosya = tam_yol
                break
            for f in os.listdir(dizin):
                if aranan_ad.lower() in f.lower() and f.lower().endswith(('.pdf', '.docx', '.txt', '.md')):
                    hedef_dosya = os.path.join(dizin, f)
                    break
            if hedef_dosya:
                break
                
    if not hedef_dosya:
        return f"'{aranan_ad}' adlı dosyayı Masaüstü veya İndirilenler klasöründe bulamadım efendim. Lütfen dosya adını kontrol edin."

    dosya_uzanti = os.path.splitext(hedef_dosya)[1].lower()
    metin = ""

    try:
        if dosya_uzanti == ".pdf":
            if not PDF_VAR:
                return "PDF okuma modülü (PyPDF2) hazır değil efendim."
            reader = PyPDF2.PdfReader(hedef_dosya)
            for page in reader.pages[:10]:
                t = page.extract_text()
                if t: metin += t + "\n"
        elif dosya_uzanti in [".docx", ".doc"]:
            if not DOCX_VAR:
                return "Word belgesi okuma modülü (python-docx) hazır değil efendim."
            doc = docx.Document(hedef_dosya)
            metin = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        else:
            with open(hedef_dosya, 'r', encoding='utf-8', errors='ignore') as f:
                metin = f.read()
    except Exception as e:
        return f"Dosya okunurken bir hata oluştu efendim: {e}"

    if not metin or len(metin.strip()) < 10:
        return f"{os.path.basename(hedef_dosya)} belgesinde okunabilir metin bulunamadı efendim."

    prompt = (
        f"Sen J.A.R.V.I.S.'sın. Kullanıcının '{os.path.basename(hedef_dosya)}' adlı belgesinin metni aşağıdadır. "
        f"Bu belgeyi en fazla 3-4 net, anlaşılır ve elit Türkçe cümleyle özetle. "
        f"Gereksiz 'İşte özet:' gibi giriş cümleleri kurmadan doğrudan özeti ver:\n\n{metin[:4500]}"
    )
    ozet = yapay_zeka_sor(prompt)
    return f"{os.path.basename(hedef_dosya)} belgesinin özeti: {ozet}"

# =========================================================================
# 📧 SESLİ E-POSTA GÖNDERME & TASLAK OLUŞTURMA
# =========================================================================

def eposta_gonder_komut(komut):
    """Sesli e-posta gönderme veya panoya hazır taslak kopyalama"""
    eposta_eslesme = re.search(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', komut)
    alici = eposta_eslesme.group(1) if eposta_eslesme else ""
    
    konu = "J.A.R.V.I.S Bildirimi"
    icerik = "Saygılarımla, J.A.R.V.I.S"
    
    konu_eslesme = re.search(r"['\"](.*?)['\"]\s*konu", komut, re.IGNORECASE)
    if not konu_eslesme:
        konu_eslesme = re.search(r"konu\s*başlıklı\s*['\"](.*?)['\"]", komut, re.IGNORECASE)
    if konu_eslesme:
        konu = konu_eslesme.group(1)

    icerik_eslesme = re.search(r"['\"](.*?)['\"]\s*(?:yaz|içerik|mesaj)", komut, re.IGNORECASE)
    if not icerik_eslesme:
        icerik_eslesme = re.search(r"(?:içeriğinde|mesajında)\s*['\"](.*?)['\"]", komut, re.IGNORECASE)
    if icerik_eslesme:
        icerik = icerik_eslesme.group(1)
    elif not alici:
        return "E-posta göndermek için lütfen bir alıcı adresi belirtin efendim. Örneğin: 'ahmet@mail.com adresine mail at'."

    gmail_adres = ayar_getir("gmail_adres", "")
    gmail_sifre = ayar_getir("gmail_sifre", "")

    if gmail_adres and gmail_sifre and alici:
        try:
            msg = MIMEMultipart()
            msg['From'] = gmail_adres
            msg['To'] = alici
            msg['Subject'] = konu
            msg.attach(MIMEText(icerik, 'plain', 'utf-8'))
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(gmail_adres, gmail_sifre)
                server.send_message(msg)
            return f"E-posta başarıyla {alici} adresine gönderildi efendim."
        except Exception as e:
            return f"E-posta gönderimi başarısız oldu: {e}"
    else:
        taslak = f"Kime: {alici or '[Belirtilmedi]'}\nKonu: {konu}\n\nİçerik:\n{icerik}"
        panoya_kopyala(taslak)
        return (f"E-posta taslağınız oluşturuldu ve panonuza kopyalandı efendim. "
                f"Otomatik gönderim yapabilmem için veritabanı ayarlarınıza Gmail adresinizi ve uygulama şifrenizi tanımlayabilirsiniz.")

# =========================================================================
# 🧹 MASAÜSTÜ TEMİZLİĞİ VE OTOMATİK ORGANİZASYON
# =========================================================================

def masaustu_duzenle():
    """Masaüstündeki dağınık dosyaları kategorilerine göre klasörlere toplar"""
    masaustu = os.path.join(os.path.expanduser("~"), "Desktop")
    if not os.path.exists(masaustu):
        return "Masaüstü dizinine ulaşılamadı efendim."

    kategoriler = {
        "Resimler": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".ico"],
        "Belgeler": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".xls", ".pptx", ".csv", ".epub"],
        "Kurulumlar ve Arşivler": [".exe", ".msi", ".zip", ".rar", ".7z", ".tar", ".gz", ".iso"],
        "Medya": [".mp3", ".wav", ".mp4", ".mkv", ".mov", ".avi", ".m4a"],
        "Kod Dosyaları": [".py", ".js", ".html", ".css", ".json", ".cpp", ".c", ".java", ".sql", ".sh", ".bat"]
    }

    tasinan = 0
    try:
        for dosya in os.listdir(masaustu):
            tam_yol = os.path.join(masaustu, dosya)
            if os.path.isdir(tam_yol):
                continue
            if dosya.lower().endswith(".lnk") or dosya.lower() == "desktop.ini":
                continue
            if dosya.lower().startswith("jarvis"):
                continue

            uzanti = os.path.splitext(dosya)[1].lower()
            hedef_kategori = None
            for kat, uzantilar in kategoriler.items():
                if uzanti in uzantilar:
                    hedef_kategori = kat
                    break

            if hedef_kategori:
                hedef_klasor = os.path.join(masaustu, hedef_kategori)
                os.makedirs(hedef_klasor, exist_ok=True)
                hedef_dosya = os.path.join(hedef_klasor, dosya)
                shutil.move(tam_yol, hedef_dosya)
                tasinan += 1

        if tasinan > 0:
            return f"Masaüstünüz organize edildi efendim. Toplam {tasinan} dosya ilgili kategorilerine ayrıldı."
        else:
            return "Masaüstünüz zaten tamamen düzenli görünüyor efendim."
    except Exception as e:
        return f"Masaüstü düzenlenirken bir aksaklık oldu: {e}"

# =========================================================================
# 📂 SON İNDİRİLENİ BUL & AÇ
# =========================================================================

def son_indirilen_dosya(acilsin_mi=False):
    """İndirilenler klasöründeki en son dosyayı bulur ve isteğe bağlı açar"""
    indirilenler = os.path.join(os.path.expanduser("~"), "Downloads")
    if not os.path.exists(indirilenler):
        return "İndirilenler klasörüne ulaşılamadı efendim."

    try:
        dosyalar = []
        for f in os.listdir(indirilenler):
            tam_yol = os.path.join(indirilenler, f)
            if os.path.isfile(tam_yol):
                if f.endswith(('.crdownload', '.tmp', '.part')):
                    continue
                dosyalar.append(tam_yol)

        if not dosyalar:
            return "İndirilenler klasöründe dosya bulunamadı efendim."

        son_dosya = max(dosyalar, key=os.path.getmtime)
        dosya_adi = os.path.basename(son_dosya)
        boyut_mb = os.path.getsize(son_dosya) / (1024 * 1024)

        if acilsin_mi:
            os.startfile(son_dosya)
            return f"Son indirdiğiniz dosya: {dosya_adi}. Boyutu: {boyut_mb:.1f} megabayt. Dosya açılıyor efendim."
        else:
            return f"Son indirdiğiniz dosya: {dosya_adi}, boyutu: {boyut_mb:.1f} megabayt efendim."
    except Exception as e:
        return f"İndirilen dosya tespit edilemedi: {e}"

# =========================================================================
# ▶️ YOUTUBE ARAMA & OYNATMA
# =========================================================================

def youtube_arama_oynat(komut):
    """YouTube üzerinde doğrudan arama yapar ve videoyu açar"""
    temiz = komut.lower()
    for at in ["youtube'da ara", "youtube'da aç", "youtube'da çal", "youtube'da izle", "youtube'da", "youtube aç", "youtube ara", "youtube çal", "youtube"]:
        temiz = temiz.replace(at, "")
    for at in ["videosunu aç", "şarkısını aç", "aç", "oynat", "dinle", "çal"]:
        temiz = temiz.replace(at, "")
    sorgu = temiz.strip()

    if sorgu:
        url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(sorgu)}"
        webbrowser.open_new_tab(url)
        return f"YouTube'da '{sorgu}' açılıyor efendim."
    else:
        webbrowser.open_new_tab("https://www.youtube.com")
        return "YouTube ana sayfası açılıyor efendim."

# =========================================================================
# 🎯 ODAKLANMA MODU (FOCUS MODE)
# =========================================================================

def odaklanma_modu_degistir(aktif=True):
    """Odaklanma modu: Discord'u kapatır, Lo-fi çalar, parlaklığı %40 yapar, VS Code açar"""
    if aktif:
        os.system("taskkill /F /IM Discord.exe /T 2>nul")
        parlaklik_ayarla("parlaklığı 40 yap")
        spotify_komut_isle("lofi beats çal")
        os.system("start code 2>nul")
        tema_uygula("stealth")
        return "Odaklanma modu aktif edildi efendim. Discord kapatıldı, Lo-fi müzik başlatıldı, parlaklık %40 seviyesine ayarlandı ve Stealth teması uygulandı. Verimli çalışmalar dilerim."
    else:
        parlaklik_ayarla("parlaklığı 80 yap")
        tema_uygula("varsayilan")
        return "Odaklanma modundan çıkıldı efendim. Sistem normal parametrelere döndürüldü."

# =========================================================================
# 🧠 MİNİ BİLGİ YARIŞMASI (TRIVIA)
# =========================================================================

TRIVIA_STATE = {"aktif": False, "soru": "", "cevap": "", "puan": 0, "soru_sayisi": 0}

def trivia_isle(komut):
    """Mini Bilgi Yarışması Motoru"""
    global TRIVIA_STATE
    if not TRIVIA_STATE["aktif"]:
        TRIVIA_STATE = {"aktif": True, "soru": "", "cevap": "", "puan": 0, "soru_sayisi": 1}
        prompt = (
            "Bana genel kültür veya coğrafya hakkında tek bir kısa soru ve doğru cevabını şu formatta üret (kurgusal film evrenleri hariç):\n"
            "SORU: [Soru metni]\nCEVAP: [Doğru cevap]"
        )
        ai_resp = yapay_zeka_sor(prompt)
        soru_match = re.search(r"SORU:\s*(.*?)(?:CEVAP:|$)", ai_resp, re.DOTALL)
        cevap_match = re.search(r"CEVAP:\s*(.*?)$", ai_resp, re.DOTALL)
        if soru_match and cevap_match:
            TRIVIA_STATE["soru"] = soru_match.group(1).strip()
            TRIVIA_STATE["cevap"] = cevap_match.group(1).strip()
        else:
            TRIVIA_STATE["soru"] = "Güneş sistemindeki en büyük gezegen hangisidir?"
            TRIVIA_STATE["cevap"] = "Jüpiter"
        return f"1. Soru: {TRIVIA_STATE['soru']}"
    else:
        prompt = (
            f"Kullanıcının cevabı doğru mu? "
            f"Soru: {TRIVIA_STATE['soru']} | Doğru Cevap: {TRIVIA_STATE['cevap']} | Kullanıcı: {komut}. "
            f"Sadece tek kısa cümle ile 'Doğru!' veya 'Yanlış, doğru cevap {TRIVIA_STATE['cevap']} idi.' şeklinde yanıt ver."
        )
        degerlendirme = yapay_zeka_sor(prompt)
        if "doğru" in degerlendirme.lower() and "yanlış" not in degerlendirme.lower()[:15]:
            TRIVIA_STATE["puan"] += 10
        TRIVIA_STATE["soru_sayisi"] += 1
        
        if TRIVIA_STATE["soru_sayisi"] > 3:
            toplam_puan = TRIVIA_STATE["puan"]
            TRIVIA_STATE["aktif"] = False
            return f"{degerlendirme} Yarışma bitti. Toplam puanınız: {toplam_puan}/30."
        else:
            prompt2 = (
                "Bana genel kültür veya coğrafya hakkında tek bir kısa soru ve cevabını şu formatta üret (kurgusal evrenler hariç):\n"
                "SORU: [Soru metni]\nCEVAP: [Doğru cevap]"
            )
            ai_resp2 = yapay_zeka_sor(prompt2)
            soru_m = re.search(r"SORU:\s*(.*?)(?:CEVAP:|$)", ai_resp2, re.DOTALL)
            cevap_m = re.search(r"CEVAP:\s*(.*?)$", ai_resp2, re.DOTALL)
            if soru_m and cevap_m:
                TRIVIA_STATE["soru"] = soru_m.group(1).strip()
                TRIVIA_STATE["cevap"] = cevap_m.group(1).strip()
            else:
                TRIVIA_STATE["soru"] = "Türkiye'nin başkenti neresidir?"
                TRIVIA_STATE["cevap"] = "Ankara"
            return f"{degerlendirme} {TRIVIA_STATE['soru_sayisi']}. Soru: {TRIVIA_STATE['soru']}"

# =========================================================================
# 🎲 TAŞ-KAĞIT-MAKAS MİNİ OYUNU
# =========================================================================

def tas_kagit_makas_oyna(hamle):
    """Taş Kağıt Makas mini oyunu"""
    secenekler = ["taş", "kağıt", "makas"]
    jarvis_secim = random.choice(secenekler)
    h = hamle.lower()
    kullanici_secim = "taş" if "taş" in h else ("kağıt" if "kağıt" in h else ("makas" if "makas" in h else ""))
    if not kullanici_secim:
        return "Taş, kağıt veya makas seçmelisiniz efendim."
    
    if kullanici_secim == jarvis_secim:
        return f"Ben de {jarvis_secim} seçtim, berabere kaldık."
    elif (kullanici_secim == "taş" and jarvis_secim == "makas") or \
         (kullanici_secim == "kağıt" and jarvis_secim == "taş") or \
         (kullanici_secim == "makas" and jarvis_secim == "kağıt"):
        return f"Ben {jarvis_secim} seçtim, siz {kullanici_secim} seçtiniz. Siz kazandınız {KULLANICI_ADI}."
    else:
        return f"Ben {jarvis_secim} seçtim, {jarvis_secim.capitalize()} {kullanici_secim} hamlesini yener. Ben kazandım {KULLANICI_ADI}."

# =========================================================================
# 📈 CANLI KRİPTO & DÖVİZ ALARMI
# =========================================================================

KRIPTO_ALARMLAR = []

def kripto_alarm_isle(komut):
    """Canlı kripto veya altın fiyat alarmı kurar"""
    global KRIPTO_ALARMLAR
    hedef_match = re.search(r'(\d+[\.,]?\d*)', komut)
    if not hedef_match:
        return "Alarm kurabilmem için lütfen hedef bir fiyat belirtin efendim. Örneğin: 'Bitcoin 65000 olursa haber ver'."
    
    hedef_fiyat = float(hedef_match.group(1).replace(',', '.'))
    kripto_id = "bitcoin" if "bitcoin" in komut or "btc" in komut else ("ethereum" if "ethereum" in komut or "eth" in komut else "bitcoin")
    yon = "alti" if any(k in komut for k in ["düşerse", "altına", "altında", "inirse"]) else "ustu"
    
    alarm = {"kripto": kripto_id, "hedef": hedef_fiyat, "yon": yon, "tetiklendi": False}
    KRIPTO_ALARMLAR.append(alarm)
    yon_metin = "altına düşerse" if yon == "alti" else "üzerine çıkarsa"
    return f"{kripto_id.capitalize()} için {hedef_fiyat:,.0f} Dolar {yon_metin} alarmı kuruldu efendim. Takipteyim."

def _kripto_alarm_kontrol_dongusu():
    """Arka planda dakikada bir kripto fiyatlarını kontrol eder"""
    while running:
        time.sleep(60)
        if not KRIPTO_ALARMLAR:
            continue
        try:
            res = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd", timeout=5).json()
            for alarm in KRIPTO_ALARMLAR:
                if alarm["tetiklendi"]:
                    continue
                kripto = alarm["kripto"]
                anlik = res.get(kripto, {}).get("usd")
                if not anlik:
                    continue
                tetiklendi = False
                if alarm["yon"] == "alti" and anlik <= alarm["hedef"]:
                    tetiklendi = True
                elif alarm["yon"] == "ustu" and anlik >= alarm["hedef"]:
                    tetiklendi = True
                
                if tetiklendi:
                    alarm["tetiklendi"] = True
                    sesli_konus(f"Piyasa Alarmı {KULLANICI_ADI}! {kripto.capitalize()} hedeflediğiniz {alarm['hedef']:,.0f} Dolar seviyesine ulaştı. Güncel fiyat: ${anlik:,.0f}.")
        except Exception:
            pass

# =========================================================================
# 🎤 MİKROFON 'DİKKATE AL' / SAĞIR MODU DURUMU
# =========================================================================

mikrofon_dikkate_alinsin_mi = True
mikrofon_btn_pencere = None

def mikrofon_modu_degistir(durum=None):
    """Mikrofon dinleme (dikkate alma) durumunu açar veya kapatır"""
    global mikrofon_dikkate_alinsin_mi
    if durum is None:
        mikrofon_dikkate_alinsin_mi = not mikrofon_dikkate_alinsin_mi
    else:
        mikrofon_dikkate_alinsin_mi = durum

    if mikrofon_dikkate_alinsin_mi:
        durum_guncelle("BEKLEMEDE")
        log_mesaj("🎙️ Mikrofon aktif: Jarvis sizi dinliyor ve dikkate alıyor.", "jarvis")
        if mikrofon_btn_pencere and simdiki_mod == "pencere":
            try:
                mikrofon_btn_pencere.configure(text="🎙️ MİKROFON: AÇIK", bg="#00aa44")
            except Exception: pass
    else:
        durum_guncelle("SAĞIR")
        konusmayi_kes()
        log_mesaj("🔇 Sağır Modu: Jarvis mikrofonu kapattı. 'Jarvis dikkate al' diyene kadar sizi dinlemeyecek.", "info")
        if mikrofon_btn_pencere and simdiki_mod == "pencere":
            try:
                mikrofon_btn_pencere.configure(text="🔇 MİKROFON: SAĞIR MODU", bg="#aa2222")
            except Exception: pass

def dikkate_al_mi_kontrol(metin):
    """Sağır modundayken kilit açma kelimelerini kontrol eder"""
    if not metin:
        return False
    kilit_acma = [
        "dikkate al", "beni dinle", "mikrofonu aç", "mikrofonu ac", 
        "uyan", "jarvis uyan", "jarvis beni dinle", "jarvis dikkate al"
    ]
    return any(k in metin.lower() for k in kilit_acma)

# =========================================================================
# 🎯 ANA KOMUT İŞLEME MERKEZİ (GENİŞLETİLMİŞ NİYET ANALİZİ)
# =========================================================================

def komut_isle(komut):
    """Gelen komutu semantik eş anlamlılar ve niyetlerle çözer"""
    global KULLANICI_ADI, TRIVIA_STATE
    if not komut or komut in ["anlasilamadi", "zaman_asimi", "hata"]:
        return True

    # --- -1. MİNİ BİLGİ YARIŞMASI AKTİFSE CEVAP İŞLE ---
    if TRIVIA_STATE["aktif"]:
        if niyet_kontrol(komut, ["yarışmayı bitir", "yarışmayı kapat", "oyunu durdur", "çık", "pes ediyorum", "iptal", "yeter", "pes"]):
            TRIVIA_STATE["aktif"] = False
            sesli_konus("Bilgi yarışması sonlandırıldı efendim.")
            return True
        cevap = trivia_isle(komut)
        sesli_konus(cevap)
        return True

    # --- 0. MİKROFON AÇMA / KAPAMA & DİKKATE AL MODU ---
    if niyet_kontrol(komut, ["beni dinleme", "mikrofonu kapat", "mikrofonu kapatsana", "sağır modu", "dinlemeyi durdur", "dikkate alma", "sus artik", "beni duyma"]):
        mikrofon_modu_degistir(False)
        sesli_konus("Mikrofon kapatıldı efendim. Tekrar ihtiyacınız olduğunda 'Jarvis dikkate al' veya 'Jarvis mikrofonu aç' demeniz yeterlidir.")
        return "sohbeti_bitir"

    elif niyet_kontrol(komut, ["dikkate al", "beni dinle", "mikrofonu aç", "mikrofonu ac", "jarvis dikkate al", "jarvis beni dinle"]):
        mikrofon_modu_degistir(True)
        sesli_konus("Sizi dinliyorum ve dikkate alıyorum efendim, buyrun.")
        return True

    # --- 1. SOHBETİ DURDURMA / UYKUYA ALMA ---
    elif niyet_kontrol(komut, ["tamamdır", "dinlen", "uykuya geç", "uyku modu", "sus", "sessiz ol", "sessiz kal", "yeterli", "şimdilik bu kadar"]) or komut.strip() in ["tamam", "kapat", "dur"]:
        sesli_konus("Emredersiniz efendim. İhtiyacınız olduğunda seslenmeniz yeterli.")
        return "sohbeti_bitir"

    # --- 2. SELAMLAMA VE DURUM ---
    elif niyet_kontrol(komut, ["merhaba", "selam", "günaydın", "iyi günler", "tünaydın", "iyi akşamlar", "orada mısın"]):
        saat = datetime.datetime.now().hour
        vakit = "Günaydın" if saat < 12 else ("İyi günler" if saat < 18 else "İyi akşamlar")
        sesli_konus(f"{vakit} {KULLANICI_ADI}! Sistemler tam kapasite devrede, sizi dinliyorum.")

    elif niyet_kontrol(komut, ["nasılsın", "durumun nasıl", "keyifler nasıl", "ne haber"]):
        sesli_konus(f"Gayet iyiyim {KULLANICI_ADI}, tüm sistemler sorunsuz çalışıyor. Sizi dinliyorum.")

    # --- 3. SAAT VE TARİH ---
    elif niyet_kontrol(komut, ["saat kaç", "saati söyle", "zaman nedir"]):
        sesli_konus(f"Saat şu an {datetime.datetime.now().strftime('%H:%M')} efendim.")

    elif niyet_kontrol(komut, ["hangi gün", "bugünün tarihi", "ayın kaçı", "tarih nedir"]):
        sesli_konus(f"Bugün {datetime.datetime.now().strftime('%d %B %Y, %A')} efendim.")

    # --- 4. SES DÜZEYİ AYARLARI (EŞ ANLAMLILAR) ---
    elif niyet_kontrol(komut, ["sesi aç", "sesi yükselt", "ses ver", "duyamıyorum", "sesi kökle", "sesi artır", "sesi kıs", "kulağımı tırmalıyor", "biraz kıs", "kıs şunu", "sessize al", "sustur", "mute"]):
        cevap = ses_ayarla(komut)
        sesli_konus(cevap)

    # --- 5. SPOTIFY & MÜZİK KONTROLÜ ---
    elif niyet_kontrol(komut, ["spotify", "spotidy", "şarkı", "sarkı", "müzik", "muzik", "parça", "parca", "çal", "cal", "oynat", "şarkıyı durdur", "müziği durdur", "müziği kapat", "şarkıyı kapat", "sıradaki", "sonraki parça"]):
        cevap = spotify_komut_isle(komut)
        sesli_konus(cevap)

    # --- 6. PENCERELER & MASAÜSTÜ KONTROLÜ ---
    elif niyet_kontrol(komut, ["pencereleri küçült", "simge durumuna al", "masaüstünü göster", "pencereleri indir", "ekranı temizle"]):
        cevap = pencereleri_simge_yap()
        sesli_konus(cevap)

    elif niyet_kontrol(komut, ["masaüstünü düzenle", "masaüstünü temizle", "masaüstünü toparla", "masaüstü temizliği", "dosyaları düzenle", "dağınıklığı topla"]):
        cevap = masaustu_duzenle()
        sesli_konus(cevap)

    elif niyet_kontrol(komut, ["son indirdiğim dosyayı aç", "son indirilen dosyayı aç", "son indirdiğimi aç", "son ineni aç"]):
        cevap = son_indirilen_dosya(acilsin_mi=True)
        sesli_konus(cevap)

    elif niyet_kontrol(komut, ["son indirdiğim dosya", "son indirilen dosya", "en son ne indirdim", "son indirilen ne"]):
        cevap = son_indirilen_dosya(acilsin_mi=False)
        sesli_konus(cevap)

    elif niyet_kontrol(komut, ["masaüstü klasörü", "masaüstünü aç"]):
        os.startfile(os.path.join(os.environ['USERPROFILE'], 'Desktop'))
        sesli_konus("Masaüstü dosya gezgininde açıldı.")

    elif niyet_kontrol(komut, ["indirilenler", "downloads"]):
        os.startfile(os.path.join(os.environ['USERPROFILE'], 'Downloads'))
        sesli_konus("İndirilenler klasörü açıldı efendim.")

    # --- 7. EKRAN GÖRÜNTÜSÜ ALMA (SS) ---
    elif niyet_kontrol(komut, ["ekran resmi çek", "ss al", "ekran görüntüsü", "ekranın fotoğrafını çek", "screenshot"]):
        cevap = ekran_goruntusu_al()
        sesli_konus(cevap)

    # --- 8. SİSTEM BİLGİSİ & DONANIM ---
    elif niyet_kontrol(komut, ["sistem durumu", "sistem bilgisi", "cpu", "ram", "işlemci durumu", "makine nasıl"]):
        cevap = sistem_durumu()
        sesli_konus(cevap)

    # --- 9. OYUN & VALORANT ---
    elif niyet_kontrol(komut, ["valo aç", "valorant gir", "valorant", "oyun vakti", "oyuna girelim"]):
        cevap = valorant_otomatik_giris()
        sesli_konus(cevap)

    elif niyet_kontrol(komut, ["oyun modu", "discord kapat"]):
        os.system("taskkill /IM discord.exe /F 2>nul")
        sesli_konus("Oyun modu aktif. Discord ve arka plan servisleri durduruldu efendim.")

    # --- 9.1 ODAKLANMA MODU (FOCUS MODE) ---
    elif niyet_kontrol(komut, ["odaklanma modunu aç", "odaklanma modu", "çalışma modunu aç", "çalışma modu", "focus mode", "odaklan", "konsantre ol"]):
        cevap = odaklanma_modu_degistir(True)
        sesli_konus(cevap)

    elif niyet_kontrol(komut, ["odaklanma modunu kapat", "odaklanma modunu bitir", "normal moda dön", "normal mod", "odaklanmayı kapat"]):
        cevap = odaklanma_modu_degistir(False)
        sesli_konus(cevap)

    # --- 9.2 YEREL DOSYA OKUMA & ÖZETLEME (PDF, DOCX, TXT) ---
    elif niyet_kontrol(komut, ["dosyasını oku", "dosyasını özetle", "belgesini oku", "belgesini özetle", "dosyayı oku", "dosyayı özetle", "belgeyi oku", "belgeyi özetle", "oku ve özetle", "dosya oku"]):
        cevap = dosya_oku_ve_ozetle(komut)
        sesli_konus(cevap)

    # --- 9.3 SESLİ E-POSTA GÖNDERME ---
    elif niyet_kontrol(komut, ["mail at", "e-posta gönder", "eposta gönder", "mail gönder", "e-posta yolla", "mail yolla", "e-posta at"]):
        cevap = eposta_gonder_komut(komut)
        sesli_konus(cevap)

    # --- 9.4 CANLI KRİPTO & FİYAT ALARMI ---
    elif niyet_kontrol(komut, ["alarmı kur", "alarm kur", "düşerse haber ver", "çıkarsa haber ver", "olursa haber ver", "kripto alarmı", "bitcoin alarmı"]):
        cevap = kripto_alarm_isle(komut)
        sesli_konus(cevap)

    # --- 10. GOOGLE CHROME & İNTERNETTE ARAMA ---
    elif niyet_kontrol(komut, ["google'da ara", "googleda ara", "google'da", "chrome'da ara", "internette ara", "arama yap"]):
        cevap = chrome_arama_yap(komut)
        sesli_konus(cevap)

    elif niyet_kontrol(komut, ["yeni sekme aç", "yeni sekme", "yeni sayfa aç", "yeni sayfa", "chrome aç", "tarayıcıyı aç"]):
        cevap = chrome_yeni_sekme()
        sesli_konus(cevap)

    elif niyet_kontrol(komut, ["sekmeyi kapat", "sayfayı kapat", "sekmeyi kapa"]):
        cevap = chrome_sekme_kapat()
        sesli_konus(cevap)

    # --- 11. TELEFON EKRANI (SCRCPY) ---
    elif niyet_kontrol(komut, ["telefonu bağla", "telefon ekranı", "ekranı yansıt", "scrcpy", "telefonu yansıt"]):
        if os.path.exists(SCRCPY_YOLU):
            os.system(f'start "" "{SCRCPY_YOLU}"')
            sesli_konus("Scrcpy başlatılıyor, telefon ekranınız aktarılıyor efendim.")
        else:
            sesli_konus("Scrcpy yolu bulunamadı efendim, lütfen yapılandırmayı kontrol edin.")

    # --- 11. DÖVİZ & FİNANS ---
    elif niyet_kontrol(komut, ["dolar", "euro", "döviz", "bitcoin", "kripto", "fiyatlar"]):
        cevap = doviz_durumu()
        sesli_konus(cevap)

    # --- 12. HAVA DURUMU ---
    elif niyet_kontrol(komut, ["hava durumu", "hava nasıl", "yağmur var mı"]):
        sehir = "Ankara" if "ankara" in komut else ("Izmir" if "izmir" in komut else "Istanbul")
        cevap = hava_durumu_al(sehir)
        sesli_konus(cevap)

    # --- 13. WIKIPEDIA & ANSİKLOPEDİK BİLGİ ---
    elif niyet_kontrol(komut, ["wikipedia'da ara", "wikipediada ara", "wikipedia", "vikipedi", "kimdir", "nedir", "hakkında bilgi ver", "bilgi ver"]):
        cevap = wikipedia_ozet_al(komut)
        sesli_konus(cevap)

    # --- 14. PANO KONTROLÜ (CLIPBOARD ASSISTANT) ---
    elif niyet_kontrol(komut, ["panoyu oku", "panoda ne var", "kopyalanan metin", "kopyaladığım metin", "panoyu seslendir"]):
        cevap = panoyu_oku()
        sesli_konus(cevap)

    # --- 15. DİNAMİK SAYAÇ & POMODORO ---
    elif niyet_kontrol(komut, ["sayaç kur", "dakika sonra haber ver", "saniye sonra haber ver", "zamanlayıcı kur", "pomodoro"]):
        sure = 25 * 60  # varsayılan 25 dk
        etiket = "Sayaç"
        kelimeler = komut.split()
        for i, kelime in enumerate(kelimeler):
            if kelime.isdigit():
                sayi = int(kelime)
                if i + 1 < len(kelimeler):
                    if "saniye" in kelimeler[i + 1]:
                        sure = sayi
                        etiket = f"{sayi} Saniyelik Sayaç"
                    elif "dakika" in kelimeler[i + 1]:
                        sure = sayi * 60
                        etiket = f"{sayi} Dakikalık Sayaç"
                break
        cevap = zamanlayici_baslat(sure, etiket)
        sesli_konus(cevap)

    # --- 16. EKRAN PARLAKLIĞI AYARLARI ---
    elif niyet_kontrol(komut, ["parlaklığı kıs", "parlaklığı yükselt", "parlaklığı artır", "parlaklığı fulle", "parlaklığı yüzde", "ekran parlaklığı"]):
        cevap = parlaklik_ayarla(komut)
        sesli_konus(cevap)

    # --- 17. EĞLENCE, OYUN & MOTİVASYON ---
    elif niyet_kontrol(komut, ["bilgi yarışması", "trivia", "soru sor", "bana soru sor", "yarışma başlat", "yarışma yap"]):
        cevap = trivia_isle(komut)
        sesli_konus(cevap)

    elif niyet_kontrol(komut, ["taş kağıt makas", "benimle taş kağıt makas oyna", "taş mı kağıt mı", "taş seçtim", "kağıt seçtim", "makas seçtim"]) or komut.strip() in ["taş", "kağıt", "makas"]:
        cevap = tas_kagit_makas_oyna(komut)
        sesli_konus(cevap)

    elif niyet_kontrol(komut, ["zar at"]):
        sesli_konus(f"Zar atıldı, gelen sayı: {random.randint(1, 6)}.")

    elif niyet_kontrol(komut, ["yazı tura", "para at"]):
        sesli_konus(f"Para çevrildi: {random.choice(['Yazı', 'Tura'])} geldi efendim.")

    elif niyet_kontrol(komut, ["fıkra anlat", "espri yap", "komik bir şey söyle"]):
        sesli_konus(random.choice(FIKRALAR))

    elif niyet_kontrol(komut, ["motivasyon", "günün sözü", "motive et"]):
        sesli_konus(random.choice(MOTIVASYON_SOZLERI))

    # --- 18. KULLANICI HİTAP VE İSİM DEĞİŞTİRME ---
    elif niyet_kontrol(komut, ["bana patron de", "bana efendim de", "bana tony de", "adımı değiştir", "bana"]):
        yeni_isim = "Efendim"
        if "patron" in komut:
            yeni_isim = "Patron"
        elif "tony" in komut:
            yeni_isim = "Tony"
        elif "bana " in komut and " de" in komut:
            try:
                yeni_isim = komut.split("bana ")[1].split(" de")[0].strip().capitalize()
            except: pass
        KULLANICI_ADI = yeni_isim
        ayar_kaydet("kullanici_adi", yeni_isim)
        sesli_konus(f"Anlaşıldı, bundan sonra size '{yeni_isim}' olarak hitap edeceğim.")

    # --- 19. GÜVENLİK, ANLIK ŞİFRE & PANOYA KOPYALAMA ---
    elif niyet_kontrol(komut, ["şifre üret", "parola oluştur", "güçlü şifre", "şifre oluştur", "parola üret"]):
        uzunluk = 16
        uzunluk_match = re.search(r'(\d+)\s*karakter', komut)
        if uzunluk_match:
            uzunluk = max(6, min(64, int(uzunluk_match.group(1))))
        karakterler = string.ascii_letters + string.digits + "!@#$%^&*"
        sifre = ''.join(secrets.choice(karakterler) for _ in range(uzunluk))
        panoya_kopyala(sifre)
        sesli_konus(f"{uzunluk} karakterlik yüksek güvenlikli şifreniz oluşturuldu ve otomatik panonuza kopyalandı efendim.")
        log_mesaj(f"🔐 Üretilen Şifre ({uzunluk} Karakter): {sifre} (Panoya kopyalandı)", "jarvis")

    # --- 20. PENCERE KAPATMA & ALT+F4 ---
    elif niyet_kontrol(komut, ["bu pencereyi kapat", "pencereyi kapat", "alt f4 yap", "uygulamayı sonlandır"]):
        if PYAUTOGUI_VAR:
            pyautogui.hotkey('alt', 'f4')
            sesli_konus("Pencere kapatıldı efendim.")
        else:
            sesli_konus("Bu işlem gerçekleştirilemedi.")

    # --- 21. SİSTEM KAPATMA, YENİDEN BAŞLATMA & İPTAL ---
    elif niyet_kontrol(komut, ["kapatmayı iptal et", "kapatma iptal", "iptal et"]):
        os.system("shutdown /a")
        sesli_konus("Sistem kapatma zamanlayıcısı iptal edildi efendim. Güvendeyiz.")

    elif niyet_kontrol(komut, ["yeniden başlat", "bilgisayarı yeniden başlat", "reset at"]):
        sesli_konus("Bilgisayarınız 15 saniye içinde yeniden başlatılacak efendim.")
        os.system("shutdown /r /t 15")

    elif niyet_kontrol(komut, ["ekranı kilitle", "bilgisayarı kilitle", "kilitle"]):
        sesli_konus("Terminal kilitleniyor efendim.")
        os.system("rundll32.exe user32.dll,LockWorkStation")

    elif niyet_kontrol(komut, ["bilgisayarı kapat", "pc kapat", "fişi çek", "sistemi kapat"]):
        sesli_konus("Sistem 15 saniye içinde kapatılacak efendim. İptal etmek için 'Kapatmayı iptal et' diyebilirsiniz.")
        os.system("shutdown /s /t 15")

    # --- 22. YOUTUBE ENTEGRASYONU, NOT DEFTERİ, HESAP MAKİNESİ ---
    elif niyet_kontrol(komut, ["youtube'da", "youtubeda", "youtube'dan", "youtube aç", "youtube ara", "youtube çal", "youtube"]):
        cevap = youtube_arama_oynat(komut)
        sesli_konus(cevap)

    elif niyet_kontrol(komut, ["not defteri", "notepad"]):
        os.system("start notepad.exe")
        sesli_konus("Not defteri açıldı.")

    elif niyet_kontrol(komut, ["hesap makinesi", "calculator"]):
        os.system("start calc.exe")
        sesli_konus("Hesap makinesi açıldı.")

    # --- 23. AYARLAR & YAPILANDIRMA PENCERESİ ---
    elif niyet_kontrol(komut, ["ayarları aç", "ayar penceresi", "yapılandırma", "ayarlar", "kimlik ayarları"]):
        if root:
            root.after(100, ayarlar_penceresi_ac)
        sesli_konus("Yapılandırma ve ayarlar penceresi açıldı efendim.")

    # --- 17. TEMA DEĞİŞTİRME ---
    elif niyet_kontrol(komut, ["tema değiştir", "kırmızı tema", "yeşil tema", "mor tema", "varsayılan tema"]):
        if "kırmızı" in komut:
            tema_uygula("mark_vii")
        elif "yeşil" in komut:
            tema_uygula("stealth")
        elif "mor" in komut:
            tema_uygula("hulkbuster")
        elif "midnight" in komut or "mavi" in komut:
            tema_uygula("midnight")
        else:
            tema_uygula("varsayilan")
        sesli_konus("HUD görsel arayüz teması güncellendi efendim.")

    # --- 18. GROQ LLAMA 3.1 70B YAPAY ZEKA FALLBACK ---
    else:
        durum_guncelle("İŞLENİYOR")
        cevap = yapay_zeka_sor(komut)
        sesli_konus(cevap)
        gecmis_kaydet(komut, cevap)

    return True

# =========================================================================
# 🎨 IRON MAN HUD ARAYÜZ MOTORU (TKINTER MODERN ENGINE)
# =========================================================================

root = None
canvas = None
info_label = None
durum_label = None
simdiki_mod = ""  # Başlangıçta boş olmalı ki mod_degistir('kure') tetiklensin!
animasyon_acisi = 0
running = True
log_listesi = []
son_mesaj = ""
sohbet_aktif = False

# Pencere Modu Bileşenleri
pencere_anim_canvas = None
log_text = None
notlar_text = None
durum_pencere_label = None
saat_pencere_label = None
komut_entry = None
cpu_label = None
ram_label = None
pil_label = None

_daktilo_kuyrugu = []
_daktilo_calisiyor = False

def _daktilo_adim():
    global _daktilo_calisiyor, _daktilo_kuyrugu
    if not _daktilo_kuyrugu or not log_text or simdiki_mod != "pencere":
        _daktilo_calisiyor = False
        return
    karakter, tag_adi = _daktilo_kuyrugu.pop(0)
    try:
        log_text.configure(state='normal')
        log_text.insert('end', karakter, tag_adi)
        log_text.see('end')
        log_text.configure(state='disabled')
    except Exception:
        _daktilo_calisiyor = False
        return

    if _daktilo_kuyrugu and root:
        root.after(8, _daktilo_adim)
    else:
        _daktilo_calisiyor = False

def log_mesaj(mesaj, tip="info"):
    """Konsol geçmişine ve arayüze mesaj yazar (Fütüristik Daktilo Efekti Destekli)"""
    global son_mesaj, _daktilo_calisiyor, _daktilo_kuyrugu
    son_mesaj = mesaj
    zaman = datetime.datetime.now().strftime("%H:%M")
    log_listesi.append({"mesaj": mesaj, "tip": tip, "zaman": zaman})
    if len(log_listesi) > 60:
        log_listesi.pop(0)

    if simdiki_mod == "pencere" and log_text:
        try:
            renk = TEMALAR[simdiki_tema]["ana"] if tip == "jarvis" else (TEMALAR[simdiki_tema]["ikincil"] if tip == "user" else "#888888")
            log_text.tag_config(tip, foreground=renk)

            if tip == "jarvis" and root:
                log_text.configure(state='normal')
                if _daktilo_kuyrugu:
                    kalan_metin = "".join(k for k, _ in _daktilo_kuyrugu)
                    log_text.insert('end', kalan_metin, "jarvis")
                    _daktilo_kuyrugu.clear()
                
                log_text.insert('end', f"[{zaman}] ", "jarvis_time")
                log_text.tag_config("jarvis_time", foreground="#557799")
                log_text.configure(state='disabled')

                for ch in mesaj + "\n":
                    _daktilo_kuyrugu.append((ch, tip))
                if not _daktilo_calisiyor:
                    _daktilo_calisiyor = True
                    root.after(10, _daktilo_adim)
            else:
                log_text.configure(state='normal')
                if _daktilo_kuyrugu:
                    kalan_metin = "".join(k for k, _ in _daktilo_kuyrugu)
                    log_text.insert('end', kalan_metin, "jarvis")
                    _daktilo_kuyrugu.clear()
                    _daktilo_calisiyor = False
                log_text.insert('end', f"[{zaman}] {mesaj}\n", tip)
                log_text.see('end')
                log_text.configure(state='disabled')
        except Exception:
            pass

def durum_guncelle(durum):
    """HUD durum göstergesini günceller"""
    renk = TEMALAR[simdiki_tema]["ana"]
    if durum == "DİNLİYOR":
        renk = "#00ff88"
    elif durum == "KONUŞUYOR":
        renk = TEMALAR[simdiki_tema]["ikincil"]
    elif durum == "İŞLENİYOR":
        renk = "#ff00bb"

    if durum_label:
        try:
            durum_label.configure(text=f"● {durum}", fg=renk)
        except Exception:
            pass

    if durum_pencere_label and simdiki_mod == "pencere":
        try:
            durum_pencere_label.configure(text=f"● SİSTEM DURUMU: {durum}", fg=renk)
        except Exception:
            pass

def tema_uygula(tema_adi):
    """Temayı hem küre hem pencere moduna uygular"""
    global simdiki_tema
    if tema_adi in TEMALAR:
        simdiki_tema = tema_adi
        t = TEMALAR[simdiki_tema]
        if simdiki_mod == "pencere" and root:
            root.configure(bg=t["arka"])
        log_mesaj(f"🎨 HUD Teması: {t['ad']}", "jarvis")

# =========================================================================
# 🔵 ARK REAKTÖRÜ ANİMASYONU (FÜTÜRİSTİK PLAZMA EFEKTLERİ)
# =========================================================================

parcaciklar = []
for i in range(20):
    parcaciklar.append({
        'aci': (360 / 20) * i,
        'yaricap': 65,
        'hiz': random.uniform(0.8, 2.5),
        'boyut': random.uniform(1.2, 2.8)
    })

def reaktor_ciz(cv, cx, cy, yaricap, durum):
    """Tek bir canvas üzerine Iron Man Arc Reactor çizer"""
    global animasyon_acisi
    t = TEMALAR[simdiki_tema]
    ana = t["ana"]
    ikincil = t["ikincil"]
    glow = t["glow"]

    hiz = 4 if durum == "DİNLİYOR" else (6 if durum == "KONUŞUYOR" else 1.8)
    animasyon_acisi = (animasyon_acisi + hiz) % 360

    # Dış dönen segmentler (Holografik halka 1)
    r1 = yaricap * 0.95
    for i in range(4):
        cv.create_arc(cx - r1, cy - r1, cx + r1, cy + r1,
                      start=animasyon_acisi + (i * 90), extent=55,
                      outline=ana, width=3, style="arc")

    # Ters dönen iç halka (Halka 2)
    r2 = yaricap * 0.72
    for i in range(8):
        cv.create_arc(cx - r2, cy - r2, cx + r2, cy + r2,
                      start=-animasyon_acisi * 1.4 + (i * 45), extent=22,
                      outline=ikincil, width=2, style="arc")

    # İç çekirdek rezonatör halkası (Halka 3)
    r3 = yaricap * 0.48
    for i in range(12):
        cv.create_arc(cx - r3, cy - r3, cx + r3, cy + r3,
                      start=animasyon_acisi * 2.2 + (i * 30), extent=12,
                      outline=ana, width=1.5, style="arc")

    # Dönen plazma parçacıkları
    for p in parcaciklar:
        p['aci'] = (p['aci'] + p['hiz']) % 360
        rad = math.radians(p['aci'])
        pr = r1 * 0.85
        px = cx + pr * math.cos(rad)
        py = cy + pr * math.sin(rad)
        s = p['boyut']
        cv.create_oval(px - s, py - s, px + s, py + s, fill=glow, outline="")

    # Plazma nabız çekirdeği (Jarvis konuştuğunda reaktif büyür)
    pulse_taban = yaricap * 0.22
    pulse_dalga = (yaricap * 0.12) if durum == "KONUŞUYOR" else ((yaricap * 0.08) if durum == "DİNLİYOR" else (yaricap * 0.04))
    pulse = pulse_taban + pulse_dalga * math.sin(math.radians(animasyon_acisi * 4))

    # Glow haleleri
    for offset in [8, 4]:
        cv.create_oval(cx - pulse - offset, cy - pulse - offset,
                       cx + pulse + offset, cy + pulse + offset,
                       outline=ana, width=1)

    # Merkez plazma
    cv.create_oval(cx - pulse, cy - pulse, cx + pulse, cy + pulse, fill=ana, outline="")
    cv.create_oval(cx - pulse * 0.65, cy - pulse * 0.65, cx + pulse * 0.65, cy + pulse * 0.65, fill="#ffffff", outline="")

def animasyon_dongusu():
    """Tüm arayüz animasyonlarını tazeleyen ana döngü"""
    if not running:
        return
    try:
        durum = "BEKLEMEDE"
        if ses_caliniyor:
            durum = "KONUŞUYOR"
        elif sohbet_aktif:
            durum = "DİNLİYOR"

        if simdiki_mod == "kure" and canvas:
            canvas.delete("all")
            reaktor_ciz(canvas, 100, 80, 75, durum)
            if info_label and son_mesaj:
                kisa = (son_mesaj[:26] + "...") if len(son_mesaj) > 26 else son_mesaj
                info_label.configure(text=kisa)

        elif simdiki_mod == "pencere" and pencere_anim_canvas:
            pencere_anim_canvas.delete("all")
            reaktor_ciz(pencere_anim_canvas, 100, 100, 90, durum)

    except Exception:
        pass

    if root:
        root.after(16, animasyon_dongusu)

# =========================================================================
# 🔄 MOD DEĞİŞİMİ & PENCERE YÖNETİMİ
# =========================================================================

def mod_degistir(hedef_mod=None):
    """Küre Modu ile Pencere Modu arasında geçiş yapar"""
    global simdiki_mod, canvas, info_label, durum_label
    global pencere_anim_canvas, log_text, notlar_text, durum_pencere_label, saat_pencere_label, komut_entry, cpu_label, ram_label

    if hedef_mod is None:
        hedef_mod = "pencere" if simdiki_mod == "kure" else "kure"

    if simdiki_mod == hedef_mod and len(root.winfo_children()) > 0:
        return

    simdiki_mod = hedef_mod
    t = TEMALAR[simdiki_tema]

    # Mevcut widget'ları temizle
    for w in root.winfo_children():
        w.destroy()

    if simdiki_mod == "pencere":
        # ========== PENCERE MODU (FULL HUD KONSOLU) ==========
        w, h = 1150, 760
        x = (root.winfo_screenwidth() // 2) - (w // 2)
        y = (root.winfo_screenheight() // 2) - (h // 2)
        root.geometry(f"{w}x{h}+{x}+{y}")
        root.overrideredirect(False)
        root.attributes('-topmost', False)
        root.attributes('-transparentcolor', '')
        root.configure(bg=t["arka"])

        # Başlık Çubuğu
        ust_bar = tk.Frame(root, bg=t["arka"], height=55)
        ust_bar.pack(fill='x', padx=15, pady=8)
        
        tk.Label(ust_bar, text="⚡ J.A.R.V.I.S — IRON MAN HUD", fg=t["ana"], bg=t["arka"], font=("Consolas", 20, "bold")).pack(side='left')
        tk.Label(ust_bar, text="STARK INDUSTRIES OS v5.0", fg=t["ikincil"], bg=t["arka"], font=("Consolas", 9)).pack(side='left', padx=12, pady=(8, 0))

        tk.Button(ust_bar, text="🔵 KÜRE MODUNA DÖN", fg="#000000", bg=t["ana"], activebackground=t["ikincil"],
                  font=("Consolas", 10, "bold"), bd=0, padx=14, pady=5, command=lambda: mod_degistir("kure"), cursor="hand2").pack(side='right')

        tk.Button(ust_bar, text="⚙️ AYARLAR", fg="white", bg="#101730", activebackground=t["ana"],
                  font=("Consolas", 10, "bold"), bd=0, padx=12, pady=5, command=ayarlar_penceresi_ac, cursor="hand2").pack(side='right', padx=8)

        # Ana Gövde
        govde = tk.Frame(root, bg=t["arka"])
        govde.pack(fill='both', expand=True, padx=15, pady=5)

        # Sol Panel (Ark Reaktörü ve Sistem Metrikleri)
        sol_panel = tk.Frame(govde, bg=t["panel"], width=280)
        sol_panel.pack(side='left', fill='y', padx=(0, 10))
        sol_panel.pack_propagate(False)

        pencere_anim_canvas = tk.Canvas(sol_panel, width=200, height=200, bg=t["panel"], highlightthickness=0)
        pencere_anim_canvas.pack(pady=10)

        durum_pencere_label = tk.Label(sol_panel, text="● SİSTEM DURUMU: BEKLEMEDE", fg=t["ana"], bg=t["panel"], font=("Consolas", 10, "bold"))
        durum_pencere_label.pack(pady=5)

        saat_pencere_label = tk.Label(sol_panel, text="", fg=t["ana"], bg=t["panel"], font=("Consolas", 18, "bold"))
        saat_pencere_label.pack(pady=4)

        def saat_guncelle():
            if running and simdiki_mod == "pencere" and saat_pencere_label:
                saat_pencere_label.configure(text=datetime.datetime.now().strftime("%H:%M:%S"))
                root.after(1000, saat_guncelle)
        saat_guncelle()

        tk.Frame(sol_panel, bg=t["ana"], height=2).pack(fill='x', padx=15, pady=10)

        # Sistem Göstergeleri
        metrik_frame = tk.Frame(sol_panel, bg=t["panel"])
        metrik_frame.pack(fill='x', padx=15)
        cpu_label = tk.Label(metrik_frame, text="⚡ CPU: Yükleniyor...", fg="#888", bg=t["panel"], font=("Consolas", 9))
        cpu_label.pack(anchor='w', pady=2)
        ram_label = tk.Label(metrik_frame, text="💾 RAM: Yükleniyor...", fg="#888", bg=t["panel"], font=("Consolas", 9))
        ram_label.pack(anchor='w', pady=2)
        pil_label = tk.Label(metrik_frame, text="🔋 Pil: Hesaplanıyor...", fg="#888", bg=t["panel"], font=("Consolas", 9))
        pil_label.pack(anchor='w', pady=2)

        def metrik_tazele():
            if running and simdiki_mod == "pencere" and PSUTIL_VAR and cpu_label:
                try:
                    cpu_label.configure(text=f"⚡ CPU: %{psutil.cpu_percent()}")
                    ram_label.configure(text=f"💾 RAM: %{psutil.virtual_memory().percent}")
                    bat = psutil.sensors_battery()
                    if bat is not None and pil_label:
                        durum_str = "Şarjda" if bat.power_plugged else "Pilde"
                        kalan_str = ""
                        if bat.secsleft > 0 and not bat.power_plugged:
                            saat = bat.secsleft // 3600
                            dakika = (bat.secsleft % 3600) // 60
                            kalan_str = f" ({saat}s {dakika}dk)"
                        pil_label.configure(text=f"🔋 Pil: %{bat.percent}{kalan_str} [{durum_str}]")
                    elif pil_label:
                        pil_label.configure(text="⚡ Güç: Masaüstü (Şebeke)")
                except: pass
                root.after(2000, metrik_tazele)
        metrik_tazele()

        tk.Frame(sol_panel, bg=t["ana"], height=2).pack(fill='x', padx=15, pady=10)
        tk.Label(sol_panel, text="📋 HATIRLATMALAR & NOTLAR", fg=t["ikincil"], bg=t["panel"], font=("Consolas", 9, "bold")).pack(pady=4)

        notlar_text = Text(sol_panel, bg="#050816", fg="#cccccc", font=("Consolas", 9), bd=0, wrap='word', state='disabled')
        notlar_text.pack(fill='both', expand=True, padx=10, pady=5)
        notlar_paneli_tazele()

        # Sağ Panel (Sohbet ve Komut Konsolu)
        sag_panel = tk.Frame(govde, bg=t["panel"])
        sag_panel.pack(side='right', fill='both', expand=True)

        tk.Label(sag_panel, text="📡 HUD ETKİLEŞİM & KOMUT KONSOLU", fg="#666666", bg=t["panel"], font=("Consolas", 10, "bold")).pack(pady=8)

        log_text = Text(sag_panel, bg="#030611", fg=t["ana"], font=("Consolas", 11), bd=0, wrap='word', state='disabled')
        log_text.pack(fill='both', expand=True, padx=12, pady=5)

        # Eski logları doldur
        log_text.configure(state='normal')
        for l in log_listesi:
            renk = t["ana"] if l["tip"] == "jarvis" else (t["ikincil"] if l["tip"] == "user" else "#888")
            log_text.insert('end', f"[{l['zaman']}] {l['mesaj']}\n", l["tip"])
            log_text.tag_config(l["tip"], foreground=renk)
        log_text.see('end')
        log_text.configure(state='disabled')

        # Hızlı Butonlar
        buton_frame = tk.Frame(root, bg=t["arka"])
        buton_frame.pack(fill='x', padx=15, pady=4)

        # Mikrofon Durum Butonu
        mik_renk = "#00aa44" if mikrofon_dikkate_alinsin_mi else "#aa2222"
        mik_yazi = "🎙️ MİKROFON: AÇIK" if mikrofon_dikkate_alinsin_mi else "🔇 MİKROFON: SAĞIR"
        global mikrofon_btn_pencere
        mikrofon_btn_pencere = tk.Button(buton_frame, text=mik_yazi, fg="white", bg=mik_renk,
                                         font=("Consolas", 9, "bold"), bd=0, padx=10, pady=6,
                                         command=mikrofon_modu_degistir, cursor="hand2")
        mikrofon_btn_pencere.pack(side='left', padx=3)

        hizli_isler = [
            ("🛑 Sus / Kes", konusmayi_kes, "#ff4444"),
            ("🎯 Odaklan", lambda: threading.Thread(target=lambda: sesli_konus(odaklanma_modu_degistir(True)), daemon=True).start(), "#00ff88"),
            ("🧹 Düzenle", lambda: threading.Thread(target=lambda: sesli_konus(masaustu_duzenle()), daemon=True).start(), "#a855f7"),
            ("📂 Son İndirilen", lambda: threading.Thread(target=lambda: sesli_konus(son_indirilen_dosya(acilsin_mi=True)), daemon=True).start(), "#eab308"),
            ("🌐 Google", lambda: threading.Thread(target=lambda: sesli_konus(chrome_arama_yap("")), daemon=True).start(), "#4285f4"),
            ("🎵 Spotify", lambda: threading.Thread(target=lambda: sesli_konus(spotify_komut_isle("spotify çal")), daemon=True).start(), "#1db954"),
            ("💱 Döviz", lambda: threading.Thread(target=lambda: sesli_konus(doviz_durumu()), daemon=True).start(), "#00d4ff"),
            ("📸 Ekran", lambda: threading.Thread(target=lambda: sesli_konus(ekran_goruntusu_al()), daemon=True).start(), "#ffaa00"),
            ("🖥️ Masaüstü", lambda: threading.Thread(target=lambda: sesli_konus(pencereleri_simge_yap()), daemon=True).start(), "#aaa")
        ]
        for yazi, fn, renk in hizli_isler:
            b = tk.Button(buton_frame, text=yazi, fg="white", bg="#101730", activebackground=renk,
                          font=("Consolas", 9, "bold"), bd=0, padx=8, pady=6, command=fn, cursor="hand2")
            b.pack(side='left', padx=2)

        # Komut Satırı
        giris_frame = tk.Frame(root, bg=t["panel"])
        giris_frame.pack(fill='x', padx=15, pady=(5, 12))

        komut_entry = tk.Entry(giris_frame, bg="#050816", fg="white", insertbackground="white", font=("Consolas", 12), bd=0)
        komut_entry.pack(side='left', fill='x', expand=True, padx=10, pady=8, ipady=4)
        komut_entry.insert(0, "Komut yazın veya seslenin...")
        komut_entry.bind('<FocusIn>', lambda e: komut_entry.delete(0, 'end') if komut_entry.get() == "Komut yazın veya seslenin..." else None)
        komut_entry.bind('<Return>', lambda e: manuel_komut_gonder())

        tk.Button(giris_frame, text="⚡ ÇALIŞTIR", fg="#050816", bg=t["ana"], activebackground=t["ikincil"],
                  font=("Consolas", 11, "bold"), bd=0, padx=16, pady=4, command=manuel_komut_gonder, cursor="hand2").pack(side='right', padx=10)

    else:
        # ========== KÜRE MODU (FLOATING ARC REACTOR) ==========
        root.overrideredirect(True)
        root.attributes('-topmost', True)
        root.attributes('-transparentcolor', 'black')
        root.configure(bg='black')
        root.geometry(f"200x200+{root.winfo_screenwidth() - 250}+50")

        kure_frame = tk.Frame(root, bg='black', width=200, height=200)
        kure_frame.pack(fill='both', expand=True)
        kure_frame.pack_propagate(False)

        canvas = tk.Canvas(kure_frame, width=200, height=160, bg='black', highlightthickness=0)
        canvas.pack(fill='both', expand=True)

        info_label = tk.Label(kure_frame, text="J.A.R.V.I.S", fg=t["ana"], bg='black', font=("Consolas", 8, "bold"))
        info_label.pack(fill='x')

        durum_label = tk.Label(kure_frame, text="● BEKLEMEDE", fg=t["ana"], bg='black', font=("Consolas", 7))
        durum_label.pack(fill='x')

        # İlk kareyi anında çiz ve güncelle
        try:
            reaktor_ciz(canvas, 100, 80, 75, "BEKLEMEDE")
            root.update_idletasks()
        except Exception:
            pass

        # Sürükleme ve Barge-in tıklama
        eski = {'x': 0, 'y': 0}
        def baslat_surukle(e):
            eski['x'], eski['y'] = e.x, e.y
            # Küreye tıklandığında konuşuyorsa anında susar
            if ses_caliniyor:
                konusmayi_kes()
        def surukle(e):
            root.geometry(f"+{root.winfo_x() + (e.x - eski['x'])}+{root.winfo_y() + (e.y - eski['y'])}")

        for elem in [kure_frame, canvas, info_label, durum_label]:
            elem.bind('<Button-1>', baslat_surukle)
            elem.bind('<B1-Motion>', surukle)
            elem.bind('<Double-Button-1>', lambda e: komut_penceresi_ac())

    menu_olustur()

def notlar_paneli_tazele():
    """Pencere modundaki notlar panelini günceller"""
    if simdiki_mod == "pencere" and notlar_text:
        try:
            notlar_text.configure(state='normal')
            notlar_text.delete('1.0', 'end')
            bugun = datetime.datetime.now().strftime("%Y-%m-%d")
            hatirlatmalar = hatirlatmalari_getir(bugun)
            notlar_text.insert('end', "═══ BUGÜNKÜ GÖREVLER ═══\n")
            if hatirlatmalar:
                for h in hatirlatmalar:
                    notlar_text.insert('end', f"• {h[2]}\n")
            else:
                notlar_text.insert('end', "Bugün hatırlatma yok.\n")

            notlar_text.insert('end', "\n═══ SON NOTLAR ═══\n")
            notlar = notlari_getir()
            if notlar:
                for n in notlar[:4]:
                    notlar_text.insert('end', f"▸ {n[0]}: {n[1][:30]}...\n")
            else:
                notlar_text.insert('end', "Kayıtlı not yok.\n")
            notlar_text.configure(state='disabled')
        except Exception:
            pass

def manuel_komut_gonder():
    if komut_entry:
        k = komut_entry.get().strip()
        if k and k != "Komut yazın veya seslenin...":
            log_mesaj(f"👤 {k}", "user")
            komut_entry.delete(0, 'end')
            threading.Thread(target=lambda: komut_isle(k.lower()), daemon=True).start()

def komut_penceresi_ac():
    komut = simpledialog.askstring("J.A.R.V.I.S Komut Satırı", "Komutunuzu giriniz efendim:", parent=root)
    if komut:
        log_mesaj(f"👤 {komut}", "user")
        threading.Thread(target=lambda: komut_isle(komut.lower()), daemon=True).start()

def ayarlar_penceresi_ac():
    """Kullanıcının API anahtarı, Valorant giriş ve kişisel ayarlarını girebileceği görsel HUD penceresi"""
    if not root:
        return
    win = tk.Toplevel(root)
    win.title("J.A.R.V.I.S — Yapılandırma & Ayarlar")
    win.geometry("540x640")
    win.configure(bg="#050816")
    win.resizable(False, False)
    win.attributes("-topmost", True)

    t = TEMALAR.get(simdiki_tema, TEMALAR["varsayilan"])

    ust = tk.Frame(win, bg="#0a0e27", height=50)
    ust.pack(fill="x", padx=15, pady=(15, 10))
    tk.Label(ust, text="⚙️ SİSTEM VE KİMLİK YAPILANDIRMASI", fg=t["ana"], bg="#0a0e27", font=("Consolas", 12, "bold")).pack(pady=10)

    govde = tk.Frame(win, bg="#050816")
    govde.pack(fill="both", expand=True, padx=25, pady=5)

    def _alan(label_text, varsayilan="", gizli=False):
        f = tk.Frame(govde, bg="#050816")
        f.pack(fill="x", pady=6)
        tk.Label(f, text=label_text, fg="#a0aec0", bg="#050816", font=("Consolas", 9, "bold")).pack(anchor="w")
        e = tk.Entry(f, bg="#0c122b", fg="#ffffff", insertbackground="white", font=("Consolas", 10), bd=1, relief="solid")
        if gizli:
            e.configure(show="*")
        e.pack(fill="x", ipady=4, pady=(2, 0))
        e.insert(0, varsayilan)
        return e

    e_api = _alan("🔑 Groq API Anahtarı (console.groq.com):", ayar_getir("groq_api_key", ""), gizli=True)
    e_hitap = _alan("👤 Hitap İsmi (Size nasıl seslensin?):", ayar_getir("kullanici_adi", KULLANICI_ADI))
    e_valo_user = _alan("🎮 Valorant Kullanıcı Adı:", ayar_getir("valorant_kullanici", ""))
    e_valo_pass = _alan("🔐 Valorant Şifresi:", ayar_getir("valorant_sifre", ""), gizli=True)
    e_gmail = _alan("📧 Gmail Adresi (Sesli mail için opsiyonel):", ayar_getir("gmail_adres", ""))
    e_gmail_pass = _alan("🔒 Gmail Uygulama Şifresi (Opsiyonel):", ayar_getir("gmail_sifre", ""), gizli=True)

    durum_lbl = tk.Label(govde, text="", fg="#00ff88", bg="#050816", font=("Consolas", 9))
    durum_lbl.pack(pady=6)

    def kaydet():
        global KULLANICI_ADI, groq_client
        api_val = e_api.get().strip()
        hitap_val = e_hitap.get().strip() or "Efendim"
        valo_u_val = e_valo_user.get().strip()
        valo_p_val = e_valo_pass.get().strip()
        gmail_val = e_gmail.get().strip()
        gmail_p_val = e_gmail_pass.get().strip()

        ayar_kaydet("groq_api_key", api_val)
        ayar_kaydet("kullanici_adi", hitap_val)
        ayar_kaydet("valorant_kullanici", valo_u_val)
        ayar_kaydet("valorant_sifre", valo_p_val)
        ayar_kaydet("gmail_adres", gmail_val)
        ayar_kaydet("gmail_sifre", gmail_p_val)

        KULLANICI_ADI = hitap_val
        groq_client = None
        get_groq_client()

        durum_lbl.configure(text="✓ Tüm ayarlar veritabanına güvenle kaydedildi!", fg="#00ff88")
        log_mesaj("⚙️ Sistem ayarları başarıyla güncellendi.", "jarvis")
        win.after(1000, win.destroy)

    btn_frame = tk.Frame(win, bg="#050816")
    btn_frame.pack(fill="x", padx=25, pady=(0, 20))

    tk.Button(btn_frame, text="💾 KAYDET & UYGULA", fg="#050816", bg=t["ana"], activebackground=t["ikincil"],
              font=("Consolas", 11, "bold"), bd=0, padx=20, pady=8, command=kaydet, cursor="hand2").pack(fill="x")

def menu_olustur():
    """Sağ tık HUD menüsü"""
    menu = tk.Menu(root, tearoff=0, bg='#0a0e27', fg='white', activebackground='#00d4ff', activeforeground='black', font=("Consolas", 9))
    menu.add_command(label="💬 Komut Gir...", command=komut_penceresi_ac)
    menu.add_command(label="🎤 Dinle", command=lambda: threading.Thread(target=tekli_ses_isle, daemon=True).start())
    menu.add_command(label="🎙️ Mikrofon: Aç / Kapat (Dikkate Al)", command=mikrofon_modu_degistir)
    menu.add_command(label="🛑 Konuşmayı Kes", command=konusmayi_kes)
    menu.add_separator()
    menu.add_command(label="⚙️ Ayarlar (API & Giriş Bilgileri)", command=ayarlar_penceresi_ac)
    menu.add_command(label="🖥️ Pencere / Küre Modu (F)", command=lambda: mod_degistir())
    menu.add_separator()
    menu.add_command(label="🔴 Iron Man Mark VII (Kırmızı)", command=lambda: tema_uygula("mark_vii"))
    menu.add_command(label="🟢 Stealth Matrix (Yeşil)", command=lambda: tema_uygula("stealth"))
    menu.add_command(label="🟣 Hulkbuster (Mor)", command=lambda: tema_uygula("hulkbuster"))
    menu.add_command(label="🔵 Stark Arc (Cyan)", command=lambda: tema_uygula("varsayilan"))
    menu.add_separator()
    menu.add_command(label="❌ Kapat", command=uygulamayi_kapat)

    root.bind('<Button-3>', lambda e: menu.tk_popup(e.x_root, e.y_root))
    root.bind('<f>', lambda e: mod_degistir())
    root.bind('<F>', lambda e: mod_degistir())
    root.bind('<Escape>', lambda e: uygulamayi_kapat())

def uygulamayi_kapat():
    global running
    running = False
    konusmayi_kes()
    try: root.destroy()
    except: pass
    os._exit(0)

# =========================================================================
# 🔄 ANA İŞLEM DÖNGÜSÜ: SÜREKLİ SOHBET (FOLLOW-UP) & WAKE-WORD
# =========================================================================

def tekli_ses_isle():
    """Manuel mikrofon tetikleme"""
    ses_efekti_cal("wake")
    durum_guncelle("DİNLİYOR")
    komut = ses_dinle(timeout=8, limit=8)
    if komut and komut not in ["anlasilamadi", "zaman_asimi", "hata"]:
        komut_isle(komut)
    durum_guncelle("BEKLEMEDE")

def jarvis_ana_dongusu():
    """
    Sürekli Sohbet (Follow-up) ve 'Dikkate Al' Sağır Modunu yöneten akıllı döngü.
    Kullanıcı 'beni dinleme' derse sağır moduna geçer, 'dikkate al' diyene kadar hiçbir şeyi işlemez.
    """
    global running, sohbet_aktif, mikrofon_dikkate_alinsin_mi, KULLANICI_ADI
    veritabani_olustur()
    threading.Thread(target=_kripto_alarm_kontrol_dongusu, daemon=True).start()
    time.sleep(1)

    # Kaydedilmiş hitap ismini yükle
    kayitli_isim = ayar_getir("kullanici_adi", "")
    if kayitli_isim:
        KULLANICI_ADI = kayitli_isim

    log_mesaj("🚀 J.A.R.V.I.S Asistan devrede.", "jarvis")
    log_mesaj("💡 F tuşu: Pencere/Küre modu | Sağ Tık: Menü | 'Beni dinleme': Sağır modu | 'Dikkate al': Uyan", "info")
    durum_guncelle("BEKLEMEDE")

    while running:
        # 🔇 1. SAĞIR MODU (MİKROFON KAPALI / DİKKATE ALINMIYOR)
        if not mikrofon_dikkate_alinsin_mi:
            durum_guncelle("SAĞIR")
            metin = ses_dinle(timeout=5, limit=4)
            if metin and dikkate_al_mi_kontrol(metin):
                ses_efekti_cal("wake")
                mikrofon_modu_degistir(True)
                sohbet_aktif = True
                sesli_konus(f"Sizi dinliyorum {KULLANICI_ADI}, dikkate alınıyorsunuz.")
            time.sleep(0.1)
            continue

        # 🎙️ 2. NORMAL MOD
        if not sohbet_aktif:
            # Wake-word Dinleme Modu (Pasif)
            metin = ses_dinle(timeout=5, limit=4)
            if metin:
                # Eğer sağır moduna alma komutu gelirse
                if any(k in metin for k in ["beni dinleme", "mikrofonu kapat", "sağır modu", "dikkate alma"]):
                    komut_isle(metin)
                    continue

                if wake_word_kontrol(metin):
                    ses_efekti_cal("wake")
                    sohbet_aktif = True
                    sesli_konus(random.choice([
                        f"Emrinizdeyim {KULLANICI_ADI}.",
                        f"Dinliyorum {KULLANICI_ADI}.",
                        "Sistemler hazır efendim, buyrun."
                    ]))
        else:
            # 🔥 SÜREKLİ SOHBET MODU (HER SEFERİNDE 'JARVIS' DEMEK YOK!)
            durum_guncelle("DİNLİYOR")
            komut = ses_dinle(timeout=14, limit=10)

            if komut == "zaman_asimi":
                # 14 saniye hiçbir şey söylenmedi -> Uyku moduna geç
                sohbet_aktif = False
                log_mesaj("💤 Sessizlik algılandı, pasif bekleme moduna geçildi.", "info")
                durum_guncelle("BEKLEMEDE")

            elif komut in ["anlasilamadi", "hata"]:
                # Anlaşılmadıysa tekrar dinle
                continue

            else:
                sonuc = komut_isle(komut)
                notlar_paneli_tazele()
                if sonuc == "sohbeti_bitir":
                    sohbet_aktif = False
                    durum_guncelle("BEKLEMEDE")

        time.sleep(0.1)

# =========================================================================
# 🚀 GİRİŞ NOKTASI
# =========================================================================

if __name__ == "__main__":
    root = tk.Tk()
    root.title("J.A.R.V.I.S")

    # İkon ayarla
    icon_yolu = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pngkey.com-arc-reactor-png-1805690.ico")
    if os.path.exists(icon_yolu):
        try:
            root.iconbitmap(icon_yolu)
        except Exception:
            pass

    # Başlangıçta Küre Modu
    mod_degistir("kure")

    # Animasyon döngüsü
    root.after(100, animasyon_dongusu)

    # Arka plan sürekli dinleme iş parçacığı
    threading.Thread(target=jarvis_ana_dongusu, daemon=True).start()

    # Tkinter ana döngüsü
    root.mainloop()
