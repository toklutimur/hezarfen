# Sınırlamalar, sapmalar ve yapılamayanlar

## Görev tanımından sapmalar

1. **Blender sürümü.** Görev "Blender 5 kullanma" diyordu; makinede yalnızca Blender 5.3 kuruluydu. Kullanıcı bu oturumda 5.3 kullanımına açıkça izin verdi. Tüm modeller, simülasyon ve renderlar 5.3 ile üretildi.
2. **Betiklerin yeri.** Çizim ve model betikleri tasarım klasörlerinde değil `hesaplamalar/` altındadır (üç tasarım aynı betiği ve aynı `parametreler.json` dosyasını kullansın diye).
3. **Simülasyon renderı iki oturumda tamamlandı.** Üç tasarımın nihai kare dizisi (10 kare/s, 1280×720) ilk oturumda sistem belleği kritik düzeye indiği için yarıda kesildi (v1 301, v2a 316, v2b 309 kare). Betiğe var olan kareleri atlama eklendi ve kalan kareler sonraki oturumda aynı sahne betiğiyle üretildi; kesim noktasında (ör. v1 301→302) sahne, kamera ve HUD sürekliliği görsel olarak denetlendi. Son durum: v1 423, v2a 698, v2b 1042 kare; keyframe–CSV en büyük sapması sırasıyla 0,0000 / 0,0000 / 0,0001 m. Videolar: `renderlar/animasyon/<kod>_sim.mp4` (42,3 / 69,8 / 104,2 s) ve üç tasarımın alt alta karşılaştırması `karsilastirma_sim.mp4` (640×1080, 104,2 s; erken biten tasarımlar son karede dondurulur). Bu bir sınırlama değil, kayıt amaçlı not olarak tutulmuştur; görselleştirme yalnızca `ucus_verileri.csv`'yi oynatır, fizik modelinin sınırları bu dosyadaki diğer maddelerde geçerlidir.

## Tarihsel araştırmanın sınırları

- Seyahatnâme'nin özgün metnine (yazma ya da tenkitli basım) **doğrudan erişilemedi**; pasaj yalnızca ikincil aktarımlar üzerinden okundu (K1, K3, K4). Aktarımlar arasında rüzgârın yönü konusunda ("lodos ile" / "lodosa karşı") fark vardır.
- Rivayeti destekleyen ya da çürüten çağdaş ikinci bir kayıt bulunamadı; "yok" denemez, "bu araştırmada bulunamadı" denir.
- Tarihçi görüşleri Vikipedi maddesi üzerinden aktarılmıştır; özgün yayınları açılıp doğrulanmadı.
- Kanatların biçimi, ölçüsü, malzemesi hakkında **hiçbir** tarihsel veri yoktur. v1 dahil tüm geometri mühendislik varsayımıdır.
- Erişilemeyen/başarısız kaynak denemeleri `kaynaklar/kaynakca.md` sonunda listelidir.

## Coğrafi verinin sınırları

- Kule zemin kotu 35 m (ikincil kaynak) ile 46–54 m (sayısal yükseklik modeli; şehir içinde çatıları görür) arasında belirsizdir; hesap 35 m ile yapıldı, duyarlılığı incelendi.
- Bugünkü külâh betonarmedir; dönemdeki çatı biçimi ve yüksekliği farklı olabilir. "Külâh ucundan kalkış" fiziksel olarak gerçekçi bir kalkış noktası değildir, iyimser üst sınır olarak alınmıştır.
- Rota boyunca gerçek arazi/kıyı kesiti ölçülmedi. Profil çizimindeki ve Blender sahnesindeki yamaçlar, kıyı konumları ve kule **şematiktir**. v1'in 463 m'lik deniz seviyesi iniş noktası gerçekte suya değil karaya (Galata–Tophane yamacı) denk gelebilir.
- O güne ait rüzgâr ölçümü yoktur; 0 / 8 / 15 m/s varsayımdır.

## Fizik modelinin sınırları

- Dengeli (sabit hızlı, sabit açılı) süzülme varsayıldı: kalkıştaki hızlanma evresi, iniş palyesi, dönüşler ve türbülans yok. Kalkış evresi gerçek menzili daha da kısaltır.
- Aerodinamik katsayılar (CD0, e, CLmax) ölçülmedi; Lilienthal planörünün belgelenmiş süzülme oranına (≈4) kalibre edilmiş varsayımlardır. **CFD yapılmadı**, rüzgâr tüneli verisi yok.
- Esnek kumaş kanadın yük altında biçim değiştirmesi, kaplamanın geçirgenliği, flutter modellenmedi.
- Yapı hesabı tek kirişli basit eğilmedir; bağlantı yerleri (kendir bağlar), burkulma, yorulma ve ahşap kusurları yoktur. Gerçek güvenlik payı hesaplanandan düşüktür.
- Kararlılık yalnızca boylamasına statik pay olarak tahmin edildi; yanal/yön kararlılığı ve kontrol edilebilirlik sayısal olarak incelenmedi.
- Yükselen hava ve rüzgâr düzgün ve sabit kabul edildi.
- v2b'nin kütlesi varsayımdır, yapısı hesaplanmadı.
- Blender simülasyonu bu analitik modelin canlandırmasıdır; bağımsız bir fizik çözümü değildir. Planörün sahnedeki burun açısı süzülme açısına eşitlenmiştir (hücum açısı gösterilmez).

## Yapılmayanlar

- Fiziksel deneme, prototip, ölçüm (görev gereği yasak).
- Giriş/üyelik/ödeme isteyen kaynaklar açılmadı.
- Rivayetin tarihsel olarak gerçekleşip gerçekleşmediğine dair kesin hüküm verilmedi; veri buna izin vermiyor.
