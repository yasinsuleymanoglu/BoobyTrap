import sys
import cv2
import os

def optimize_and_convert(input_path):
    if not os.path.exists(input_path):
        print(f"HATA: Dosya bulunamadı -> {input_path}")
        sys.exit(1)

    print(f"[*] Görsel işleniyor: {input_path}...")
    img = cv2.imread(input_path)
    
    if img is None:
        print("[-] HATA: Görsel okunamadı! Lütfen geçerli bir JPG veya PNG dosyası seçin.")
        sys.exit(1)

    # Maksimum çözünürlük sınırı (Sistemi yormaması ve milisaniyeler içinde açılması için)
    MAX_DIMENSION = 1920
    height, width = img.shape[:2]
    
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        print(f"[*] Görsel boyutu çok büyük ({width}x{height}). Sistem performansı için optimize ediliyor...")
        scaling_factor = MAX_DIMENSION / float(max(width, height))
        new_width = int(width * scaling_factor)
        new_height = int(height * scaling_factor)
        # INTER_AREA küçültme işlemleri için en kaliteli ve pürüzsüz sonucu verir
        img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
        print(f"[+] Yeni optimize çözünürlük: {new_width}x{new_height}")
    else:
        print(f"[+] Görsel boyutu uygun ({width}x{height}). Boyutlandırmaya gerek yok.")

    # Çıktı yolu (Kodun bulunduğu klasöre shame_image.ppm olarak kaydet)
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shame_image.ppm")
    
    # PPM formatında kaydet (Mac'in yerel Tkinter altyapısının en sevdiği formatsız ham veri)
    cv2.imwrite(output_path, img)
    print(f"\n✅ BAŞARILI! Görsel tuzağa yerleştirildi.")
    print(f"💾 Dosya Yolu: {output_path}")
    print("🚀 Artık sistemi çalıştırdığınızda bu görsel kullanılacaktır.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanım: python setup_image.py <fotograf_yolu.jpg>")
        print("Örnek: python setup_image.py benim_fotografim.jpg")
        sys.exit(1)
        
    optimize_and_convert(sys.argv[1])
