import os
import sys
import time
from datetime import datetime
import cv2
import tkinter as tk
import ctypes
from pynput import keyboard, mouse

# --- AYARLAR ---
# Windows için varsayılan fotoğraf kaydetme dizini (Masaüstü)
SAVE_DIR = os.path.join(os.environ["USERPROFILE"], "Desktop", "Intruder_Photos")

# Tuzağı sessizce kapatmak için gereken gizli tuş kombinasyonu (Sırasıyla basılmalı)
SECRET_COMBO = ['t', 'r']

# Ekrana tam ekran basılacak resim. Kullanmak istemiyorsanız içini boş bırakın.
SHAME_IMAGE_PATH = "shame_image.jpg" 

def show_countdown():
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes('-topmost', True)
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - 250
    y = (screen_height // 2) - 125
    root.geometry(f"500x250+{x}+{y}")
    root.configure(bg='#1e1e1e')
    
    label = tk.Label(root, text="3", font=("Helvetica", 80, "bold"), fg="white", bg="#1e1e1e")
    label.pack(expand=True)
    
    def update_timer(count):
        if count > 0:
            label.config(text=str(count))
            root.after(250, update_timer, count-1)
        else:
            label.config(text="Tuzak Devrede!", font=("Helvetica", 50, "bold"), fg="#ff4444")
            def close_down():
                root.destroy()
                root.quit()
            root.after(250, close_down)
            
    root.after(250, update_timer, 3)
    root.mainloop()

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

        if char == SECRET_COMBO[self.combo_index]:
            self.combo_index += 1
            if self.combo_index == len(SECRET_COMBO):
                self.armed = False
                print("Tuzak başarıyla devre dışı bırakıldı.")
                os._exit(0)
            return
        else:
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
        mouse_listener = mouse.Listener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll)
        keyboard_listener = keyboard.Listener(on_press=self.on_press)
        
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
                        img = cv2.imread(SHAME_IMAGE_PATH)
                        if img is not None:
                            cv2.namedWindow("Tuzak", cv2.WINDOW_NORMAL)
                            cv2.setWindowProperty("Tuzak", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                            cv2.setWindowProperty("Tuzak", cv2.WND_PROP_TOPMOST, 1)
                            
                            for _ in range(20):
                                cv2.imshow("Tuzak", img)
                                cv2.waitKey(100) # 2 saniye
                                
                            cv2.destroyAllWindows()
                            
                    # 3. Bilgisayarı ZORLA kilit ekranına (Lock Screen) at (Sadece Windows)
                    ctypes.windll.user32.LockWorkStation()
                    
                    os._exit(0)
                
                time.sleep(0.05)
                
        except KeyboardInterrupt:
            # Ctrl+C panik kilidi
            ctypes.windll.user32.LockWorkStation()
            os._exit(0)

if __name__ == "__main__":
    trap = BoobyTrap()
    trap.start()
