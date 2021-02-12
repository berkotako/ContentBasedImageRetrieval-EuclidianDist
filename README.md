# ContentBasedImageRetrieval-EuclidianDist

Konu : İçerik Tabanlı Görüntü Erişimi (Content Based Image Retrieval) Uygulaması : Bir resmin renk ve
doku bilgisine göre benzerlerinin bulunması 

1. Veritabanındaki resimlerin renk histogramlarının hesaplanması : Renk benzerliklerinin
ölçülmesi için resimlerin :
a. HSV uzayında H(Hue) değerine göre renk histogramı hesaplama.
b. RGB uzayında R, G ve B bileşenlerinin ayrı ayrı histogramlarını hesaplama.

2.Normalization -> 0-1 Normalization

3.Test Aşaması
a. Benzerlik ölçümlerinde L2 Distance kullanılmıştır.
b. Hue Histogramına göre 5 Resim (En Yakın),
c. RGB Histogramları için 5 Resim (En Yakın) alınmıştır.
