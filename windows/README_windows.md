# 🛡️ BoobyTrap (Windows Edition)

Windows bilgisayarınızın başından kalktığınızda cihazınızı koruyan nihai ajan tuzağı! Biri farenizi oynattığı veya klavyenize dokunduğu an gizlice fotoğrafını çeker, ekrana saniyeler içinde devasa bir uyarı görseli basar ve bilgisayarı kilitler.

## 🚀 Özellikler
- **Fiziksel Sensör Tuzağı**: Klavye veya fare üzerindeki en ufak bir harekette tetiklenir.
- **Gizli Çekim**: Hareketi algıladığı an web kamerasını (ışığı çok kısa yakarak) açar ve sızan kişinin fotoğrafını `Masaüstü/Intruder_Photos` klasörüne kaydeder.
- **Utanç Duvarı (Opsiyonel)**: Kilitlenmeden önce kullanıcının seçtiği bir fotoğrafı ekranın 100% boyutunda devasa bir şekilde sızan kişinin yüzüne çarpar.
- **Sistem Kilidi**: Windows'un yerleşik API'si (ctypes) ile bilgisayarı direkt Kilit Ekranına (Win+L) atar.
- **Gizli Şifre Kombinasyonu**: Tuzağı kapatmak için sadece sizin bildiğiniz ardışık tuş kombinasyonu (`t` ve `r`) kullanılır.

## ⚙️ Kurulum ve İzinler

### 1. Gereksinimler ve Kurulum (Sanal Ortam / Venv)
Bilgisayarınızda **Python 3** yüklü olmalıdır. Projeyi çalıştırırken sisteminizin ana Python ayarlarını bozmamak ve paket çakışmalarını (Örn: opencv hataları) engellemek için izole bir "Sanal Ortam" kurmanız şiddetle tavsiye edilir.

Komut İstemi'ni (CMD) veya PowerShell'i açıp şu komutları sırasıyla çalıştırın:

1. Projenin bulunduğu klasörün içine girin (Yolu indirdiğiniz yere göre değiştirin):
```cmd
cd \yol\BoobyTrap\windows
```
2. `trap` adında yeni bir sanal ortam oluşturun:
```cmd
python -m venv trap
```
2. Ortamı aktif edin:
```cmd
trap\Scripts\activate
```
3. Gerekli kütüphaneleri (requirements.txt) bu güvenli alana kurun:
```cmd
pip install -r ..\requirements.txt
```
*(Not: Sistemi her kullanacağınızda önce `trap\Scripts\activate` komutuyla ortamı aktif ettiğinizden emin olun.)*

### 2. İzinler
- Windows'ta `pynput` kütüphanesi tuşları dinlemek için çoğunlukla ek bir izne ihtiyaç duymaz. 
- Ancak eğer web kameranızdan fotoğraf çekemezse, Windows `Ayarlar -> Gizlilik -> Kamera` bölümünden masaüstü uygulamalarının kameraya erişimine izin verdiğinizden emin olun.

## 📸 Opsiyonel Uyarı Fotoğrafı (Shame Image) Nasıl Eklenir?
Sızan kişinin suratına basmak istediğiniz herhangi bir `.jpg` veya `.png` fotoğrafının adını `shame_image.jpg` yapın ve `trap_windows.py` dosyası ile **aynı klasöre** koyun. Hepsi bu kadar! 
*(Not: Resmi koymazsanız program yine kusursuz çalışır, gizli fotoğrafı çeker ve uyarı ekranı göstermeden direkt kilit ekranına atlar).*

## 🏃 Nasıl Çalıştırılır?
Komut satırını açıp kodu çalıştırın:
```cmd
python trap_windows.py
```
- Ekranda şık bir popup 3-2-1 diye sayarak tuzağı kuracaktır. Ardından masadan ayrılabilirsiniz.
- Geri döndüğünüzde **SADECE SİZ** klavyeden önce `t` sonra `r` tuşlarına hızlıca basarak tuzağı sessizce imha edebilirsiniz. (Bu kısayolu kodun içinden istediğiniz gibi değiştirebilirsiniz).
- Yanlış tuşa basıldığı veya fare oynatıldığı an tuzak patlar!

---

### 💡 İpucu: Hızlı Başlatma (Masaüstü Kısayolu)
Sistemi her seferinde komut isteminden çalıştırmak veya sanal ortamı (`venv`) aktif etmekle uğraşmamak için projeyi tek tıkla çalıştıracak bir `.bat` dosyası yapabilirsiniz:

1. Proje klasörünün içine girin, sağ tıklayıp yeni bir metin belgesi oluşturun ve adını **`trap.bat`** yapın (Sonunun `.txt` değil `.bat` olduğundan emin olun).
2. Dosyanın içine şu 3 satırı kopyalayıp kaydedin:
```bat
@echo off
call trap\Scripts\activate
python trap_windows.py
```
3. Artık bu dosyaya her çift tıkladığınızda arka planda sanal ortam otomatik olarak yüklenir ve tuzak saniyeler içinde devreye girer! İsterseniz bu `trap.bat` dosyasına sağ tıklayıp "Gönder -> Masaüstüne Kısayol Oluştur" diyerek tamamen masaüstünden tek tıkla da kullanabilirsiniz.
