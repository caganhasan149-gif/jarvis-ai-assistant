# J.A.R.V.I.S — Tam Yetenek & Komut Kılavuzu (v5.5 Iron Man HUD Edition)

Tüm sistemler, niyet motoru, yapay zeka entegrasyonu, dosya analizleri ve sesli kontroller uçtan uca test edilmiş ve %100 kararlılıkla onaylanmıştır.

---

## ⚡ 1. Temel Etkileşim, Uyanma & Mikrofon Kontrolleri
| Komut / Hareket | Açıklama |
| :--- | :--- |
| **"Jarvis"** / **"Hey Jarvis"** / **"Uyan"** | Asistanı uyandırır, **Iron Man Repulsor şarj ses efekti** çalar ve **Sürekli Sohbet Modu**'nu başlatır. |
| **"Beni dinleme"** / **"Mikrofonu kapat"** / **"Sağır modu"** | Mikrofonu tamamen devre dışı bırakır. Siz *"Jarvis dikkate al"* diyene kadar ortam seslerine tepki vermez. |
| **"Jarvis dikkate al"** / **"Beni dinle"** / **"Mikrofonu aç"** | Sağır modundan çıkar, reaktör açılış sesi çalar ve tekrar komut almaya başlar. |
| **"Tamamdır"** / **"Dinlen"** / **"Sus"** / **"Bekle"** | Aktif sohbeti bitirir ve pasif bekleme moduna geçer. |
| **Jarvis konuşurken konuşmak veya Küreye tıklamak** | **Barge-in:** Jarvis'in sözünü anında keser, susar ve sizi dinler. |
| **"Bana patron de"** / **"Bana Tony de"** / **"Bana [İsim] de"** | Hitap ismini kalıcı olarak günceller ve hafızaya kaydeder. |
| **F Tuşu** | **Küre Modu (Floating Arc Reactor)** ile **Genişletilmiş Pencere Modu** arasında geçiş yapar. |

---

## 🧠 2. Yapay Zeka, Dosya Okuma & Verimlilik
| Komut | Açıklama |
| :--- | :--- |
| **"[Dosya] oku ve özetle"** / **"Masaüstündeki rapor.pdf dosyasını özetle"** | Masaüstü veya İndirilenler'deki PDF, DOCX veya TXT dosyasını bulur, metnini okur ve **Groq AI** ile 3-4 cümlelik Türkçe elit bir özet çıkarıp seslendirir. |
| **"[Adres]'e '[Konu]' konulu '[Mesaj]' içerikli mail at"** | Sesli e-posta gönderir veya otomatik olarak panoya hazır taslağı kopyalar. |
| **"[X] karakterlik güçlü şifre üret"** / **"Parola oluştur"** | İstenen uzunlukta yüksek güvenlikli şifre üretir, **otomatik panoya kopyalar** ve seslendirir. |
| **"Panoyu oku"** / **"Kopyalanan metin neydi"** | Panonuzdaki metni sesli olarak size okur. |
| **Serbest Sohbet & Sorular** | Groq AI (Qwen 3.8 / GPT-OSS) altyapısıyla her türlü soruya akıllı, hafif esprili ve elit yanıtlar verir. |

---

## 🎯 3. Gelişmiş Sistem Otomasyonu & Düzen
| Komut | Açıklama |
| :--- | :--- |
| **"Odaklanma modunu aç"** / **"Focus mode"** / **"Çalışma modu"** | Tek komutla: Discord'u kapatır, Lo-fi müzik açar, ekran parlaklığını %40 yapar, VS Code'u başlatır ve Stealth HUD temasını uygular. |
| **"Odaklanma modunu kapat"** / **"Normal moda dön"** | Parlaklığı %80 yapar ve normal temaya döner. |
| **"Masaüstünü düzenle"** / **"Masaüstünü temizle"** / **"Dosyaları toparla"** | Masaüstündeki dağınık dosyaları otomatik olarak *Resimler*, *Belgeler*, *Kurulumlar ve Arşivler*, *Medya*, *Kod Dosyaları* klasörlerine organize eder. |
| **"Son indirdiğim dosyayı aç"** / **"Son indirdiğimi aç"** | İndirilenler klasörünüzdeki en son inen dosyayı otomatik olarak açar. |
| **"Son indirdiğim dosya ne?"** | Son indirilen dosyanın adını ve boyutunu seslendirir. |

---

## 🎵 4. Spotify & YouTube Entegrasyonu
| Komut | Açıklama |
| :--- | :--- |
| **"YouTube'da [Video/Şarkı] aç"** / **"YouTube'da [Konu] ara"** | YouTube'da doğrudan ilgili videoyu/aramayı yeni sekmede başlatır. |
| **"[Şarkı adı] çal"** / **"[Şarkı] aç"** / **"Spotify [şarkı]"** | Masaüstü Spotify uygulamasında `Ctrl+L` aramasıyla şarkıyı anında aratıp başlatır. |
| **"Müziği durdur"** / **"Şarkıyı duraklat"** / **"Devam et"** | Oynat/Duraklat kısayolunu tetikler. |
| **"Sıradaki şarkı"** / **"Sonraki parça"** | Bir sonraki parçaya geçer. |

---

## 🎮 5. Eğlence, Mini Oyunlar & Trivia
| Komut | Açıklama |
| :--- | :--- |
| **"Bilgi yarışması başlat"** / **"Trivia oyna"** / **"Bana soru sor"** | Etkileşimli 3 soruluk bilgi yarışması başlatır. Groq AI soruları sorar, cevabınızı dinler, doğruluğunu tartar ve puanınızı tutar! |
| **"Taş kağıt makas oyna"** / **"Taş"** / **"Kağıt"** / **"Makas"** | Jarvis ile sesli taş-kağıt-makas oynarsınız. |
| **"Yazı tura at"** / **"Para çevir"** | Yazı mı tura mı geldiğini söyler. |
| **"Zar at"** | 1 ile 6 arasında zar atar. |
| **"Fıkra anlat"** / **"Espri yap"** | Yazılımcı esprileri ve fıkralar anlatır. |
| **"Motive et"** / **"Günün sözü"** | İlham verici ve Tony Stark alıntıları seslendirir. |

---

## 📈 6. Finans, Kripto Alarmı & Bilgi Alma
| Komut | Açıklama |
| :--- | :--- |
| **"Bitcoin 65000 altına düşerse haber ver"** / **"Kripto alarmı kur"** | Arka planda CoinGecko API ile dakikada bir kontrol eder, hedef fiyat görüldüğünde sesli uyarı verir. |
| **"Döviz fiyatları"** / **"Dolar"** / **"Euro"** / **"Bitcoin"** | Güncel kurları ve kripto değerlerini söyler. |
| **"Wikipedia'da ara [konu]"** / **"[Kişi/Kavram] kimdir/nedir"** | Wikipedia REST API üzerinden resmi Türkçe ansiklopedik özeti çeker. |
| **"Hava durumu"** / **"[Şehir] hava durumu"** | Anlık canlı hava raporunu seslendirir. |

---

## 🖥️ 7. Donanım & Sistem Kontrolleri
| Komut | Açıklama |
| :--- | :--- |
| **"Sistem durumu"** / **"CPU durumu"** / **"RAM kullanımı"** | İşlemci, RAM, Disk ve Pil durumunu canlı raporlar. |
| **Pil Ömrü Göstergesi (HUD)** | Panelde anlık pil yüzdesi ve tahmini kalan süreyi gösterir (Masaüstü için şebeke durumu). |
| **"Sesi aç"** / **"Sesi kıs"** / **"Sessize al"** | Sistem sesini artırır, azaltır veya susturur. |
| **"Parlaklığı kıs"** / **"Parlaklığı yüzde 50 yap"** / **"Parlaklığı fulle"** | Monitör parlaklığını ayarlar. |
| **"Ekran resmi çek"** / **"SS al"** | Masaüstüne yüksek çözünürlüklü ekran yakalama dosyası kaydeder. |
| **"Pencereleri küçült"** / **"Masaüstünü göster"** | Tüm pencereleri simge durumuna küçültür (`Win+D`). |
| **"Bu pencereyi kapat"** / **"Alt F4 yap"** | Aktif pencereyi kapatır (`Alt+F4`). |
| **"Ekranı kilitle"** | Windows oturumunu kilitler. |
| **"Bilgisayarı kapat"** / **"Kapatmayı iptal et"** | 15 saniyelik güvenli geri sayımla kapatır veya iptal eder (`shutdown /a`). |
| **"Bilgisayarı yeniden başlat"** | Bilgisayarı yeniden başlatır. |
| **"Valorant aç"** / **"Valo gir"** | Riot Client'ı açar ve otomatik giriş yapar. |

---

## 🎨 8. Görsel HUD, Temalar & Efektler
- **Fütüristik Daktilo Efekti:** Pencere modunda Jarvis'in yanıtları gerçek bir Tony Stark terminali gibi harf harf akıcı şekilde yazılır.
- **Synthesized Wake Sound:** "Jarvis" veya uyandırma komutu algılandığında saf Python ile sentezlenmiş 44.1kHz repulsor çınlama sesi çalar.
- **Temalar:** 
  - *"Varsayılan tema"* (Stark Arc Cyan)
  - *"Kırmızı tema"* (Mark VII Altın/Kırmızı)
  - *"Yeşil tema"* (Stealth Matrix)
  - *"Mor tema"* (Hulkbuster)
  - *"Midnight tema"* (Gece Mavisi)
