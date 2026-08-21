import os
import sys
import time
import subprocess
from datetime import datetime
import cv2
from pynput import keyboard, mouse

# --- AYARLAR ---
SAVE_DIR = os.path.expanduser("~/Desktop/Intruder_Photos")

# Tuzağı sessizce kapatmak için gereken gizli tuş kombinasyonu (Sırasıyla basılmalı)
SECRET_COMBO = ['t', 'r']

# Ekrana tam ekran basılacak resim. Kullanmak istemiyorsanız içini boş bırakın veya dosyayı silin.
# Mac tam ekranında sorunsuz çalışması için resmi .ppm formatında yanına koymanız tavsiye edilir.
SHAME_IMAGE_PATH = os.path.join(os.path.dirname(__file__), "shame_image.ppm")

def show_countdown():
    countdown_path = os.path.join(os.path.dirname(__file__), "countdown.py")
    subprocess.run([sys.executable, countdown_path])

class BoobyTrap:
    def __init__(self):
        self.armed = False
        self.triggered = False
        self.combo_index = 0
        
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)
            
        show_countdown()
        self.armed = True

    def trigger(self):
        if not self.armed or self.triggered:
            return
        self.triggered = True

    def on_press(self, key):
        if not self.armed or self.triggered:
            return

        try:
            char = key.char.lower()
        except AttributeError:
            char = str(key)

        # Doğru sırayla gizli tuşlara basılıyor mu kontrol et
        if char == SECRET_COMBO[self.combo_index]:
            self.combo_index += 1
            if self.combo_index == len(SECRET_COMBO):
                # Başarılı şifre girişi, tuzağı imha et
                self.armed = False
                subprocess.run(["osascript", "-e", 'display notification "Tuzak sessizce devre dışı bırakıldı." with title "Güvenlik Tuzağı"'])
                os._exit(0)
            return
        else:
            # Yanlış tuşa basıldığı an tetiklenir!
            self.trigger()

    def on_move(self, x, y):
        if self.armed:
            self.trigger()

    def on_click(self, x, y, button, pressed):
        if self.armed and pressed:
            self.trigger()

    def on_scroll(self, x, y, dx, dy):
        if self.armed:
            self.trigger()

    def start(self):
        mouse_listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll)
            
        keyboard_listener = keyboard.Listener(
            on_press=self.on_press)
            
        mouse_listener.start()
        keyboard_listener.start()
        
        try:
            while True:
                if self.triggered:
                    # 1. Kameradan gizlice fotoğraf çek
                    cap = cv2.VideoCapture(0)
                    if cap.isOpened():
                        for _ in range(3):
                            cap.read()
                            time.sleep(0.05)
                        ret, frame = cap.read()
                        if ret:
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                            photo_path = os.path.join(SAVE_DIR, f"intruder_{timestamp}.jpg")
                            cv2.imwrite(photo_path, frame)
                        cap.release()
                    
                    # 2. Opsiyonel: İzinsiz giren kişinin ekranına tam ekran fotoğraf bas
                    if SHAME_IMAGE_PATH and os.path.exists(SHAME_IMAGE_PATH):
                        viewer_path = os.path.join(os.path.dirname(__file__), "show_image.py")
                        subprocess.run([sys.executable, viewer_path, SHAME_IMAGE_PATH])
                            
                    # 3. Bilgisayarı ZORLA kilit ekranına (Lock Screen) at
                    lock_script = 'tell application "System Events" to keystroke "q" using {command down, control down}'
                    subprocess.run(['osascript', '-e', lock_script])
                    
                    os._exit(0)
                
                time.sleep(0.05)
                
        except KeyboardInterrupt:
            # Biri panikleyip Ctrl+C ile programı durdurmaya çalışırsa, anında ekranı kilitle
            lock_script = 'tell application "System Events" to keystroke "q" using {command down, control down}'
            subprocess.run(['osascript', '-e', lock_script])
            os._exit(0)

if __name__ == "__main__":
    trap = BoobyTrap()
    trap.start()
