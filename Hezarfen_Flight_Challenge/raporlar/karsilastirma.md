# Sayısal karşılaştırma — v1 / v2a / v2b

Kaynak: `hesaplamalar/ozet.json`, `hesaplamalar/sonuclar.csv`, `simulasyon/ucus_verileri.csv`. Tümü `[HESAP]`; girdilerin hangileri `[VARSAYIM]` olduğu `hesaplamalar/parametreler.json` içinde işaretlidir.

## Tasarım ve performans

| Parametre | v1 (ilk rekonstrüksiyon) | v2a (dönem malzemesi) | v2b (modern, tarihsel değil) |
|---|---|---|---|
| Kanat açıklığı (m) | 7,00 | 10,00 | 10,50 |
| Kanat alanı (m²) | 11,92 | 16,21 | 14,88 |
| Açıklık oranı | 4,11 | 6,17 | 7,41 |
| Yapı kütlesi (kg) | 21,3 | 39,8 | 32,0 (varsayım) |
| Uçuş kütlesi (kg) | 86,3 | 104,8 | 97,0 |
| Kanat yüklemesi (N/m²) | 71,0 | 63,4 | 63,9 |
| Süzülme oranı L/D | 4,75 | 7,20 | 11,89 |
| Uçuş (hava) hızı (m/s) | 11,2 | 10,2 | 11,2 |
| Stall hızı (m/s) | 10,8 | 9,7 | 9,0 |
| Batış hızı (m/s) | 2,31 | 1,40 | 0,94 |
| Statik kararlılık payı (% MAC) | +8 | +9 | +7 |
| Kiriş güvenlik katsayısı (gergili, n=2) | 2,36 | 2,89 | modellenmedi |

## Süzülme mesafesi (m) — hedef kotuna inene kadar

| Senaryo (gereken mesafe; gereken oran) | Lodos | v1 | v2a | v2b |
|---|---|---|---|---|
| N: kule tepesi → Doğancılar (3360 m; 65:1) | 0 m/s | 245 | 372 | 613 |
| | 8 m/s | 287 | 432 | 720 |
| | 15 m/s | 178* | 294* | 438* |
| K: en üst kat → Doğancılar (3360 m; 116:1) | 0 | 138 | 209 | 345 |
| | 8 | 162 | 243 | 405 |
| S: kule tepesi → Üsküdar kıyısı, deniz seviyesi (3423 m; 36:1) | 0 | 454 | 689 | 1136 |
| | 8 | 532 | 800 | 1334 |
| I: ikincil kaynaktaki 127,9 m iddiası (3360 m; 41:1) | 0 | 389 | 590 | 974 |
| | 8 | 456 | 685 | 1143 |

\* 15 m/s lodosta yan rüzgâr bileşeni (≈%85) hava hızını aşar ya da ona yaklaşır; rota tutulamaz, değer rota doğrultusundaki izdüşümdür.

## Hedefe ulaşma

| | v1 | v2a | v2b |
|---|---|---|---|
| Herhangi bir senaryoda hedefe ulaşıyor mu? | Hayır | Hayır | Hayır |
| En iyi durumda katedilen pay | %16 (S, 8 m/s) | %23 (S, 8 m/s) | %39 (S, 8 m/s) |
| Nominal senaryoda katedilen pay | %7 | %11 | %18 |
| Nominal senaryo için gereken sürekli yükselen hava (m/s) | ≈2,1 | ≈1,2 | ≈0,8 |
| Yalnız arka rüzgârla kapatmak için gereken rüzgâr bileşeni (m/s) | ≈139 | ≈81 | ≈50 |

Son satırın hesabı: gereken yer hızı = gereken oran × batış hızı (65,1 × 2,31 = 150 m/s vb.), eksi yatay hava hızı. Bunlar kasırga mertebesinin üzerindedir; fiziksel olarak anlamlı bir çözüm değildir.

Görsel karşılaştırma: `simulasyon/ucus_profili.png`.
