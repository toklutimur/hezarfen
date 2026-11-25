# Hezarfen Flight Challenge

Hezarfen Ahmed Çelebi'ye atfedilen Galata Kulesi → Üsküdar uçuşu rivayetinin kaynak eleştirisi, mühendislik rekonstrüksiyonu ve fizik sınaması. Yalnızca dijital model ve teorik analiz; fiziksel deneme yoktur.

## Durum

| Aşama | Durum | Çıktı |
|---|---|---|
| A0 Klasör iskeleti | ✔ | bu dosya |
| A1 Tarihsel araştırma | ✔ | `kaynaklar/`, `arastirma/` |
| A2 Tasarım v1 + teknik çizim | ✔ | `tasarim_v1/kanat_cizimi.svg`, `.png`, `tasarim_notlari.md` |
| A3 Hesaplamalar | ✔ | `hesaplamalar/aerodinamik.py`, `sonuclar.csv`, `duyarlilik_*.csv`, `ozet.json`, `fizik_raporu.md` |
| A4 Uçuş senaryosu | ✔ | `fizik_raporu.md` §3, `arastirma/tarihsel_teknoloji.md` §3 |
| A5 Blender modeli v1 + tek önizleme | ✔ (kullanıcı onayladı) | `tasarim_v1/model.blend`, `renderlar/onizleme/v1_onizleme.png` |
| A6 Süzülme simülasyonu | ✔ | `simulasyon/simulasyon.py`, `ucus_verileri.csv`, `ucus_profili.svg|png`, `sahne_olustur.py`, `sim_<kod>.blend`, `onizleme/`; kareler `renderlar/animasyon/<kod>_sim/`, videolar `renderlar/animasyon/<kod>_sim.mp4` ve üç tasarım alt alta `karsilastirma_sim.mp4` |
| A7 v1 hükmü | ✔ | `raporlar/nihai_degerlendirme.md` §A |
| A8 Tasarım v2 | ✔ | `tasarim_v2/v2a/`, `tasarim_v2/v2b/`, `tasarim_v2/iyilestirme_raporu.md` |
| A9 Nihai Cycles renderları + turntable | ✔ | `renderlar/nihai/<kod>_*.png`, `renderlar/animasyon/<kod>_turntable.mp4` |
| A10 Raporlar | ✔ | `raporlar/nihai_degerlendirme.md`, `karsilastirma.md`, `sinirlamalar.md` |

**Sonuç (özet):** gereken süzülme oranı 36–116:1; v1 4,75, v2a 7,20, modern v2b 11,89. Hiçbiri hedefe ulaşmıyor. Ayrıntı: `raporlar/nihai_degerlendirme.md`.

## Yeniden üretim

```
python hesaplamalar/aerodinamik.py
python hesaplamalar/cizim_olustur.py v2a tasarim_v2/v2a/kanat_cizimi.svg
"C:/Program Files/Inkscape/bin/inkscape.com" tasarim_v2/v2a/kanat_cizimi.svg --export-type=png --export-filename=tasarim_v2/v2a/kanat_cizimi.png --export-width=2400
blender -b --python hesaplamalar/model_olustur.py -- v2a
python simulasyon/simulasyon.py
blender -b --python simulasyon/sahne_olustur.py -- v1 24 onizleme
blender -b --python simulasyon/sahne_olustur.py -- v1 10 nihai
blender -b tasarim_v1/model.blend --python renderlar/nihai_render.py -- v1
```
(`blender` = `C:/Program Files/Blender Foundation/Blender 5.3/blender.exe`; kod: `v1`, `v2a`, `v2b`.)

Simülasyon videoları (nihai modda var olan kareler atlanır; kesilen render aynı komutla kaldığı yerden sürer):
```
ffmpeg -framerate 10 -i renderlar/animasyon/<kod>_sim/%04d.png -c:v libx264 -pix_fmt yuv420p -crf 18 renderlar/animasyon/<kod>_sim.mp4
ffmpeg -i renderlar/animasyon/v1_sim.mp4 -i renderlar/animasyon/v2a_sim.mp4 -i renderlar/animasyon/v2b_sim.mp4 -filter_complex "[0]scale=640:360,tpad=stop_mode=clone:stop=-1[a];[1]scale=640:360,tpad=stop_mode=clone:stop=-1[b];[2]scale=640:360[c];[a][b][c]vstack=inputs=3[v]" -map "[v]" -frames:v 1042 -r 10 -c:v libx264 -pix_fmt yuv420p -crf 18 renderlar/animasyon/karsilastirma_sim.mp4
```
`renderlar/animasyon/fragman_kismi.mp4`, aynı dikey düzenin kısmi karelerle (316 kare) üretilmiş eski sürümüdür; yerini `karsilastirma_sim.mp4` almıştır.

**v1 dondurulmuştur.** `tasarim_v1/kanat_cizimi.svg|png` ve `model.blend`, v2 için betiklere eklenen genellemelerden *önce* üretilmiştir; yeniden üretilirse ölçüler aynı kalır ama etiket yerleşimi/kamera kadrajı değişebilir. Bu yüzden v1 çıktıları yeniden üretilmemiştir.

Tek doğruluk kaynağı `hesaplamalar/parametreler.json`'dur; çizim, hesap, 3B model ve simülasyon aynı dosyayı (ve ondan türeyen `ozet.json`'u) okur.

## Görevden sapmalar

- **Blender sürümü:** Görev metni Blender 5 kullanılmamasını ister. Makinede yalnızca Blender 5.3.0 kuruludur; kullanıcı bu oturumda 5.3 kullanımına açıkça izin vermiştir.
- **Betik konumu:** Çizim ve model betikleri sürümler arasında ortak kullanıldığı için `tasarim_v1/` yerine `hesaplamalar/` altındadır.
- Seyahatnâme'nin özgün metnine ve hakemli makalelere erişilemedi (ayrıntı: `kaynaklar/kaynakca.md`).
