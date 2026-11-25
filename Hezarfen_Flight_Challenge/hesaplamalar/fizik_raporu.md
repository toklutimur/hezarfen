# Fizik raporu — v1

Yeniden üretim: `python hesaplamalar/aerodinamik.py` → `sonuclar.csv`, `duyarlilik_v1.csv`, `ozet.json`.
Tüm girdiler `parametreler.json` içindedir ve `OLCUM / KAYNAK / HESAP / VARSAYIM` etiketlidir. Birimler SI.
Bu bir **basitleştirilmiş nokta-kütle süzülme modelidir; CFD veya uçuş testi değildir.**

## 1. Denklemler ve geçerlilik koşulları

| Büyüklük | Denklem | Geçerlilik |
|---|---|---|
| Taşıma, sürükleme | L = ½ρV²S·C_L, D = ½ρV²S·C_D | Sürekli, sıkıştırılamaz akış |
| Sürükleme poları | C_D = C_D0 + C_L²/(π·e·AR) | Stall'dan uzak; parabolik yaklaşım. İnce, sızdıran, esneyen bez kanat için kabadır |
| En iyi süzülme | (L/D)max = ½·√(π·e·AR / C_D0), C_L* = √(C_D0·π·e·AR) | C_L* ≤ C_Lmax ise. Değilse 0,9·C_Lmax'ta uçulur (stall sınırlı) |
| Denge süzülmesi | tan γ = 1/(L/D), V = √(2W·cos γ / (ρ·S·C_L)), batış = V·sin γ | Sabit hız, ivmesiz, durgun veya düzgün rüzgâr |
| Menzil | R = Δh·(L/D) (durgun hava); rüzgârda yer hızı × süre | Kalkış geçişi ve iniş manevrası yok sayılır (rivayet lehine) |
| Rüzgâr | Rota boyunca ve rotaya dik bileşen; dik bileşen yengeç açısıyla karşılanır | Düzgün rüzgâr; türbülans, kule ardı girdap yok |
| Kiriş eğilmesi | σ = M/Z, Z = πd³/32; konsol M = wL²/2, gergili açıklıkta M ≈ wL²/8 | Düzgün yayılı yük, lineer elastik, kusursuz ağaç |
| Statik kararlılık | Pay = (x_NN − x_AM)/MAC | Kaba tahmin: kuyruk etkinliği 0,5, yapı AM'si x_ac + 0,20·MAC varsayımı |

## 2. v1 temel sonuçlar

| Büyüklük | Değer | Tür |
|---|---|---|
| Kanat alanı S / açıklık b / AR / MAC | 11,92 m² / 7,00 m / 4,11 / 1,81 m | HESAP |
| Yapı kütlesi (kirişler 9,41 + nervür 1,90 + kuyruk kirişi 2,22 + direk 0,87 + kaplama 3,86 + bağ 3,00) | 21,3 kg | HESAP |
| Pilot | 65 kg (55–80) | VARSAYIM |
| Uçuş kütlesi / ağırlık | 86,3 kg / 846 N | HESAP |
| Kanat yüklemesi W/S | 71,0 N/m² | HESAP |
| C_D0 / e / C_Lmax | 0,10 / 0,70 / 1,0 | VARSAYIM |
| Süzülme oranı L/D | **4,75** (stall sınırlı, C_L = 0,90) | HESAP |
| Süzülme hızı / stall hızı | 11,2 / 10,8 m/s | HESAP |
| Batış hızı / süzülme açısı | 2,31 m/s / 11,9° | HESAP |
| L / D (dengede) | 828 N / 174 N | HESAP |

Elle sağlama: R = Δh·L/D = 51,59 × 4,75 = 245 m (betik: 244,9 m). W = 86,26 × 9,80665 = 846 N. ✔

**Hız payı uyarısı:** En iyi süzülme hızı stall hızının yalnızca %4 üzerindedir. Göstergesiz, türbülanslı havada bu noktada uçmak gerçekçi değildir; pilot ya daha hızlı (daha kötü L/D) uçar ya da stall'a girer. 4,75 bu nedenle **üst sınırdır**.

## 3. Uçuş senaryoları

Rota yönü 102,9°. Lodos 225°'den eser → rota boyunca arka bileşen hızın %53'ü, yan bileşen %85'i.

| Senaryo | Kalkış → iniş kotu (m) | Δh (m) | Mesafe (m) | **Gereken L/D** |
|---|---|---|---|---|
| N — külâh ucu → Doğancılar (nominal) | 97,6 → 46 | 51,6 | 3360 | **65** |
| K — en üst kat → Doğancılar (kötümser) | 75,0 → 46 | 29,0 | 3360 | **116** |
| S — külâh ucu → Üsküdar kıyısı | 97,6 → 2 | 95,6 | 3423 | **36** |
| I — ikincil kaynağın 127,9 m iddiası → Doğancılar | 127,9 → 46 | 81,9 | 3360 | **41** |

v1'in ulaştığı menzil (m) ve hedef mesafeye oranı:

| Senaryo | Sakin | Lodos 8 m/s | Lodos 15 m/s | Uçuş süresi |
|---|---|---|---|---|
| N | 245 (%7,3) | 287 (%8,6) | 178 (%5,3)* | 22 s |
| K | 138 (%4,1) | 162 (%4,8) | 100 (%3,0)* | 13 s |
| S | 454 (%13,3) | 532 (%15,6) | 329 (%9,6)* | 41 s |
| I | 389 (%11,6) | 456 (%13,6) | 282 (%8,4)* | 35 s |

\* 15 m/s'de yan bileşen (12,7 m/s) uçuş hızını (11,2 m/s) aşar: **rota tutulamaz**, araç kuzeydoğuya sürüklenir; verilen değer rota doğrultusundaki izdüşümdür.

Hiçbir senaryoda hedefe ulaşılmaz. En iyi durumda (kıyıya iniş, 8 m/s lodos) mesafenin %16'sı kat edilir; araç Haliç ağzı / Boğaz'a iner.

**Rüzgâr neden kurtarmaz:** Uçuş 13–41 s sürer. Arka rüzgâr menzile yalnızca (arka bileşen × süre) ekler: 8 m/s lodosta +42…+79 m.

**Gereken yükselen hava:** 3,4 km'yi mevcut irtifayla geçmek için rota boyunca **kesintisiz ≈2,0–2,2 m/s** yükselen hava gerekir (uçuş ≈5 dakika sürerdi). Açık su üzerinde böyle sürekli bir yükselme için fiziksel mekanizma yoktur; yamaç yükselticisi yalnızca kule/Galata sırtı yakınında oluşur.

## 4. Duyarlılık (N senaryosu, sakin hava, nominal 245 m)

| Parametre | Aralık | Menzil (m) | Salınım (m) |
|---|---|---|---|
| C_D0 | 0,06 … 0,14 | 317 … 202 | 114 |
| Kalkış noktası (üst kat / külâh ucu) | Δh 29,0 … 51,6 | 138 … 245 | 107 |
| Kule zemin kotu | 35 … 54 m | 245 … 335 | 90 |
| Oswald e | 0,55 … 0,85 | 217 … 267 | 50 |
| İniş kotu | 54 … 44 m | 207 … 254 | 47 |
| C_Lmax | 0,8 … 1,3 | 236 … 245 | 9 |
| Pilot kütlesi | 55 … 80 kg | 245 | 0 |
| Yapı kütlesi | −%30 … +%50 | 245 | 0 |
| Hava yoğunluğu | 1,15 … 1,29 | 245 | 0 |

- Sonucu en çok etkileyen: **parazit sürükleme (C_D0)** ve **kalkış irtifası**.
- Kütle ve hava yoğunluğu durgun havada menzili **değiştirmez**; yalnızca hızı (√(W/S)) değiştirir. Daha hafif pilot daha yavaş uçar ama aynı açıyla iner.
- Tüm belirsizlikler aynı anda en iyimser uçta alınsa bile menzil yüzlerce metre mertebesinde kalır; gereken 3360 m ile arada **bir büyüklük mertebesi** fark vardır. Sonuç varsayımlara duyarlı değildir.

## 5. Yapısal kontrol

| Durum | 1 g gerilme | Güvenlik payı (1 g) | Güvenlik payı (n = 2) |
|---|---|---|---|
| Gergisiz (konsol) kirişler | 41,4 MPa | 2,50 | 1,25 |
| Direk + kendir gergili | 22,0 MPa | 4,71 | 2,36 |

Referans: dişbudak kopma modülü 103,6 MPa (kusursuz küçük numune, K14). Budak, nem, el işçiliği ve sargı bağlantılar gerçek dayanımı belirgin biçimde düşürür; gergisiz yapı sağanakta **yetersiz** sayılmalıdır. Burkulma, burulma, bağlantı dayanımı ve bez gerginliği **hesaplanmamıştır**.

## 6. Denge ve kontrol

- x_AM = 0,48 m, x_NN = 0,62 m → statik pay **+%8 MAC** (kaba tahmin). z_AM = −0,41 m (sarkaç etkisi).
- İlk yerleşimde (pilot x = 0,62 m) pay −%4 MAC çıkmış, pilot öne alınarak düzeltilmiştir. Bu, dönemin bir yapımcısının **ancak deneme-yanılmayla** bulabileceği bir ayardır; rivayetteki Okmeydanı talimleri bununla tutarlıdır ama bunu kanıtlamaz.
- Kontrol yalnızca ağırlık kaydırma. Lilienthal deneyimi (K9) bu yöntemin sağanakta yetersiz kaldığını gösterir. Dinamik kararlılık, yalpa/sapma ve kule ardı türbülans **modellenmemiştir**.
- İniş: yer hızı ≈11–13 m/s (≈40–46 km/sa), batış 2,3 m/s. Palamar (flare) başarılı olmazsa ciddi yaralanma beklenir.

## 7. Modellenmeyenler

Kalkıştaki hızlanma kaybı (atlayışta ilk metrelerde irtifa kaybedilir), kule ardı türbülans, bezin sızdırması ve şişmesi, kanat esnemesi, pilot kol kuvvetleri (846 N'luk yükün kollarla/koşumla taşınması), dinamik kararlılık. Bunların hepsi performansı **düşürür**; dolayısıyla yukarıdaki menziller iyimser taraftadır.

---

## Ek: v2 tasarımları ve simülasyon

Bu rapor v1 için yazılmıştır. Aynı denklemler ve aynı betik (`aerodinamik.py`) v2a ve v2b için de çalıştırılmıştır; girdileri `parametreler.json`, çıktıları `ozet.json`, `sonuclar.csv`, `duyarlilik_v2a.csv`, `duyarlilik_v2b.csv` içindedir.

| | v1 | v2a | v2b |
|---|---|---|---|
| L/D | 4,75 | 7,20 | 11,89 |
| V / V_stall (m/s) | 11,2 / 10,8 | 10,2 / 9,7 | 11,2 / 9,0 |
| Batış (m/s) | 2,31 | 1,40 | 0,94 |
| Nominal menzil (m) | 245 | 372 | 613 |

Yorum ve karşılaştırma: `tasarim_v2/iyilestirme_raporu.md`, `raporlar/karsilastirma.md`.

Simülasyon (`simulasyon/simulasyon.py`) yeni bir fizik çözmez: yukarıdaki dengeli süzülme değerlerini x(t) = V_yer·t, z(t) = h0 − batış·t zaman serisine çevirir ve hedef kotunun altına indikten sonra deniz seviyesine kadar sürdürür. Blender sahnesindeki keyframe'ler bu CSV'den okunur; betik keyframe–CSV sapmasını denetler (v1 için ölçülen en büyük sapma 0,0000 m). CFD değildir.
