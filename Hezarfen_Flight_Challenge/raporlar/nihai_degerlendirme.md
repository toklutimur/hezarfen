# Nihai değerlendirme

Etiketler: **[RİVAYET]** tarihsel anlatı · **[DOĞRULANMIŞ]** birden çok bağımsız kaynakla desteklenen bilgi · **[MODERN YORUM]** bugünkü yazarların görüşü · **[VARSAYIM]** bu projenin mühendislik kabulü · **[HESAP]** `hesaplamalar/aerodinamik.py` çıktısı. Kaynak kodları (K1…K14) `kaynaklar/kaynakca.md` içindedir.

## Kısa hüküm

- **Tarihsel olarak:** uçuşun gerçekleştiği doğrulanamıyor; tek kaynağa dayanan bir rivayettir.
- **Fiziksel olarak:** burada kurulan hiçbir tasarım — dönem malzemesiyle iyileştirilmiş olan da, modern karşılaştırma kanadı da — Galata Kulesi'nden Üsküdar'a **süzülerek ulaşamıyor**. Gereken süzülme oranı 36–116:1, elde edilen 4,8 – 7,2 – 11,9.
- **Açık kalan:** kuleden atlayıp birkaç yüz metre süzülmek fiziksel olarak mümkündür. Rivayetin çekirdeğinde böyle bir olay bulunup bulunmadığı bu verilerle **belirsizdir**.

---

## A. İlk tasarımın (v1) bilimsel yargısı

**Soru: Bu kanat, belirtilen koşullarda Galata'dan Üsküdar'a süzülebilir mi? — Hayır.**

| Alt soru | Değerlendirme | Sayı |
|---|---|---|
| Yeterli kaldırma üretilebilir mi? | **Evet.** 846 N ağırlık, 11,2 m/s hızda CL = 0,90 ile taşınır. Sorun kaldırma değil, sürüklemedir. | S = 11,92 m², W/S = 71 N/m², stall 10,8 m/s |
| Süzülme oranı yeterli mi? | **Hayır**, 14–24 kat eksik. | L/D = 4,75; gereken 65:1 (nominal), 36–116:1 (aralık) |
| Kanatlar ağırlığı taşır mı? | **Kâğıt üzerinde evet, pay dar.** Gergisiz konsol kirişte n=2 yükünde güvenlik 1,25; gergili 2,36. Bağlantılar hesapta yok. | dişbudak kopma modülü 103,6 MPa (K14) |
| Pilot aracı kontrol edebilir mi? | **Belirsiz, muhtemelen zayıf.** Statik pay +%8 MAC, pilotun ≈19 cm geri kayması kararsızlığa götürür. Yalnız ağırlık kaydırma; Lilienthal aynı yöntemle stall'dan öldü (K9). Hava hızı stall'ın yalnızca %4 üstünde. | V/Vs = 1,04 |
| Kalkış gerçekçi mi? | **Hayır / çok riskli.** Külâh ucu erişilebilir bir kalkış yeri değildir; balkondan atlayışta 11 m/s'ye ulaşmak için ≈6 m serbest düşüş gerekir ve taş gövdeye çarpma riski vardır. | en üst kat senaryosunda menzil 138 m |
| Hız ve iniş güvenli mi? | **Hayır.** ≈40 km/h yatay, 2,3 m/s düşey hızla, palye imkânı kısıtlı; kırık beklenir (Eilmer rivayetiyle aynı mertebe, K10). Lodosta yer hızı 13 m/s'ye çıkar. | batış 2,31 m/s ≈ 0,27 m'den serbest düşüş |
| Hangi nedenle başarısız olur? | Menzil: 245 m'de hedef kotunun altına iner, ≈460 m'de deniz seviyesindedir (hedef 3360 m). İkincil: stall, yan rüzgâr (15 m/s lodosta rota tutulamaz), yapısal bağlantılar. | katedilen pay %7 |
| Sonuç hangi varsayımlara bağlı? | En etkili: CD0 (menzil 202–317 m), kalkış noktası (138–245 m), zemin kotu (245–335 m). Hiçbiri sonucu "ulaşır"a çevirmez; en iyimser birleşim %16'da kalır. | `duyarlilik_v1.csv` |

v1'in süzülme oranı (4,75), belgelenmiş Lilienthal planörünün ≈4 değeriyle (K8) aynı mertebededir; yani v1 "kötü tasarlanmış" değil, o teknoloji sınıfının tipik örneğidir.

---

## B. On soru

### 1. Tarihsel kanıtların güvenilirliği nedir?
**Düşük.** Olayın bilinen **tek** kaynağı Evliya Çelebi'nin Seyahatnâme'sidir [DOĞRULANMIŞ: K1, K3, K4 bağımsız olarak aynı tespiti yapar]. Çağdaş ikinci bir tanıklık, resmî kayıt ya da rivayetteki ödülün maliye kaydı bu araştırmada bulunamadı [K4 aktarımı]. Seyahatnâme'nin abartı ve anlatı süslemesi içerdiği tarihçilerce kabul edilir [MODERN YORUM]. Özgün metne doğrudan erişilemedi; pasaj ikincil aktarımlardan okundu ve aktarımlar rüzgâr yönünde bile birbirini tutmuyor. Sayıyla: bağımsız kaynak sayısı = 1, doğrulayan belge = 0.

### 2. Kanatların özgün tasarımı hakkında gerçekten ne biliyoruz?
**Hiçbir şey ölçülebilir düzeyde.** Rivayet yalnızca "kartal kanatları" der [RİVAYET]; açıklık, alan, malzeme, bağlantı, kuyruk, pilotun duruşu verilmez. Döneme ait çizim ya da nesne yoktur; dolaşımdaki görseller modern temsildir (`kaynaklar/gorsel_kaynaklari.md`). Bilinen parametre sayısı = 0; v1'deki her ölçü [VARSAYIM].

### 3. İlk rekonstrüksiyon fiziksel olarak uçabilir mi?
**Süzülebilir, ama kısa.** [HESAP] L/D 4,75, hava hızı 11,2 m/s, batış 2,31 m/s. Kule tepesinden sakin havada hedef kotuna kadar 245 m / 22 s; deniz seviyesine kadar ≈460 m / 42 s. Kaldırma ve (gergili) yapı yeterli; kontrol ve iniş güvenliği zayıf.

### 4. Galata–Üsküdar mesafesi için hangi koşullar gerekir?
Yatay 3360 m, kullanılabilir irtifa farkı 51,6 m (kule tepesi 97,6 m → Doğancılar 46 m) [HESAP; K5, K6, K7]. Gerekenlerden **biri**:
- süzülme oranı ≥ 65:1 (kıyıya inişte ≥ 36:1; en üst kattan ≥ 116:1) — bugünün en iyi yelken kanatları 17–20:1 (K12);
- ya da rota boyunca **kesintisiz** yükselen hava: v1 için ≈2,1 m/s, v2a ≈1,2 m/s, v2b ≈0,8 m/s — 3,4 km'lik açık su üzerinde bunu sağlayacak bir mekanizma (yamaç, güçlü termik) beklenmez;
- ya da arka rüzgâr bileşeni ≈139 m/s (v1), ≈81 m/s (v2a), ≈50 m/s (v2b) — fiziksel olarak anlamsız.
Lodos güneybatıdan eser; rota doğu-güneydoğuya (≈103°) gittiği için rüzgârın yalnızca ≈%53'ü arkadan, ≈%85'i yandan gelir. 8 m/s lodos menzili yalnızca %17 artırır.

### 5. İlk tasarımın en büyük mühendislik problemi nedir?
**Süzülme oranı.** Düşük açıklık oranı (4,1) ve dik asılı pilot + açık iskeletin yüksek parazit sürüklemesi (CD0 = 0,10) L/D'yi 4,75'te tutar; üstelik en iyi süzülme noktası stall sınırının ötesinde kaldığı için araç stall'a %4 mesafede uçmak zorundadır. İkinci sırada: yalnız ağırlık kaydırmayla kontrol.

### 6. İkinci tasarım hangi parametreleri iyileştirdi?
v2a (dönem malzemesi): açıklık 7,0 → 10,0 m, alan 11,9 → 16,2 m², açıklık oranı 4,1 → 6,2, yatay pilotla CD0 0,10 → 0,07. Sonuç: L/D 4,75 → 7,20 (+%52), batış 2,31 → 1,40 m/s (−%39), nominal menzil 245 → 372 m. Bedel: yapı kütlesi 21 → 40 kg. v2b (modern, tarihsel değil): L/D 11,89, batış 0,94 m/s, menzil 613 m. Ayrıntı: `tasarim_v2/iyilestirme_raporu.md`.

### 7. Yeniden tasarlanan araç hedeflenen uçuşu teorik olarak gerçekleştirebilir mi?
**Hayır.** v2a nominal senaryoda mesafenin %11'ini, en iyimser senaryoda %23'ünü kateder. Modern v2b bile %18 / %39'da kalır. Gereken mesafe ile katedilen arasındaki fark v2a için 4,3–9 kat, modern v2b için 2,6–5,5 kattır.

### 8. Dönemin teknolojisiyle böyle bir araç ne kadar gerçekçi?
**Malzeme ve işçilik açısından gerçekçi, tasarım bilgisi açısından değil.** Dişbudak, söğüt, keten, kendir ve bunları işleyecek marangozluk/yelkencilik dönemde vardı; v1 sınıfı bir kanat (21 kg, 7 m) yapılabilirdi [VARSAYIM, `arastirma/tarihsel_teknoloji.md`]. Ama kamburlu profil, açıklık oranı, ağırlık merkezi–kararlılık ilişkisi bilinmiyordu; belgelenmiş ilk kontrollü süzülmeler çok daha geç bir döneme aittir ve onlar da ≈250 m ile sınırlı kalmıştır (K8). 40 kg'lık 10 m açıklıklı v2a'yı bir kule balkonundan tek kişinin fırlatması ayrıca pratik bir sorundur.

### 9. Sonuçları en fazla etkileyen belirsizlikler nelerdir?
v1 nominal menziline etkileriyle [HESAP, `duyarlilik_v1.csv`]:
1. Parazit sürükleme CD0 (0,06–0,14): 317–202 m
2. Kalkış noktası (külâh ucu / en üst kat): 245–138 m
3. Kule zemin kotu (35–54 m): 245–335 m
4. Oswald katsayısı: 217–267 m
5. İniş kotu: 207–254 m
6. Rüzgâr (0–8 m/s lodos): 245–287 m
Kütle ve hava yoğunluğu bu modelde menzili değiştirmez (yalnız hızı değiştirir). Modelde olmayan ama önemli belirsizlikler: kalkış evresi, türbülans, kanadın yük altında biçim değiştirmesi. **Hiçbir belirsizlik tek başına ya da birlikte sonucu tersine çevirecek büyüklükte değildir** (v1 için gereken en az 6 kat).

### 10. Rivayet ve hesap birlikte değerlendirildiğinde hüküm
- "Galata Kulesi'nden havalanıp Boğaz'ı geçerek Üsküdar Doğancılar'a indi" biçimindeki **anlatı, süzülme fiziğiyle bağdaşmıyor**: dönem teknolojisiyle beklenebilecek menzil gereken mesafenin onda biri mertebesindedir; modern bir yelken kanatla bile beşte biri. Bu kısım için hüküm: **mümkün görünmüyor**.
- "Bir kişi kanat takıp kuleden atladı ve bir süre süzüldü" biçimindeki daha mütevazı bir çekirdek fiziksel olarak **mümkündür** (v1: ≈250–460 m), ancak bunu destekleyen bağımsız kanıt yoktur. Bu kısım için hüküm: **belirsiz**.
- Teorik fizibilite tarihsel gerçekleşmeyi kanıtlamaz; fiziksel imkânsızlık da rivayetin tamamen uydurma olduğunu kanıtlamaz — yalnızca aktarıldığı ölçüde gerçekleşmediğini gösterir.

Bu sonuç ikincil kaynaktaki modern değerlendirmeyle (K4: gereken oran ≈41:1) aynı yöndedir; buradaki hesap bağımsız yapılmış ve aralık 36–116:1 bulunmuştur.

---

## C. Karşılaştırma tablosu (özet)

| | v1 | v2a | v2b (modern) | Gereken |
|---|---|---|---|---|
| Kanat alanı (m²) | 11,92 | 16,21 | 14,88 | — |
| Uçuş kütlesi (kg) | 86,3 | 104,8 | 97,0 | — |
| Süzülme oranı | 4,75 | 7,20 | 11,89 | 65 (36–116) |
| Uçuş hızı (m/s) | 11,2 | 10,2 | 11,2 | — |
| Batış hızı (m/s) | 2,31 | 1,40 | 0,94 | ≤ 0,17 |
| Süzülme mesafesi, nominal (m) | 245 | 372 | 613 | 3360 |
| Süzülme mesafesi, en iyimser (m) | 532 | 800 | 1334 | 3423 |
| Hedefe ulaşma | Hayır | Hayır | Hayır | |

Tam tablo: `raporlar/karsilastirma.md`. Sınırlamalar: `raporlar/sinirlamalar.md`.
