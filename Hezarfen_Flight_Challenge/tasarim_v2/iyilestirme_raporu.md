# Tasarım v2 — iyileştirme raporu

v1 dondurulmuştur ve değiştirilmemiştir (`tasarim_v1/`). v2 iki ayrı kolda tutulur:

- **v2a — dönem malzemesiyle** (`tasarim_v2/v2a/`): dişbudak kiriş, söğüt nervür, mumlu keten, kendir gergi. Malzeme dönemin elindedir; **geometri seçimleri ise modern aerodinamik bilgiye dayanır** (yüksek açıklık oranı, yatay pilot, gergili kiriş). Bu yüzden v2a "dönemde yapılabilir", ama "dönemde tasarlanabilir" olduğu gösterilmiş değildir. `[VARSAYIM]`
- **v2b — modern karşılaştırma** (`tasarim_v2/v2b/`): alüminyum boru, sentetik kaplama, çelik tel. **Tarihsel değildir**; yalnızca "bugünün basit bir yelken kanadı aynı rotada ne yapardı?" sorusunun üst sınırıdır. Yapı kütlesi (32 kg) hesaplanmamış, varsayılmıştır; kiriş mukavemeti modellenmemiştir.

Tüm sayılar `hesaplamalar/aerodinamik.py` çıktısıdır (`ozet.json`, `sonuclar.csv`).

## 1. Ne değişti, neden

| Parametre | v1 | v2a | v2b | Gerekçe |
|---|---|---|---|---|
| Kanat açıklığı b (m) | 7,00 | 10,00 | 10,50 | İndüklenmiş sürükleme ∝ 1/AR |
| Kanat alanı S (m²) | 11,92 | 16,21 | 14,88 | Kanat yüklemesini düşürür → daha düşük hız |
| Açıklık oranı AR | 4,11 | 6,17 | 7,41 | (L/D)max ∝ √AR |
| Pilot duruşu | dik (asılı) | yatay | yatay | Parazit sürükleme: CD0 0,10 → 0,07 → 0,035 `[VARSAYIM]` |
| Oswald e | 0,70 | 0,75 | 0,85 | Daha düzgün plan biçimi `[VARSAYIM]` |
| CLmax | 1,0 | 1,1 | 1,3 | Daha belirgin kambur / gergin kaplama `[VARSAYIM]` |
| Yapı kütlesi (kg) | 21,3 (hesap) | 39,8 (hesap) | 32,0 (varsayım) | Açıklık büyüdükçe ahşap kiriş ağırlaşır |
| Uçuş kütlesi (kg) | 86,3 | 104,8 | 97,0 | pilot 65 kg `[VARSAYIM]` |
| Kanat yüklemesi (N/m²) | 71,0 | 63,4 | 63,9 | |
| Statik kararlılık payı (% MAC) | +8 | +9 | +7 | Pilot konumu ile ayarlandı |

## 2. Sonuç farkı (nominal senaryo: kule tepesi → Doğancılar, 3360 m, Δh 51,6 m, gereken oran 65:1)

| Büyüklük | v1 | v2a | v2b |
|---|---|---|---|
| Süzülme oranı L/D | 4,75 | 7,20 | 11,89 |
| Süzülme açısı (°) | 11,9 | 7,9 | 4,8 |
| Hava hızı / stall hızı (m/s) | 11,2 / 10,8 | 10,2 / 9,7 | 11,2 / 9,0 |
| Batış hızı (m/s) | 2,31 | 1,40 | 0,94 |
| Menzil, sakin hava (m) | 245 | 372 | 613 |
| Menzil, lodos 8 m/s (m) | 287 | 432 | 720 |
| Menzil / gereken mesafe | %7 | %11 | %18 |
| Havada kalış, hedef kotuna kadar (s) | 22 | 37 | 55 |
| Rota boyunca gereken sürekli yükselen hava (m/s) | ≈2,1 | ≈1,2 | ≈0,8 |
| Kiriş güvenlik katsayısı, gergili, n=2 | 2,36 | 2,89 | modellenmedi |
| Hedefe ulaşır mı? | hayır | hayır | hayır |

v1 → v2a: L/D +%52, menzil +%52, batış −%39; bedeli yapı kütlesinde +18,5 kg.
v1 → v2b: L/D +%150, menzil +%150.

En iyimser birleşim bile (v2b, kule tepesi → **Üsküdar kıyısı, deniz seviyesi**, lodos 8 m/s) 1334 m ile 3423 m'nin %39'unda kalır.

## 3. Neden daha fazla deneme yapılmadı

Gereken süzülme oranı senaryoya göre 36–116:1'dir. v2a 7,2'de, v2b 11,9'da kalır; kaynakçadaki modern üst sınır (K12) esnek kanat için ≈17:1, rijit kanat için ≈20:1'dir. Aradaki fark geometri ayarıyla kapanacak mertebede değildir (en az 2–3 kat), bu yüzden v2c, v2d… üretmek ilerleme sağlamaz; görev tanımındaki "ilerleme sağlamayan denemeleri çoğaltma" kuralı uygulanmıştır.

## 4. Dosyalar

- `v2a/kanat_cizimi.svg|png`, `v2a/model.blend`
- `v2b/kanat_cizimi.svg|png`, `v2b/model.blend`
- Parametreler: `hesaplamalar/parametreler.json` → `tasarimlar.v2a`, `tasarimlar.v2b`
- Modeller ölçü denetimi (betik çıktısı): v2a açıklık 10,001 m (JSON 10,000), v2b 10,500 m (JSON 10,500); boy farkı ≈2 cm = kuyruk kirişi uç yarıçapı.
