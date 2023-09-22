# Tony'nin geliştirmeleri #

* Yazar: Tony Malykh
* [kararlı sürümü][1] indir
* NVDA uyumluluğu: 2022.4 ve 2023.1

Bu eklenti, NVDA ekran okuyucu için her biri ayrı bir eklentiyi hak
etmeyecek kadar küçük olan bir dizi küçük iyileştirme içerir.

## Geliştirilmiş tablo gezinme komutları

* NVDA+Control+rakamlar - tablodaki 1./2./3./... 10. sütuna atlayın.
* NVDA+Alt+rakamlar - tabloda 1./2./3./... 10. sıraya atla.

## Kaldırılan tablo gezinme komutları

Aşağıdaki tablo gezinme komutları, NVDA çekirdeğinin en son sürümüne entegre
edildikleri için kaldırıldı.

* Tablodaki ilk/son sütuna atlayın.
* Tablodaki ilk/son satıra atlayın.
* Geçerli hücreden başlayarak tablodaki geçerli sütunu okuyun.
* Geçerli hücreden başlayarak tablodaki geçerli satırı okuyun.
* Yukarıdan başlayarak tablodaki mevcut sütunu okuyun.
* Satırın başından başlayarak tablodaki mevcut satırı okuyun.

Not: NVDA'nın bu özellikler için varsayılan hareketleri hakkında bilgi
edinmek için lütfen NVDA kullanım kılavuzuna bakın.

## Tabloları panoya kopyalama

Aşağıdaki kısayollarla, tablonun tamamını veya geçerli satırı veya geçerli
sütunu biçimlendirilmiş bir şekilde kopyalayabilir, böylece Microsoft Word
veya WordPad gibi zengin metin editörlerine tablo olarak
yapıştırabilirsiniz.

* NVDA+Alt+T - tabloyu veya bir kısmını kopyalamak için seçenekler içeren
  açılır menüyü gösterir.

Tabloları, satırları, sütunları ve hücreleri kopyalamak için ayrı komutlar
da vardır, ancak bunların varsayılan olarak atanmış klavye kısayolları
yoktur, onlar için özel klavye kısayolları NVDA'nın Girdi Hareketleri
iletişim kutusunda atanabilir.

## Gelişmiş kelime gezinme komutları

1.8 sürümünden itibaren bu işlevsellik [WordNav
eklentisine](https://github.com/mltony/nvda-word-nav/) taşınmıştır.

## Otomatik dil değiştirme

Sentezleyicinizin dilini karakter kümesine göre otomatik olarak
değiştirmenize izin verir. Bu eklenti için tercihler penceresinde her dil
için refgular ifade yapılandırılabilir. Lütfen sentezleyicinizin
ilgilendiğiniz tüm dilleri desteklediğinden emin olun. Latin tabanlı iki dil
veya karakter kümeleri benzer olan iki dil arasında geçiş şu anda
desteklenmemektedir.

## Hızlı arama komutları

Düzenlenebilir dosyalarda sıkça aradığınız yapılandırılabilir düzenli
ifadeler için en fazla üç yuvaya sahip olabilirsiniz. Bunlar varsayılan
olarak `PrintScreen`, `ScrollLock` ve `Pause` düğmelerine atanmıştır. Bu
düğmelerle birlikte `Shift` tuşuna basarak ileri veya geri arama
yapabilirsiniz.

## NVDA'dan gelen istenmeyen 'seçilmemiş' konuşmayı bastırın

Metin editörlerinde bazı metinlerin seçili olduğunu varsayalım. Ardından,
sizi belgenin başka bir bölümüne götürmesi gereken Ana Sayfa veya Yukarı Ok
gibi bir tuşa basarsınız. NVDA 'seçilmedi' duyurusunu yapar ve ardından eski
seçimi söyler, bu bazen rahatsız edici olabilir. Bu özellik, NVDA'nın bu
gibi durumlarda önceden seçilen metni konuşmasını engeller.

## Dinamik kısayollar

Belirli tuş vuruşlarını dinamik olarak atayabilirsiniz. Böyle bir tuş vuruşu
yaptıktan sonra, NVDA o anda odaklanılan pencerede herhangi bir güncelleme
olup olmadığını kontrol edecek ve satır güncellenirse, NVDA bunu otomatik
olarak söyleyecektir. Örneğin, metin düzenleyicilerdeki bazı tuş vuruşları
dinamik olarak işaretlenmelidir, örneğin yer imine atla, başka bir satıra
atla ve adım at/adım atma gibi hata ayıklama tuş vuruşları.

Dinamik kısayol tuşları tablosunun formatı basittir: her satır aşağıdaki
formatta bir kural içerir:
```
uygulamaAdı tuş vuruşu
```
burada "Uygulama adı", bahsi geçen kısayol tuşunun dinamik olarak
işaretlendiği (veya "*" ile tüm uygulamalarda dinamik olarak işaretlendiği)
uygulamanın adıdır ve "klavye kısayolu", NVDA biçiminde bir kısayoludur,
örneğin, "control+alt+shift" +sayfa aşağı`.

Uygulamanız için appName'i bulmak için şunu yapın:

1. Uygulamanıza geçin.
2. NVDA+Shift+Z tuşlarına basarak NVDA Python Konsolunu açın.
3. Focus.appModule.appName yazın ve enter tuşuna basın.
4. Çıktı bölmesine gitmek ve son satırda appName değerini bulmak için F6'ya
   basın.

## Pencereleri gösterme ve gizleme

Geçerli pencereyi gizleyebilir ve o anda gizli olan tüm pencereleri
gösterebilirsiniz. Aynı uygulamada birden fazla pencere kullanıyorsanız
(Chrome diyelim) ve bunları yeniden düzenlemek istiyorsanız bu yararlı
olabilir.

* NVDA+Shift+-: mevcut pencereyi gizler.
* NVDA+Shift+=: Şu anda kapalı olan tüm pencereleri gösterir.

Bir pencere gizliyken NVDA'dan çıkarsanız, şu anda NVDA yeniden
başlatıldıktan sonra pencereyi göstermenin bir yolu olmadığını unutmayın.

## Konsol geliştirmeleri

Daha önce bu eklenti, konsolla ilgili bir dizi özellik içeriyordu. 1.8
sürümünden itibaren, konsolla ilgili tüm özellikler [Konsol Araç Seti
eklentisine](https://github.com/mltony/nvda-console-toolkit/)
taşınmıştır. özellikle:

* Gerçek zamanlı konsol çıktısı
* Konsol güncellemelerinde bip sesi
* Konsollarda Control+V'yi zorunlu kılın

## NVDA meşgulken bip sesi

NVDA meşgul olduğunda NVDA'nın sesli geri bildirim sağlaması için bu
seçeneği işaretleyin. NVDA'nın meşgul olması, mutlaka NVDA ile ilgili bir
sorun olduğunu göstermez, bunun yerine, bu, kullanıcıya herhangi bir NVDA
komutunun hemen çalıştıramayacağının bir işaretidir.

## Ses ayarı

* NVDA+Control+sayfa yukarı/sayfa aşağı - NVDA sesini ayarlayın.
* NVDA+Alt+Sayfa yukarı/Sayfa Aşağı - NVDA hariç tüm uygulamaların ses
  seviyesini ayarlar.

## Ses ayırıcı

Ses ayırıcı modunda, NVDA tüm ses çıkışını sağ kanala yönlendirirken,
uygulamalar seslerini sol kanalda çalar. Kanallar ayarlarda
değiştirilebilir.

* NVDA+Alt+S, ses ayırıcı modunu değiştirir.

Belirli durumlarda, NVDA çalışmıyorken bile bir uygulamadan ses çıkışının
bir kanalla sınırlı olabileceğini lütfen unutmayın. Örneğin, ses ayırma
açıkken NVDA çökerse veya söz konusu uygulama çalışmıyorken NVDA temiz bir
şekilde çıkarsa bu durum meydana gelebilir. Bu gibi durumlarda, lütfen söz
konusu uygulama çalışırken NVDA'yı yeniden başlatın ve ses ayırmayı kapatın.

## Gelişmiş fare işlevleri

* Alt+NumPad Bölü: Fare imlecini geçerli nesneye getirin ve tıklayın.
* Alt+NumPad Çarpı: Fare imlecini geçerli nesneye getirin ve farenin sağ
  tuşuyla üzerine tıklayın.
* Alt+NumPad Artı/NumPad Eksi: Fare imlecini geçerli nesneye getirin ve
  aşağı/yukarı kaydırın. Bu, sonsuz kaydırmalı web sayfaları ve kaydırmada
  daha fazla içerik yükleyen web sayfaları için kullanışlıdır.
* Alt+NumPad Sil: Fare imlecini ekranın sol üst köşesine doğru hareket
  ettirin. Bu, belirli uygulamalarda istenmeyen pencerelerin üzerine gelmeyi
  önlemek için yararlı olabilir.


## Metin editörlerinde ekleme modunu algılama

Bu seçenek etkinleştirilirse, NVDA metin editörlerinde ekleme modunu
algıladığında bip sesi çıkarır.

## Shift insert kısayolunu engelleme

NVDA'da İnsert tuşuna arka arkaya iki kez basmak uygulamalarda ekleme modunu
değiştirir. Ancak bu durum bazen yanlışlıkla olabilir. Bu özel bir kısayol
tuşu olduğundan, ayarlarda devre dışı bırakılamaz. Bu eklenti, bu klavye
kısayolunu engellemenizi sağlar.

Bu seçenek varsayılan olarak devre dışıdır ve ayarlarda
etkinleştirilmelidir.

## NVDA işleminin sistem önceliği

Bu, özellikle CPU yükü yüksek olduğunda, NVDA yanıt verme hızını artırabilen
NVDA işleminin sistem önceliğini artırmaya olanak tanır.

## Windows+sayı tuşlarına basıldığında odak görev çubuğunda takılıp kaldığında oluşan bir hatayı düzeltme

Windows 10'da ve muhtemelen diğer sürümlerde bir hata var. Windows+sayı
kısayolunu kullanan uygulamalar arasında geçiş yaparken bazen odak, geçiş
yapılan pencereye atlamak yerine görev çubuğu alanında takılıp kalıyor. Bu
hatayı Microsoft'a bildirmeye çalışmak umutsuz olduğundan, bu eklentide bir
geçici çözüm uygulanmıştır. Eklenti bu durumu algılar ve bu durum
algılandığında kısa, düşük perdeli bir bip sesi çıkarır, ardından eklenti
otomatik olarak düzeltir.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=tonysEnhancements
