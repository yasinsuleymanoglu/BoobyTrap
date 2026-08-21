# 🛡️ BoobyTrap (Mac Edition)

Mac bilgisayarınızın başından kalktığınızda cihazınızı koruyan nihai ajan tuzağı! Biri farenizi oynattığı veya klavyenize dokunduğu an gizlice fotoğrafını çeker, ekrana saniyeler içinde devasa bir uyarı görseli basar ve bilgisayarı kilitler.

## 🚀 Özellikler
- **Fiziksel Sensör Tuzağı**: Klavye veya fare (touchpad dahil) üzerindeki en ufak bir harekette tetiklenir.
- **Gizli Çekim**: Hareketi algıladığı an web kamerasını (yeşil ışığı çok kısa yakarak) açar ve sızan kişinin fotoğrafını `Masaüstü/Intruder_Photos` klasörüne kaydeder.
- **Utanç Duvarı (Opsiyonel)**: Kilitlenmeden önce kullanıcının seçtiği bir fotoğrafı ekranın 100% boyutunda devasa bir şekilde sızan kişinin yüzüne çarpar.
- **Panik Kilidi (Zırhlı)**: Eğer sızan kişi panikleyip programı kapatmaya (`Ctrl+C`, `Esc`, `Cmd+Q`) çalışırsa, program intihar etmeden önce ekranı zorla (Lock Screen) kilitler.
- **Gizli Şifre Kombinasyonu**: Tuzağı kapatmak için sadece sizin bildiğiniz ardışık tuş kombinasyonu (`t` ve `r`) kullanılır.

## ⚙️ Kurulum ve İzinler

### 1. Gereksinimler ve Kurulum (Sanal Ortam / Venv)
Mac'inizde **Python 3** yüklü olmalıdır. Projeyi çalıştırırken bilgisayarınızın ana Python ayarlarını bozmamak ve paket çakışmalarını (Örn: opencv hataları) engellemek için izole bir "Sanal Ortam" kurmanız şiddetle tavsiye edilir.

Terminali açın ve şu komutları sırasıyla çalıştırarak kurulumu tamamlayın:

1. Projenin bulunduğu klasörün içine girin (Yolu indirdiğiniz yere göre değiştirin):
```bash
cd /yol/BoobyTrap/mac
```
2. `trap` adında yeni bir sanal ortam oluşturun:
```bash
python3 -m venv trap
```
2. Ortamı aktif edin:
```bash
source trap/bin/activate
```
3. Gerekli kütüphaneleri bu güvenli alana kurun:
```bash
pip install opencv-python pynput
```
*(Not: Sistemi her kullanacağınızda önce `source trap/bin/activate` komutuyla ortamı aktif ettiğinizden emin olun.)*

### 2. MacOS İzinleri (ÇOK ÖNEMLİ)
Bu uygulamanın klavyeyi dinleyebilmesi ve kamerayı açabilmesi için Mac'inizin güvenlik duvarına izin vermeniz gerekir.
1. `Sistem Ayarları` -> `Gizlilik ve Güvenlik` bölümüne girin.
2. **Erişilebilirlik (Accessibility)** kısmına girip Terminal (veya iTerm) uygulamasını aktif edin (Tuşları dinleyebilmek için zorunludur).
3. **Kamera (Camera)** kısmına girip yine Terminal uygulamasını aktif edin (Fotoğraf çekebilmek için zorunludur).

## 📸 Opsiyonel Uyarı Fotoğrafı (Shame Image) Nasıl Eklenir?
Mac'in tam ekran arayüzlerinde sistemin çökmemesi ve görselin milisaniyeler içinde ekrana basılması için görselin optimize edilmiş bir `.ppm` formatında olması gerekir. 
Bunun için projenin içine özel bir yükleyici (setup) betiği ekledik. İnternetten bulduğunuz herhangi bir JPG veya PNG dosyasını tuzağa eklemek için şu komutu çalıştırmanız yeterlidir:
```bash
python setup_image.py <kendi_resminiz.jpg>
```
*Bu betik, seçtiğiniz fotoğrafı otomatik olarak okur, eğer çözünürlüğü Mac'i yoracak kadar büyükse (Örn: 4K) akıllıca küçültür (1920px) ve anında tuzağa entegre eder.*
*(Not: Resmi koymazsanız program yine kusursuz çalışır, fotoğrafı çeker ve uyarı ekranı göstermeden direkt kilit ekranına atlar).*

## 🏃 Nasıl Çalıştırılır?
Terminalinizi açın ve programı çalıştırın:
```bash
python trap_mac.py
```
- Ekranda şık bir popup 3-2-1 diye sayarak tuzağı kuracaktır. Ardından masadan ayrılabilirsiniz.
- Geri döndüğünüzde **SADECE SİZ** klavyeden önce `t` sonra `r` tuşlarına hızlıca basarak tuzağı sessizce imha edebilirsiniz.
- Yanlış tuşa basıldığı veya fare oynatıldığı an tuzak patlar!

---

## 📡 Ekstra Modül: Bluetooth Oto-Tuzak (Honeypot)
Projenin içinde yer alan **`bluetooth_trap.py`** modülü, tamamen otomatik bir ajan yazılımı (Bal Küpü) olarak tasarlanmıştır.

### 🌟 Özellikleri:
- **Akıllı Yakınlık Sensörü:** Telefonunuz (Örn: Yasin iPhone'u) Mac'e yakın olduğu sürece tuzak pasiftir ve bilgisayar normal şekilde kullanılabilir.
- **Gizli Pusu Modu:** Masadan kalkıp yaklaşık 2 metre uzaklaştığınızda, sağ üstte sessiz bir bildirim çıkar ve bilgisayar "Pusu" moduna geçer. Ekranda hiçbir kilit belirtisi olmaz, bilgisayar tamamen savunmasız görünür.
- **Sinsi Tetikleyici:** Bilgisayar pusu modundayken içeri giren bir izinsiz kişi fareye veya klavyeye dokunduğu an (3 saniyelik geri sayım dahi olmadan) fotoğrafı çekilir, uyarı resmi ekrana basılır ve ekran anında kilitlenir!
- **Terminal Kamuflajı:** Uygulama terminalde çalışırken büyük uyarılar vermek yerine, sıradan bir sistem servisi (`[sys.bluetooth.daemon] pid: 4892`) gibi görünerek kendini gizler.
- **Otomatik İptal:** Tuzağa kimse düşmezse ve siz masaya geri dönerseniz, Mac telefonunuzun yaklaştığını algılar ve tuzağı siz daha sandalyeye oturmadan otomatik olarak devreden çıkarır.

### Kurulum (Sadece bu modül için):
Bu modül Apple'ın çekirdek Bluetooth altyapısını kullandığı için ek bir kütüphaneye ihtiyaç duyar:
```bash
pip install pyobjc-framework-CoreBluetooth
```
Çalıştırmak için UUID kodunuzu kodun içindeki ayarlar kısmına yapıştırın ve çalıştırın:
```bash
python bluetooth_trap.py
```

---

### 💡 İpucu: Hızlı Başlatma (Terminal Kısayolu Ekleme)
Her sabah bilgisayarı açtığınızda uzun uzun dosya yolunu yazmak veya sanal ortamı (venv) aktif etmekle uğraşmak istemiyorsanız, terminalinize kalıcı bir kısayol (alias) ekleyebilirsiniz.

Bunun için terminalinizde şu komutu kendi indirdiğiniz dosya yoluna göre düzenleyip yapıştırın (Sanal ortamdaki python dosyasının yolunu gösterdiğimize dikkat edin):
```bash
echo "alias trap='/bilgisayarinizdaki/tam/yol/BoobyTrap/mac/trap/bin/python /bilgisayarinizdaki/tam/yol/BoobyTrap/mac/bluetooth_trap.py'" >> ~/.zshrc
source ~/.zshrc
```
*(Artık terminale tıpkı bizim yaptığımız gibi sadece **`trap`** yazmanız yeterlidir! Arka planda tüm sanal ortamı kendisi halledip tuzağı anında kuracaktır.)*
