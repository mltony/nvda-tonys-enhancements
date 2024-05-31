# Tony'nin geliştirmeleri #

Bu eklenti, NVDA ekran okuyucu için her biri ayrı bir eklentiyi hak
etmeyecek kadar küçük olan bir dizi küçük iyileştirme içerir.

Bu eklenti NVDA'nın 2022.4 ve 2024.1 sürümleriyle uyumludur.

## İndirin

Lütfen NVDA eklenti mağazasından en son sürümü yükleyin.

## Geliştirilmiş tablo gezinme komutları
* NVDA+Control+rakamlar - tablodaki 1./2./3./... 10. sütuna atlayın.
* NVDA+Alt+rakamlar - tabloda 1./2./3./... 10. sıraya atla.

## Tabloları panoya kopyalama

Aşağıdaki kısayollarla, tablonun tamamını veya geçerli satırı veya geçerli
sütunu biçimlendirilmiş bir şekilde kopyalayabilir, böylece Microsoft Word
veya WordPad gibi zengin metin editörlerine tablo olarak
yapıştırabilirsiniz.

* NVDA+Alt+T - tabloyu veya bir kısmını kopyalamak için seçenekler içeren
  açılır menüyü gösterir.

Tabloları, satırları, sütunları ve hücreleri kopyalamak için ayrı komutlar
da vardır, ancak bunlara varsayılan olarak atanmış klavye kısayolları
yoktur; bunlar için özel klavye kısayolları NVDA'nın Girdi Hareketleri
iletişim kutusunda atanabilir.

## Otomatik dil değiştirme
Sentezleyicinizin dilini karakter kümesine göre otomatik olarak
değiştirmenize izin verir. Bu eklenti için tercihler penceresinde her dil
için refgular ifade yapılandırılabilir. Lütfen sentezleyicinizin
ilgilendiğiniz tüm dilleri desteklediğinden emin olun. Latin tabanlı iki dil
veya karakter kümeleri benzer olan iki dil arasında geçiş şu anda
desteklenmemektedir.

## Hızlı arama komutları

Sürüm 1.18'den itibaren, Hızlı Arama komutları [Girinti Dolaşımı
eklentisine](https://github.com/mltony/nvda-indent-nav) taşınmıştır.

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

Sürüm 1.18'den itibaren göster/gizle komutları [Görev Değiştirici
eklentisine](https://github.com/mltony/nvda-task-switcher) taşınmıştır.

## NVDA meşgulken bip sesi

NVDA meşgul olduğunda NVDA'nın sesli geri bildirim sağlaması için bu
seçeneği işaretleyin. NVDA'nın meşgul olması, mutlaka NVDA ile ilgili bir
sorun olduğunu göstermez, bunun yerine, bu, kullanıcıya herhangi bir NVDA
komutunun hemen çalıştıramayacağının bir işaretidir.

## Uygulama Ses ayarı

Bu işlevsellik NVDA çekirdeğiyle birleştirilmiştir ve NVDA v2024.3 veya
sonraki sürümlerinde mevcuttur.

## Ses ayırıcı

Bu işlevsellik NVDA çekirdeğiyle birleştirilmiştir ve NVDA v2024.2 veya
sonraki sürümlerinde mevcuttur.

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

Bu özellik v1.18 sürümünden itibaren kaldırılmıştır. Daha güvenilir bir
görev değiştirme işlevine ihtiyacınız varsa lütfen [Görev Değiştirici
eklentisini](https://github.com/mltony/nvda-task-switcher) kullanmayı
düşünün.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=tonysEnhancements
