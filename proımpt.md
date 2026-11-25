

# CHALLENGE: Hezarfen Ahmet Çelebi'nin Kanatlarını Bilimsel Olarak Yeniden İnşa Et ve Test Et

## GÖREVİN

Senin görevin, Hezarfen Ahmet Çelebi'nin Galata Kulesi'nden Üsküdar'a uçtuğu yönündeki tarihsel rivayeti araştırmak, rivayette tarif edilen uçuş aracının olası bir mühendislik tasarımını oluşturmak ve bu tasarımın fiziksel olarak çalışıp çalışamayacağını bilimsel yöntemlerle test etmek.

Bu çalışma yalnızca tarihsel bir araştırma değildir. Aynı zamanda kaynak doğrulama, aerodinamik hesaplama, teknik çizim, 3D modelleme, fiziksel simülasyon, görselleştirme ve iteratif mühendislik tasarımı içeren kapsamlı bir araştırma projesidir.

**Temel soru:** Hezarfen Ahmet Çelebi, döneminin teknolojik imkânlarıyla üretilebilecek kanat benzeri bir araç kullanarak rivayet edilen uçuşu gerçekleştirmiş olabilir mi?

Amacın bu soruyu önceden belirlenmiş bir sonuca ulaşmadan, elde ettiğin kanıtlar ve fiziksel hesaplamalar doğrultusunda cevaplamak.

Tüm çalışmayı yerel bilgisayarda yürüt. Araştırma verilerini, kaynakları, çizimleri, hesaplamaları, Blender dosyalarını, renderları ve sonuç raporlarını tek bir proje klasöründe düzenli olarak sakla.

---

## 1. TARİHSEL ARAŞTIRMA

Araştırmayı **Claude in Chrome** kullanarak gerçekleştir.

Tarayıcıyı görünür biçimde kullan. Araştırdığın sayfaları gerçekten aç, incele ve mümkün olduğunda ilgili görselleri ekranda göster.

Özellikle aşağıdaki kaynakları araştır:

- Evliya Çelebi'nin *Seyahatnâme* eserinde Hezarfen Ahmet Çelebi ile ilgili anlatım.

- Güvenilir ansiklopedi maddeleri ve tarihsel referans yayınları.

- Akademik araştırmalar, tarih makaleleri ve ilgili birincil/ikincil kaynaklar.

- Hezarfen'e atfedilen resimler, gravürler, çizimler ve kanat tasvirleri.

- Dönemin uçuş teknolojileri, malzemeleri ve insan uçuşuna ilişkin tarihsel örnekler.

### Araştırma kuralları

1. Her önemli iddianın kaynak URL'sini kaydet.

2. **Tarihsel rivayet, doğrulanmış tarihsel bilgi, modern yorum ve mühendislik varsayımı** kategorilerini açıkça birbirinden ayır.

3. Evliya Çelebi'nin anlatımını doğrulanmış bir uçuş kaydı olarak kabul etme; başka kanıtlarla desteklenip desteklenmediğini araştır.

4. Orijinal kaynak ile onu aktaran ikincil kaynağı birbirinden ayır.

5. Ulaşabildiğin tarihsel görsellerin gerçekten döneme ait olup olmadığını doğrula. Modern illüstrasyonları tarihsel gravür diye sunma.

6. Giriş, üyelik veya ödeme gerektiren sayfalara girme; erişim engelini aşmaya çalışma.

7. Kaynak bulunamıyorsa veya bir iddia doğrulanamıyorsa bunu açıkça belirt.

8. **Uçuşun yılını raporlarında, görsellerinde ve çıktılarında yazma.** Diğer tarihsel dönem bilgilerini gerektiğinde kullanabilirsin.

Her kaynak için başlık, yazar/kurum, URL, erişim tarihi ve araştırmada ne için kullanıldığını kaydet.

Önemli görselleri, erişim ve kullanım koşulları izin veriyorsa, kaynak URL'leri ve açıklamalarıyla birlikte `kaynaklar/` klasörüne kaydet.

---

## 2. İLK KANAT TASARIMI VE TEKNİK ÇİZİM

Tarihsel araştırmadan elde ettiğin bilgiler doğrultusunda Hezarfen'in kullanmış olabileceği bir uçuş aracının mühendislik rekonstrüksiyonunu oluştur.

Tarihsel kaynaklarda kesin bir kanat geometrisi bulunmuyorsa bunu açıkça belirt. Eksik bilgileri tarihsel gerçekmiş gibi gösterme.

Tasarımda şunları değerlendir:

- Kanat açıklığı ve kanat alanı

- Kanat profili ve geometrisi

- Taşıyıcı iskelet yapısı

- Döneme uygun olabilecek malzemeler

- Toplam sistem ağırlığı

- Pilotun konumu ve ağırlık merkezi

- Aerodinamik stabilite

- Kontrol yüzeyleri veya olası ağırlık kaydırmalı kontrol

- Yapısal dayanım ve bağlantı noktaları

Tasarımın teknik çizimini **SVG formatında** oluştur.

Çizimde mümkün olduğunca üst, ön ve yan görünüşleri, temel ölçüleri ve önemli bileşenleri göster.

Ardından **Inkscape komut satırını** kullanarak SVG dosyasını PNG formatına aktar. Komutun başarılı çalıştığını ve PNG dosyasının oluştuğunu doğrula.

---

## 3. BLENDER İLE ÜÇ BOYUTLU MODELLEME

Bilgisayarda açık bir Blender penceresi göreceksin. Mevcut Blender kurulumunu ve kullanılabilir sürümü kontrol et.

**Blender 5 kullanma.** Uyumlu, kurulu başka bir sürümü kullan. Uygun sürüm yoksa bunu bildir; gizlice farklı bir sürüme geçme.

Oluşturduğun teknik tasarıma uygun bir 3D model hazırla.

Model yalnızca görsel olarak etkileyici olmamalı; teknik çizimde kullandığın boyutlarla ve hesaplamalardaki parametrelerle tutarlı olmalı.

Blender sahnesinde:

- Kanat yapısını

- İskelet ve bağlantı elemanlarını

- Pilotun temsilî kütlesini veya insan modelini

- Malzemeleri

- Ağırlık merkezi gibi önemli teknik referansları

olabildiğince açık göster.

### Zorunlu onay noktası

**Önce yalnızca tek bir durağan önizleme karesi üret ve onayıma sun.**

Bu aşamada üç nihai renderı veya turntable animasyonunu üretme.

Onayımı aldıktan sonra:

1. Cycles kullanarak üç farklı açıdan yüksek kaliteli durağan render üret.

2. Kısa bir 360° turntable animasyonu oluştur.

3. Proje dosyasını ve render çıktılarını kaydet.

Bu onay noktası zorunludur. Onay beklerken aşağıdaki bağımsız araştırma ve hesaplama işlerini sürdürebilirsin; ancak nihai görsel üretim aşamasına geçme.

---

## 4. AERODİNAMİK VE FİZİKSEL HESAPLAMALAR

Tasarladığın uçuş aracının performansını açık matematiksel formüllerle hesapla.

Hesaplamalar yalnızca sözel tahminlerden oluşmasın. Gerçek sayısal sonuçlar, birimler, ara işlemler ve doğrulanabilir formüller içersin.

En az aşağıdaki parametreleri değerlendir:

- Pilotun kütlesi

- Kanatların ve iskeletin kütlesi

- Toplam uçuş kütlesi

- Kanat alanı

- Kanat yüklenmesi

- Yerçekimi kuvveti

- Kaldırma kuvveti

- Sürükleme kuvveti

- Kaldırma/sürükleme oranı (L/D)

- Gereken minimum süzülme oranı

- Tahmini süzülme hızı

- Hava hızı ve stall hızı

- Yatay ilerleme mesafesi

- Düşey irtifa kaybı

- Başlangıç irtifası ve kullanılabilir irtifa farkı

- Rüzgârın ve hava yoğunluğunun etkisi

- Gerekli yapısal dayanım ve yaklaşık güvenlik payı

Temel aerodinamik denklemleri kullan; ancak bu denklemlerin hangi koşullarda geçerli olduğunu da açıkla.

### Veri güvenilirliği

**Hiçbir veriyi uydurma.**

Ölçüm, tarihsel kaynak, bilimsel referans, matematiksel hesap ve varsayım birbirinden ayırt edilebilir olmalı.

Bilinmeyen parametreler için makul ve gerekçeli varsayımlar kullan. Her varsayımı açıkça işaretle.

Örneğin pilot kütlesi, kanat kütlesi veya aerodinamik katsayılar kesin olarak bilinmiyorsa bunları tek bir kesin sayı olarak sunmak yerine mümkün olduğunda aralıklar ve senaryolar üzerinden değerlendir.

Bütün sonuçların SI birimleriyle tutarlı olmasını sağla.

Hesaplamaları tekrar üretilebilir bir Python betiğine dönüştür. Ayrıca duyarlılık analizi yaparak hangi varsayımların sonucu en fazla değiştirdiğini belirle.

---

## 5. GALATA–ÜSKÜDAR UÇUŞ SENARYOSU

Tarihsel rivayette geçen başlangıç ve varış bölgelerinin coğrafi konumlarını araştır.

Galata Kulesi ile Üsküdar arasındaki olası uçuş güzergâhını oluştur.

Şunları hesapla:

- Olası başlangıç noktası

- Olası iniş bölgesi

- Yatay mesafe

- Başlangıç noktasının deniz seviyesinden yüksekliği

- Olası iniş bölgesinin yüksekliği

- Kullanılabilir irtifa farkı

- Uçuş için gereken minimum süzülme oranı

- İlk tasarımın tahmini erişebileceği yatay mesafe

- İdeal koşullar ve olumsuz koşullar arasındaki fark

Kule yüksekliği ile deniz seviyesinden yüksekliği birbirine karıştırma.

Tarihsel ve modern coğrafi koşullar arasında fark bulunabileceğini hesaba kat.

Uçuşu yalnızca iki nokta arasındaki düz çizgiye indirgeme. Olası rota, rüzgâr ve iniş koşullarını da değerlendir.

---

## 6. BLENDER'DA BASİT SÜZÜLME SİMÜLASYONU

Hesapladığın fiziksel parametrelerle Blender içerisinde basitleştirilmiş bir süzülme simülasyonu kur.

**Bu simülasyonun yüksek doğruluklu CFD veya gerçek uçuş dinamiği simülasyonu olmadığını açıkça belirt.**

Simülasyon, hesaplanan hız, süzülme oranı, mesafe ve irtifa kaybından türetilmiş, fiziksel açıdan tutarlı bir hareket modeli olsun.

Uygun görürsen hesaplamaları Python ile yapıp sonuçları Blender'a aktar.

Sahnede Galata Kulesi, Boğaz ve Üsküdar tarafını temsil eden basitleştirilmiş bir coğrafi ortam oluştur.

Uçuş boyunca ekranda şu bilgiler gösterilsin:

- Geçen süre

- Yatay ilerleme

- Kalan yatay mesafe

- Başlangıca göre irtifa kaybı

- Deniz seviyesine göre irtifa

- Hava hızı

- Yer hızı

- Süzülme oranı

- Kullanılan senaryo ve varsayımlar

Simülasyonun gerçek coğrafi ölçülerle hangi seviyede örtüştüğünü açıkla.

Başlangıçta kısa, düşük çözünürlüklü bir önizleme renderı hazırla. Nihai görsel üretim aşamasında onay kuralına uy.

Animasyon ve hesaplamalardaki uçuş hareketi birbirini tutmalı. Yalnızca görsel açıdan başarılı görünen fakat hesaplamalarla çelişen bir animasyon üretme.

---

## 7. İLK TASARIMI BİLİMSEL OLARAK YARGILA

İlk tasarım için net bir mühendislik değerlendirmesi yap.

Şu soruya cevap ver:

**Bu kanat tasarımı, belirtilen koşullar altında Galata'dan Üsküdar'a süzülebilir mi?**

Yalnızca 'evet' veya 'hayır' deme. Kararını hesaplamalarla gerekçelendir.

Özellikle şunları değerlendir:

- Yeterli kaldırma kuvveti üretilebilir mi?

- Süzülme oranı yeterli mi?

- Kanatlar toplam ağırlığı taşıyabilir mi?

- Pilot aracı kontrol edebilir mi?

- Kalkış koşulları gerçekçi mi?

- Uçuş hızı ve iniş koşulları güvenli mi?

- Tasarım hangi nedenle başarısız olabilir?

- Sonuç hangi varsayımlara bağlı?

Hesapların kesin bir sonuca izin vermiyorsa **'belirsiz'** sonucunu kullan ve belirsizliğin nedenlerini açıkla.

Bir uçuşun teorik olarak mümkün olmasıyla, tarihsel olarak gerçekten gerçekleşmiş olmasını birbirine karıştırma.

---

## 8. İKİNCİ TASARIM: MÜHENDİSLİK CHALLENGE

İlk tasarım hedeflenen uçuşu gerçekleştiremiyorsa veya performansı yetersizse yeni bir tasarım geliştir.

Amaç, ilk tasarımın zayıflıklarını mühendislik yöntemleriyle gidermek.

Şu parametreleri optimize etmeyi dene:

- Kanat alanı

- Kanat açıklığı

- En-boy oranı

- Kanat profili

- Yapısal ağırlık

- Aerodinamik verimlilik

- Stabilite

- Kontrol kabiliyeti

- Malzeme seçimi

- Gerekli uçuş hızı

Öncelikle tarihsel dönemde erişilebilir olması makul teknolojilerle bir çözüm üretmeye çalış.

Bu kısıt altında başarılı olunamıyorsa, ikinci bir karşılaştırma olarak modern teknolojiye izin verilen bir tasarım geliştirebilirsin. Bu iki tasarımı birbirine karıştırma.

### Her yeniden tasarım için

1. Yeni SVG teknik çizimini üret.

2. Yeni parametrelerle fizik hesaplamalarını tekrarla.

3. Blender modelini güncelle veya yeni bir model oluştur.

4. Süzülme simülasyonunu yeni değerlere göre çalıştır.

5. İlk tasarımla karşılaştır.

6. Performans farklarını sayısal olarak göster.

İlk tasarımı sessizce değiştirme. Versiyonları ve sonuçlarını ayrı kaydet.

Tasarım iyileştirmesinin gerçekten işe yarayıp yaramadığını değerlendir. Daha iyi görünen bir modelin otomatik olarak daha iyi uçtuğunu varsayma.

Birden fazla iyileştirme denemesi yapabilirsin; fakat gerçek ilerleme sağlamayan denemeleri gereksiz yere çoğaltma.

---

## 9. PROJE KLASÖRÜ VE DOSYA DÜZENİ

Çalışma dizininde `Hezarfen_Flight_Challenge` adlı bir klasör oluştur.

Tüm çıktıları bu klasör altında sakla.

Önerilen yapı:

```
Hezarfen_Flight_Challenge/│├── README.md├── kaynaklar/│   ├── kaynakca.md│   ├── gorseller/│   └── gorsel_kaynaklari.md│├── arastirma/│   ├── tarihsel_arastirma.md│   ├── rivayet_ve_kanitlar.md│   └── tarihsel_teknoloji.md│├── tasarim_v1/│   ├── kanat_cizimi.svg│   ├── kanat_cizimi.png│   ├── model.blend│   └── tasarim_notlari.md│├── hesaplamalar/│   ├── parametreler.json│   ├── aerodinamik.py│   ├── sonuclar.csv│   └── fizik_raporu.md│├── simulasyon/│   ├── simulasyon.blend│   ├── simulasyon.py│   ├── ucus_verileri.csv│   └── onizleme/│├── tasarim_v2/│   ├── kanat_cizimi.svg│   ├── kanat_cizimi.png│   ├── model.blend│   └── iyilestirme_raporu.md│├── renderlar/│   ├── onizleme/│   ├── nihai/│   └── animasyon/│└── raporlar/    ├── karsilastirma.md    ├── nihai_degerlendirme.md    └── sinirlamalar.md
```

Gerekli gördüğün ek dosyaları ve alt klasörleri oluşturabilirsin.

Dosyaları düzenli aralıklarla kaydet. Yalnızca çalışma sonunda dosya oluşturmaya çalışma.

Üretilen her çıktının gerçekten mevcut olduğunu ve mümkünse doğru açıldığını kontrol et.

---

## 10. ÇALIŞMA PROTOKOLÜ

Bu görevde bağımsız bir araştırmacı ve mühendislik ajanı gibi hareket et.

- Mümkün olan araçları gerçekten kullan; yaptığın bir işlemi yalnızca yaptığını söylemekle yetinme.

- Claude in Chrome ile araştırma yaparken sayfaları görünür şekilde aç.

- Inkscape dönüşümünü gerçek komut satırı işlemleriyle gerçekleştir.

- Blender dosyalarını gerçek Blender ortamında oluştur.

- Hesaplamalarını çalıştırılabilir kod ile doğrula.

- Başarısız komutların nedenini araştır ve mümkün olduğunda düzelt.

- Araç erişimi veya sürüm uyumsuzluğu varsa bunu açıkça bildir.

- Kaynak göstermeden tarihsel veya sayısal veri üretme.

- Varsayımlarını kayıt altına al.

- Önceki sonuçlarınla çelişen yeni bir bulgu elde edersen önceki sonucu güncelle ve nedenini açıkla.

- Projenin her aşamasında yeniden üretilebilirliği önceliklendir.

- Kaynak güvenilirliği ile görsel kalitesini birbirine karıştırma.

- Teorik fizibiliteyi gerçek dünya güvenliği veya tarihsel doğrulama olarak sunma.

- Fiziksel uçuş denemesi gerçekleştirme veya bunu güvenli kabul etme; çalışma dijital modelleme ve teorik analizle sınırlı kalmalı.

### Önemli çalışma ilkesi

Gereksiz onay istemeden ilerle. Problemleri önce kendi başına çözmeye çalış.

**Ancak ilk Blender durağan önizleme karesini oluşturduğunda mutlaka dur ve onayımı iste.** Bu onay olmadan üç nihai Cycles renderına veya turntable üretimine geçme.

Bu zorunlu durak dışında bağımsız kararlar verebilirsin.

---

## 11. NİHAİ DEĞERLENDİRME

Sonuç raporunda aşağıdaki soruları açık ve sayısal olarak cevapla:

1. Hezarfen'in uçuşu hakkındaki tarihsel kanıtların güvenilirliği nedir?

2. Kanatların orijinal tasarımı hakkında gerçekten ne biliyoruz?

3. İlk rekonstrüksiyon fiziksel olarak uçabilir mi?

4. Galata–Üsküdar mesafesini katetmek için hangi koşullar gerekir?

5. İlk tasarımın en büyük mühendislik problemi nedir?

6. İkinci tasarım hangi parametreleri iyileştirdi?

7. Yeniden tasarlanan araç hedeflenen uçuşu teorik olarak gerçekleştirebilir mi?

8. Dönemin teknolojisiyle böyle bir araç yapmak ne kadar gerçekçidir?

9. Sonuçları en fazla etkileyen belirsizlikler nelerdir?

10. Tarihsel rivayet ile mühendislik hesaplamaları birlikte değerlendirildiğinde nasıl bir hükme varılabilir?

İlk ve geliştirilmiş tasarımları sayısal bir karşılaştırma tablosunda göster.

Mümkünse her tasarım için süzülme mesafesi, süzülme oranı, kütle, kanat alanı, uçuş hızı ve hedefe ulaşma durumu gibi parametreleri karşılaştır.

**Son hükmün açık, gerekçeli ve eleştirel olsun.**

'Bilinmiyor', 'kanıt yetersiz' veya 'mevcut modelle mümkün görünmüyor' gibi sonuçları da geçerli bilimsel sonuçlar olarak kabul et.

Başarılı bir proje, uçuşun mutlaka mümkün olduğunu kanıtlayan proje değildir. Başarılı bir proje, varsayımlarını açıkça belirleyen, hesaplarını doğrulayan ve elde ettiği sonuçları dürüstçe değerlendiren projedir.

---

## BAŞLA

Önce proje klasörünü oluştur ve tarihsel kaynak araştırmasına başla.

Kaynaklarını topla, olası ilk tasarımı geliştir, hesaplamaları yap ve Blender'da ilk önizleme modelini hazırla.

İlk durağan önizleme karesini onayıma sunduğunda nihai render aşamasına geçmeden dur.

**Bu bir mühendislik challenge'ıdır. Yalnızca güzel bir 3D model değil, kendi hesaplarıyla sınanabilen ve eleştirel olarak değerlendirilebilen bir uçuş sistemi ortaya koymanı bekliyorum.**

İlk önizleme için net durma koşulu ekleAraştırma ve üretim aşamalarını sırala
