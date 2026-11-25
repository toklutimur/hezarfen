# Tasarım v1 — notlar

**Durum:** Tarihsel kaynaklarda kanadın ölçüsü, biçimi veya malzemesi **yoktur**; döneme ait tasvir bulunamamıştır. Bu tasarımın tamamı `[VARSAYIM]`dır: metindeki "kartal kanatları" ifadesi + dönem malzemeleri + belgelenmiş ilk planör sınıfı (Lilienthal) temel alınmıştır. Amaç "Hezarfen'in kanadı buydu" demek değil, **dönem imkânlarıyla makul bir üst düzey örnek** kurup sınamaktır.

## Dosyalar

| Dosya | İçerik |
|---|---|
| `../hesaplamalar/parametreler.json` | Tek doğruluk kaynağı (`tasarimlar.v1`) |
| `kanat_cizimi.svg` / `.png` | Üst, ön, yan görünüş; `cizim_olustur.py` üretir, PNG Inkscape komut satırıyla dışa aktarıldı |
| `model.blend` | `../hesaplamalar/model_olustur.py` ile üretilen 3B model |

## Ölçüler

| Büyüklük | Değer | Tür | Gerekçe |
|---|---|---|---|
| Açıklık | 7,00 m | VARSAYIM | Lilienthal 6,70 m; tek kişinin taşıyıp koşabileceği sınır |
| Kök veteri / en geniş veter | 2,00 / 2,10 m | VARSAYIM | Kuş kanadı benzeri geniş, kısa plan |
| Plan biçimi | 6 istasyonlu, uçlara doğru geriye süpürülen yuvarlak uç | VARSAYIM | "Kartal kanadı" |
| Alan | 11,92 m² | HESAP | İstasyonlardan |
| Açıklık oranı | 4,11 | HESAP | b²/S |
| Kambur | %7, tek yüzeyli yay | VARSAYIM | Kuş kanadı gözlemi |
| Dihedral | 5° | VARSAYIM | Yalpa kararlılığı |
| Yatay kuyruk | 0,96 m², üçgen, x = 2,6–3,8 m | VARSAYIM | Kuş kuyruğu; Eilmer anlatısındaki "kuyruk eksikliği" dersi |
| Ana kirişler | yarım kanat başına 2 adet, dişbudak, Ø45 → Ø25 mm, veterin %12 ve %55'inde | VARSAYIM | — |
| Nervürler | yarım kanat başına 7 adet, söğüt Ø15 mm | VARSAYIM | — |
| Direk + gergi | 0,9 m üst + 0,9 m alt, Ø30 mm; kendir halat yarı açıklığın ortasına | VARSAYIM | Gergisiz kiriş n = 2'de yetersiz |
| Kaplama | Mumlu keten, 0,30 kg/m² | VARSAYIM | — |
| Pilot | 65 kg, dik duruş, kollar deri halkalarda, x = 0,35 m | VARSAYIM | — |
| Yapı kütlesi | 21,3 kg | HESAP | Hacim × yoğunluk + kaplama + 3 kg bağ |

## Bilinen zayıflıklar

1. Süzülme oranı ≈4,75 (üst sınır); en iyi süzülme hızı stall'ın yalnızca %4 üzerinde.
2. Dik duran pilot ve açık iskelet nedeniyle parazit sürükleme yüksek.
3. Kontrol yalnızca ağırlık kaydırma; yalpa/sapma kontrol yüzeyi yok.
4. Statik pay küçük (+%8 MAC) ve kaba tahmine dayalı; pilot ≈19 cm geriye kayarsa kararsızlaşır.
5. Bağlantılar (sargı düğümler) hesaplanmadı; en olası kırılma noktalarıdır.

## Değişiklik kaydı

- Çizim/model üretilmeden **önce** pilot konumu x = 0,62 → 0,35 m alındı (statik pay −%4 → +%8 MAC). Bundan sonra v1 **dondurulmuştur**; iyileştirmeler `tasarim_v2/` altında ayrı tutulacaktır.
