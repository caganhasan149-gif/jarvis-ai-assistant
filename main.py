"""
╔══════════════════════════════════════════════════════╗
║          J.A.R.V.I.S - ULTIMATE EDITION v2.0         ║
║     Just A Rather Very Intelligent System            ║
║                                                      ║
║  🎤 Sesli komut + 💬 Yazılı komut                    ║
║  🔵 Küre Modu + 🖥️ Pencere Modu                     ║
║  🤖 Groq AI + 🧠 Akıllı Komut İşleme                ║
║  📊 Sohbet Baloncukları + 📋 Notlar & Hatırlatmalar   ║
╚══════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import random
import datetime
import threading
import webbrowser

# Modül yolunu ayarla
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.config import (
    GROQ_API_KEY, KULLANICI_ADI, TEMALAR, Tema,
    MOTIVASYON_SOZLERI, FIKRALAR, KITAP_ONERILERI, FILM_ONERILERI,
    WAKE_WORDS, WAKE_WORD_KOKLERI,
    MASAUSTU, DB_PATH,
    EDGE_TTS_SESLER, TTS_HIZ,
    DINLEME_TIMEOUT, DINLEME_FRAZ_LIMITI,
    WAKE_TIMEOUT, WAKE_FRAZ_LIMITI, ENERJI_ESIGI,
    AI_MODEL, AI_SYSTEM_PROMPT,
    GMAIL_ADRES, GMAIL_SIFRE,
    VALORANT_KULLANICI_ADI, VALORANT_SIFRE,
    WHATSAPP_REHBERI, SCRCPY_YOLU,
)
from core.utils import (
    simdi, bugunun_tarihi, tarih_kisa, saat_dilimi_selamlama,
    tarihi_parse_et, fuzzy_eslesme, anahtar_kelime_bul,
    matematik_hesapla, sifre_uret,
)
from core.database import JarvisDB
from core.speech import SesMotoru
from core.commands import (
    kutuphane_durumu, bildirim_gonder,
    doviz_fiyatlari, hava_durumu, haberleri_getir,
    zar_at, yazitura_at, rastgele_say, fıkra_anlat, motivasyon_ver,
    kitap_oner, film_oner,
    ekran_goruntusu_al, sistem_bilgisi,
    dosya_ara, klasor_olustur, son_indirilen,
    spotify_kontrol, pomodoro_baslat,
    wikipedia_ara, cevir, internette_ara,
    uyku_modu, oyun_modu,
    mail_gonder, pdf_oku, web_ozetle,
    yuz_tanima_baslat, whatsapp_gonder,
    valorant_ac, valorant_giris,
    sifre_uret_komut, scrcpy_baslat,
    bilgisayar_kapat, ekrani_kilitle, masaustu_ac,
    indirilenler_ac, not_defteri_ac, hesap_makinesi_ac,
    youtube_ac, gunluk_rutin,
)
from core.gui import JarvisGUI

# Groq client
try:
    from groq import Groq
    client = Groq(api_key=GROQ_API_KEY)
    GROQ_VAR = True
except Exception:
    GROQ_VAR = False
    client = None


class JarvisApp:
    """Ana Jarvis Uygulaması - Tüm bileşenleri bir araya getirir"""

    def __init__(self):
        # Veritabanı
        self.db = JarvisDB(DB_PATH)

        # Ses motoru
        self.ses = SesMotoru(
            edge_tts_sesler=EDGE_TTS_SESLER,
            tts_hiz=TTS_HIZ,
            dinleme_timeout=DINLEME_TIMEOUT,
            dinleme_fraz_limiti=DINLEME_FRAZ_LIMITI,
            wake_timeout=WAKE_TIMEOUT,
            wake_fraz_limiti=WAKE_FRAZ_LIMITI,
            enerji_esigi=ENERJI_ESIGI,
            wake_words=WAKE_WORDS,
            wake_kokleri=WAKE_WORD_KOKLERI,
        )

        # GUI
        self.gui = JarvisGUI()

        # Durum
        self.running = True

        # Callback'leri bağla
        self._callbacklari_bagla()

    def _callbacklari_bagla(self):
        """Tüm callback'leri bağlar"""
        # Ses → GUI
        self.ses.on_log = self.gui.log
        self.ses.on_durum_degisti = self.gui.durum_guncelle

        # GUI → Komut işleme
        self.gui.on_komut = lambda k: threading.Thread(
            target=lambda: self.komut_isle(k), daemon=True
        ).start()
        self.gui.on_sesli_dinle = self._sesli_dinle_ve_isle
        self.gui.on_kapat = self._kapat

    # =====================================================
    # 🤖 YAPAY ZEKA
    # =====================================================

    def yapay_zekaya_sor(self, soru: str) -> str:
        """Groq AI'ya soru sorar"""
        if not GROQ_VAR or not client:
            return "AI bağlantısı kurulamadı."
        try:
            system_prompt = AI_SYSTEM_PROMPT.replace("{kullanici_adi}", KULLANICI_ADI)
            chat = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": soru},
                ],
                model=AI_MODEL,
            )
            return chat.choices[0].message.content
        except Exception as e:
            return f"AI hatası: {str(e)[:80]}"

    # =====================================================
    # 🎯 KOMUT İŞLEME - ANA MOTOR
    # =====================================================

    def komut_isle(self, komut: str) -> bool:
        """Ana komut işleme fonksiyonu - NLP tabanlı fuzzy matching"""
        komut = komut.lower().strip()

        # Boş/hatalı komutları atla
        if komut in ["anlasilamadi", "hata", "bekleme_suresi_doldu", ""]:
            return True

        # Komut istatistiği kaydet
        self.db.komut_kaydet(komut)

        # ====== SELAMLAŞMA ======
        if anahtar_kelime_bul(komut, ["merhaba", "selam", "hey"]):
            self._konustur(random.choice([
                f"Merhaba {KULLANICI_ADI}! Size nasıl yardımcı olabilirim?",
                f"Selamlar {KULLANICI_ADI}! Emrinize amadeyim.",
                "Merhaba efendim! Sizi dinliyorum.",
            ]))

        elif anahtar_kelime_bul(komut, ["nasılsın", "nasilsin", "naber"]):
            self._konustur(f"İyiyim {KULLANICI_ADI}, teşekkür ederim! Siz nasılsınız?")

        # ====== SAAT / TARİH ======
        elif anahtar_kelime_bul(komut, ["saat kaç", "saat kac", "saati söyle"]):
            self._konustur(f"🕐 Saat {simdi()}.")

        elif anahtar_kelime_bul(komut, ["tarih", "bugün ne", "hangi gün"]):
            self._konustur(f"📅 Bugün {bugunun_tarihi()}.")

        # ====== HAVA DURUMU ======
        elif anahtar_kelime_bul(komut, ["hava durumu", "hava nasıl", "hava"]):
            sehir = "Ankara" if "ankara" in komut else "Istanbul"
            self._konustur(hava_durumu(sehir))

        # ====== DÖVİZ ======
        elif anahtar_kelime_bul(komut, ["dolar", "euro", "döviz", "bitcoin", "fiyat", "kur"]):
            self._konustur(doviz_fiyatlari())

        # ====== EĞLENCE ======
        elif anahtar_kelime_bul(komut, ["zar at", "zar"]):
            self._konustur(zar_at())

        elif anahtar_kelime_bul(komut, ["yazı tura", "para at"]):
            self._konustur(yazitura_at())

        elif anahtar_kelime_bul(komut, ["sayı tut", "rastgele sayı"]):
            self._konustur(rastgele_say())

        elif anahtar_kelime_bul(komut, ["motivasyon", "günün sözü", "motive"]):
            self._konustur(motivasyon_ver(MOTIVASYON_SOZLERI))

        elif anahtar_kelime_bul(komut, ["fıkra", "şaka", "espri"]):
            self._konustur(fıkra_anlat(FIKRALAR))

        elif anahtar_kelime_bul(komut, ["kitap öner", "kitap tavsiye"]):
            self._konustur(kitap_oner(komut, KITAP_ONERILERI))

        elif anahtar_kelime_bul(komut, ["film öner", "film tavsiye", "dizi öner"]):
            self._konustur(film_oner(komut, FILM_ONERILERI))

        # ====== MATEMATİK ======
        elif anahtar_kelime_bul(komut, ["çarpı", "bölü", "hesapla", "kaç eder", "toplam", "artı", "eksi"]):
            self._konustur(matematik_hesapla(komut))

        # ====== EKRAN GÖRÜNTÜSÜ ======
        elif anahtar_kelime_bul(komut, ["ekran görüntüsü", "screenshot", "ss al"]):
            self._konustur(ekran_goruntusu_al(MASAUSTU))

        # ====== SİSTEM ======
        elif anahtar_kelime_bul(komut, ["sistem bilgisi", "cpu", "ram", "sistem"]):
            self._konustur(sistem_bilgisi())

        # ====== MÜZİK / SPOTIFY ======
        elif anahtar_kelime_bul(komut, ["spotify", "şarkı", "müzik", "çal"]):
            self._konustur(spotify_kontrol(komut, log_fn=self.gui.log))

        # ====== POMODORO ======
        elif anahtar_kelime_bul(komut, ["pomodoro", "odaklan", "zamanlayıcı"]):
            self._konustur(pomodoro_baslat(25, bitince_fn=self._konustur))

        # ====== WIKIPEDIA ======
        elif anahtar_kelime_bul(komut, ["wikipedia", "vikipedi", "wiki"]):
            sorgu = komut
            for k in ["wikipedia", "vikipedi", "wiki"]:
                sorgu = sorgu.replace(k, "")
            sorgu = sorgu.strip()
            self._konustur(wikipedia_ara(sorgu if sorgu else "Türkiye"))

        # ====== ÇEVİRİ ======
        elif anahtar_kelime_bul(komut, ["çevir", "translate", "ingilizce"]):
            sorgu = komut
            for k in ["çevir", "translate", "ingilizce", "türkçe"]:
                sorgu = sorgu.replace(k, "")
            hedef = "en" if "ingilizce" in komut else "tr"
            self._konustur(cevir(sorgu.strip(), hedef))

        # ====== İNTERNET ARAMA ======
        elif anahtar_kelime_bul(komut, ["ara", "internette ara", "kimdir", "nedir", "google"]):
            sorgu = komut
            for k in ["internette ara", "ara", "kimdir", "nedir", "google"]:
                sorgu = sorgu.replace(k, "")
            sorgu = sorgu.strip()
            if sorgu:
                self._konustur(internette_ara(sorgu))
            else:
                self._konustur("Ne aramamı istersiniz?")

        # ====== DOSYA YÖNETİMİ ======
        elif anahtar_kelime_bul(komut, ["dosya ara", "dosya bul"]):
            aranan = komut.replace("dosya ara", "").replace("dosya bul", "").strip()
            if aranan:
                self._konustur(dosya_ara(aranan))
            else:
                self._konustur("Ne aramamı istersiniz?")

        elif anahtar_kelime_bul(komut, ["klasör oluştur", "klasör aç"]):
            isim = komut.replace("klasör oluştur", "").replace("klasör aç", "").strip()
            if isim:
                self._konustur(klasor_olustur(isim))
            else:
                self._konustur("Klasör adı söyleyin.")

        elif anahtar_kelime_bul(komut, ["son indirilen"]):
            self._konustur(son_indirilen())

        # ====== PARLAKLIK / UYKU ======
        elif anahtar_kelime_bul(komut, ["uyku modu", "parlaklık", "parlaklik"]):
            self._konustur(uyku_modu())

        # ====== OYUN MODU ======
        elif anahtar_kelime_bul(komut, ["oyun modu"]):
            self._konustur(oyun_modu())

        # ====== ŞİFRE ======
        elif anahtar_kelime_bul(komut, ["şifre üret", "parola", "şifre oluştur"]):
            uzunluk = 16
            if "32" in komut:
                uzunluk = 32
            elif "8" in komut:
                uzunluk = 8
            elif "24" in komut:
                uzunluk = 24
            self._konustur(sifre_uret_komut(uzunluk))

        # ====== HATIRLATMA ======
        elif anahtar_kelime_bul(komut, ["hatırla", "hatırlat"]) and not anahtar_kelime_bul(komut, ["hatırlatma", "hatırlatmalarım"]):
            self._konustur("Ne zaman hatırlatayım? (bugün, yarın, haftaya)")
            tarih_metni = self.ses.ses_dinle()
            if tarih_metni not in ["anlasilamadi", "hata", "bekleme_suresi_doldu"]:
                self._konustur("Hatırlatılacak mesajı söyleyin.")
                mesaj = self.ses.ses_dinle()
                if mesaj not in ["anlasilamadi", "hata", "bekleme_suresi_doldu"]:
                    tarih = tarihi_parse_et(tarih_metni)
                    self.db.hatirlatma_ekle(tarih, mesaj)
                    bildirim_gonder("📌 Hatırlatma", f"{tarih}: {mesaj}")
                    self._konustur(f"✅ Kaydedildi! {tarih} tarihinde hatırlatacağım: {mesaj}")
                    self._notlari_guncelle()

        elif anahtar_kelime_bul(komut, ["hatırlatmalarım", "hatırlatma listesi"]):
            hatirlatmalar = self.db.hatirlatmalari_getir()
            if hatirlatmalar:
                mesajlar = "\n".join([f"📌 {h['tarih']}: {h['mesaj']}" for h in hatirlatmalar[:5]])
                self._konustur(f"Hatırlatmalarınız:\n{mesajlar}")
            else:
                self._konustur("Aktif hatırlatmanız yok.")

        elif anahtar_kelime_bul(komut, ["bugün ne var"]):
            bugun = tarih_kisa()
            hatirlatmalar = self.db.hatirlatmalari_getir(bugun)
            if hatirlatmalar:
                mesajlar = ", ".join([h['mesaj'] for h in hatirlatmalar])
                self._konustur(f"📌 Bugünkü hatırlatmalar: {mesajlar}")
            else:
                self._konustur("Bugün için hatırlatma yok.")

        # ====== NOTLAR ======
        elif anahtar_kelime_bul(komut, ["not al", "not tut", "not kaydet", "not ekle", "not yaz"]):
            self._konustur("Not başlığını söyleyin.")
            baslik = self.ses.ses_dinle()
            if baslik not in ["anlasilamadi", "hata", "bekleme_suresi_doldu"]:
                self._konustur("Not içeriğini söyleyin.")
                icerik = self.ses.ses_dinle()
                if icerik not in ["anlasilamadi", "hata", "bekleme_suresi_doldu"]:
                    self.db.not_ekle(baslik, icerik)
                    self._konustur(f"✅ '{baslik}' notu kaydedildi.")
                    self._notlari_guncelle()

        elif anahtar_kelime_bul(komut, ["notlarım", "notları göster"]):
            notlar = self.db.notlari_getir()
            if notlar:
                mesajlar = "\n".join([f"📝 {n['baslik']}: {n['icerik'][:40]}..." for n in notlar[:5]])
                self._konustur(f"Notlarınız:\n{mesajlar}")
            else:
                self._konustur("Hiç notunuz yok.")

        # ====== GEÇMİŞ TEMİZLE ======
        elif anahtar_kelime_bul(komut, ["geçmişi temizle", "hafıza temizle", "herşeyi sil"]):
            self._konustur("Emin misiniz? 'Evet' deyin.")
            onay = self.ses.ses_dinle()
            if "evet" in onay:
                self.db.tumu_temizle()
                self._konustur("🗑️ Tüm hafıza temizlendi.")
                self._notlari_guncelle()
            else:
                self._konustur("Tamam, hafıza korundu.")

        # ====== HABER ======
        elif anahtar_kelime_bul(komut, ["haber", "gündem", "son dakika"]):
            self._konustur(haberleri_getir())

        # ====== MAIL ======
        elif anahtar_kelime_bul(komut, ["mail gönder", "eposta gönder"]):
            self._konustur("Alıcı e-posta adresini söyleyin.")
            alici = self.ses.ses_dinle()
            if alici not in ["anlasilamadi", "hata"]:
                self._konustur("Mail konusunu söyleyin.")
                konu = self.ses.ses_dinle()
                if konu not in ["anlasilamadi", "hata"]:
                    self._konustur("Mail içeriğini söyleyin.")
                    icerik = self.ses.ses_dinle()
                    if icerik not in ["anlasilamadi", "hata"]:
                        self._konustur(mail_gonder(alici, konu, icerik, GMAIL_ADRES, GMAIL_SIFRE))

        # ====== PDF ======
        elif anahtar_kelime_bul(komut, ["pdf oku", "pdf"]):
            dosya = komut.replace("pdf oku", "").replace("pdf", "").strip()
            if dosya:
                yol = os.path.join(MASAUSTU, dosya)
                if not dosya.endswith('.pdf'):
                    yol += '.pdf'
                self._konustur(pdf_oku(yol))
            else:
                self._konustur("PDF dosya adını söyleyin.")

        # ====== WEB ÖZET ======
        elif anahtar_kelime_bul(komut, ["web özet", "özetle", "sayfa özetle"]):
            url = komut.replace("web özet", "").replace("sayfa özetle", "").replace("özetle", "").strip()
            if url:
                self._konustur(web_ozetle(url))
            else:
                self._konustur("URL söyleyin.")

        # ====== YÜZ TANIMA ======
        elif anahtar_kelime_bul(komut, ["yüz tanı", "kamera aç"]):
            self._konustur(yuz_tanima_baslat())

        # ====== TEMA ======
        elif anahtar_kelime_bul(komut, ["tema"]):
            tema_adi = "varsayilan"
            if "kırmızı" in komut or "kirmizi" in komut:
                tema_adi = "kirmizi"
            elif "yeşil" in komut or "yesil" in komut:
                tema_adi = "yesil"
            elif "mor" in komut:
                tema_adi = "mor"
            elif "matrix" in komut:
                tema_adi = "matrix"
            elif "cyberpunk" in komut:
                tema_adi = "cyberpunk"
            elif "midnight" in komut or "gece" in komut:
                tema_adi = "midnight"
            elif "değiştir" in komut:
                mevcut_temalar = list(TEMALAR.keys())
                mevcut = mevcut_temalar.index(self.gui.simdiki_tema_adi) if self.gui.simdiki_tema_adi in mevcut_temalar else 0
                tema_adi = mevcut_temalar[(mevcut + 1) % len(mevcut_temalar)]

            if tema_adi in TEMALAR:
                tema_obj = TEMALAR[tema_adi]
                self.gui.tema_degistir(tema_adi, {
                    "arka_plan": tema_obj.arka_plan,
                    "panel": tema_obj.panel,
                    "ana_renk": tema_obj.ana_renk,
                    "ikincil": tema_obj.ikincil,
                })
                self._konustur(f"🎨 Tema '{tema_adi}' olarak değiştirildi.")

        # ====== GÜNLÜK RUTİN ======
        elif anahtar_kelime_bul(komut, ["günaydın", "rutin başlat", "günü özetle"]):
            self._konustur(gunluk_rutin(
                KULLANICI_ADI, MOTIVASYON_SOZLERI,
                hatirlatma_fn=lambda t: self.db.hatirlatmalari_getir(t)
            ))

        # ====== YOUTUBE ======
        elif anahtar_kelime_bul(komut, ["youtube", "yt"]):
            youtube_ac()
            self._konustur("🎬 YouTube açılıyor efendim.")

        # ====== VALORANT ======
        elif anahtar_kelime_bul(komut, ["valorant", "valo"]):
            self.gui.log("🎮 Valorant açılıyor...", "info")
            valorant_ac()
            self._konustur("🎮 Valorant açılıyor efendim. 12 saniye sonra otomatik giriş yapılacak.")
            threading.Thread(
                target=lambda: self._konustur(
                    valorant_giris(VALORANT_KULLANICI_ADI, VALORANT_SIFRE, self.gui.root)
                ),
                daemon=True,
            ).start()

        # ====== WHATSAPP ======
        elif anahtar_kelime_bul(komut, ["mesaj at", "whatsapp"]):
            for isim, numara in WHATSAPP_REHBERI.items():
                if isim in komut:
                    self._konustur(f"{isim.capitalize()} için mesaj söyleyin.")
                    mesaj = self.ses.ses_dinle()
                    if mesaj not in ["anlasilamadi", "hata"]:
                        self._konustur(whatsapp_gonder(numara, mesaj))
                    return True
            self._konustur("Kime mesaj atmak istiyorsunuz?")

        # ====== SCRCPY / TELEFON YANSITMA ======
        elif anahtar_kelime_bul(komut, ["ekran paylaş", "scrcpy", "telefon ekranı", "telefonu yansıt"]):
            self._konustur(scrcpy_baslat(SCRCPY_YOLU))

        # ====== MASAÜSTÜ ======
        elif anahtar_kelime_bul(komut, ["masaüstü", "desktop"]):
            masaustu_ac()
            self._konustur("🖥️ Masaüstü açılıyor.")

        # ====== İNDİRİLENLER ======
        elif anahtar_kelime_bul(komut, ["indirilenler", "downloads"]):
            indirilenler_ac()
            self._konustur("📥 İndirilenler klasörü açılıyor.")

        # ====== NOT DEFTERİ ======
        elif anahtar_kelime_bul(komut, ["not defteri", "notepad"]):
            not_defteri_ac()
            self._konustur("📝 Not defteri açılıyor.")

        # ====== HESAP MAKİNESİ ======
        elif anahtar_kelime_bul(komut, ["hesap makinesi", "calculator"]):
            hesap_makinesi_ac()
            self._konustur("🔢 Hesap makinesi açılıyor.")

        # ====== KAPAT / KİLİTLE ======
        elif anahtar_kelime_bul(komut, ["bilgisayarı kapat", "pc kapat"]):
            self._konustur("💻 Bilgisayar 15 saniye içinde kapanacak...")
            bilgisayar_kapat()

        elif anahtar_kelime_bul(komut, ["ekranı kilitle", "kilitle", "lock"]):
            self.gui.log("🔒 Ekran kilitleniyor...", "info")
            ekrani_kilitle()

        # ====== GÖRÜŞÜRÜZ ======
        elif anahtar_kelime_bul(komut, ["görüşürüz", "bye", "hoşça kal", "kapan"]):
            self._konustur(f"Görüşürüz {KULLANICI_ADI}! İyi günler dilerim. 👋")
            return False

        # ====== AI FALLBACK ======
        else:
            self.gui.durum_guncelle("İŞLENİYOR")
            cevap = self.yapay_zekaya_sor(komut)
            self._konustur(cevap)
            self.db.gecmis_kaydet(komut, cevap)

        return True

    # =====================================================
    # 🔧 YARDIMCI METODLAR
    # =====================================================

    def _konustur(self, mesaj: str):
        """Mesajı hem seslendirir hem de GUI'ye yazar"""
        self.ses.sesli_konus(mesaj)

    def _sesli_dinle_ve_isle(self):
        """Mikrofonu dinler ve komutu işler"""
        self.gui.durum_guncelle("DİNLİYOR")
        komut = self.ses.ses_dinle()
        if komut and komut not in ["anlasilamadi", "hata", "bekleme_suresi_doldu"]:
            self.gui.durum_guncelle("İŞLENİYOR")
            self.komut_isle(komut)
        self.gui.durum_guncelle("BEKLEMEDE")

    def _notlari_guncelle(self):
        """Notlar panelini günceller"""
        bugun = tarih_kisa()
        hatirlatmalar = self.db.hatirlatmalari_getir(bugun)
        notlar = self.db.notlari_getir()
        istatistikler = self.db.istatistik()
        
        istatistik_map = {
            "hatirlatma": istatistikler.get("hatirlatmalar", 0),
            "not": istatistikler.get("notlar", 0),
            "komut": istatistikler.get("gecmis", 0),
        }
        
        self.gui.notlar_paneli_guncelle(hatirlatmalar, notlar, istatistik_map)

    def _kapat(self):
        """Uygulamayı düzgün kapatır"""
        self.running = False

    # =====================================================
    # 🚀 ANA DÖNGÜ
    # =====================================================

    def jarvis_dongusu(self):
        """Arka plan Jarvis döngüsü (wake word dinleme)"""
        self.gui.log("🚀 J.A.R.V.I.S v2.0 başlatılıyor...", "info")

        # Kütüphane durumu
        durumlar = kutuphane_durumu()
        aktif = [f"✓ {k}" for k, v in durumlar.items() if v]
        if aktif:
            self.gui.log(f"📦 Aktif modüller: {', '.join(aktif)}", "success")

        time.sleep(1)

        # Notları güncelle
        self._notlari_guncelle()

        # Bugünkü hatırlatmaları seslendir
        bugun = tarih_kisa()
        hatirlatmalar = self.db.hatirlatmalari_getir(bugun)
        if hatirlatmalar:
            mesajlar = ", ".join([h['mesaj'] for h in hatirlatmalar])
            self._konustur(f"📌 Bugün için {len(hatirlatmalar)} hatırlatmanız var: {mesajlar}")
            bildirim_gonder("🔔 Hatırlatma", mesajlar)

        self.gui.log("💡 'Jarvis' diyerek seslenebilirsiniz | F: Mod değiştir | Sağ tık: Menü", "info")
        self.gui.durum_guncelle("BEKLEMEDE")

        # Ana wake word döngüsü
        while self.running:
            try:
                if self.ses.wake_word_dinle():
                    self.gui.durum_guncelle("UYANDI")
                    self._konustur("Efendim, sizi dinliyorum.")

                    komut = self.ses.ses_dinle()
                    if komut and komut not in ["anlasilamadi", "hata", "bekleme_suresi_doldu"]:
                        self.gui.durum_guncelle("İŞLENİYOR")
                        devam = self.komut_isle(komut)
                        self._notlari_guncelle()
                        if not devam:
                            self.running = False
                            break

                    self.gui.durum_guncelle("BEKLEMEDE")
            except Exception as e:
                self.gui.log(f"⚠️ Hata: {str(e)[:60]}", "error")
                time.sleep(1)

            time.sleep(0.1)

    def baslat(self):
        """Uygulamayı başlatır"""
        # GUI başlat
        self.gui.baslat()

        # Arka plan döngüsü başlat
        threading.Thread(target=self.jarvis_dongusu, daemon=True).start()

        # Ana döngü
        self.gui.mainloop()


# =====================================================
# 🚀 PROGRAM BAŞLANGIÇ NOKTASI
# =====================================================
if __name__ == "__main__":
    app = JarvisApp()
    app.baslat()
