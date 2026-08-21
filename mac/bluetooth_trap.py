import os
import sys
import time
import subprocess
from datetime import datetime
import cv2
import objc
from CoreBluetooth import CBCentralManager, NSObject
from Foundation import NSRunLoop, NSDate, NSDictionary, NSNumber
from pynput import keyboard, mouse

# --- AYARLAR ---
TARGET_UUID = "BURAYA_TELEFONUNUZUN_UUID_KODUNU_YAZIN"
RSSI_THRESHOLD = -65  # Bu mesafeden uzaklaşırsanız tuzak KURULUR. (-50 yaparsanız çok daha kısa mesafede tetiklenir)
TIMEOUT_SECONDS = 15  

SAVE_DIR = os.path.expanduser("~/Desktop/Intruder_Photos")
SHAME_IMAGE_PATH = os.path.join(os.path.dirname(__file__), "shame_image.ppm")

class ProximityTrap:
    def __init__(self):
        self.armed = False
        self.triggered = False
        self.triggered_reason = None
        self.last_seen = time.time()
        self.last_rssi = -100
        self.bad_signal_start_time = None
        self.good_signal_start_time = None
        
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)
            
        print("🛡️ BLUETOOTH OTO-TUZAK AKTİF! 🛡️")
        print("Sistem telefonunuzu izliyor...")
        print("- Masadan kalkıp uzaklaştığınızda bilgisayarınız sinsice 'Tuzak Moduna' geçer.")
        print("- Tuzak modundayken biri fareye dokunursa kilitlenir!")
        print("(Durdurmak için Ctrl+C'ye basın)\n")

    def arm_trap(self):
        if not self.armed and not self.triggered:
            self.armed = True
            print("\n[!] Patron masadan ayrıldı. TUZAK KURULDU! (Kimse dokunmasın)")
            subprocess.run(["osascript", "-e", 'display notification "Masa terk edildi, güvenlik tuzağı aktif. Kimse dokunmasın!" with title "Oto-Tuzak"'])

    def disarm_trap(self):
        if self.armed and not self.triggered:
            self.armed = False
            print("\n[+] Patron geri döndü. Tuzak devreden çıktı.")
            subprocess.run(["osascript", "-e", 'display notification "Patron döndü, güvenlik devreden çıktı." with title "Oto-Tuzak"'])

    def trigger_from_thread(self, reason):
        if not self.armed or self.triggered:
            return
        self.triggered = True
        self.triggered_reason = reason  # Ana döngüye sinyal gönderiyoruz

    def execute_trigger(self):
        # Bilerek ekrana bir şey basmıyoruz ki kurban ne olduğunu anlamasın
        
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
        
        # 2. Opsiyonel: Uyarı görseli
        if SHAME_IMAGE_PATH and os.path.exists(SHAME_IMAGE_PATH):
            viewer_path = os.path.join(os.path.dirname(__file__), "show_image.py")
            subprocess.run([sys.executable, viewer_path, SHAME_IMAGE_PATH])
                
        # 3. Kilit Ekranına At
        lock_script = 'tell application "System Events" to keystroke "q" using {command down, control down}'
        subprocess.run(['osascript', '-e', lock_script])
        
        os._exit(0)

    def on_press(self, key):
        if self.armed:
            self.trigger_from_thread("Klavyeye basıldı!")

    def on_move(self, x, y):
        if self.armed:
            self.trigger_from_thread("Fare hareket ettirildi!")

    def on_click(self, x, y, button, pressed):
        if self.armed and pressed:
            self.trigger_from_thread("Fareye tıklandı!")

    def on_scroll(self, x, y, dx, dy):
        if self.armed:
            self.trigger_from_thread("Fare tekerleği kullanıldı!")

trap_instance = ProximityTrap()

class BLEScanner(NSObject):
    def centralManagerDidUpdateState_(self, manager):
        if manager.state() == 5:
            options = NSDictionary.dictionaryWithObject_forKey_(NSNumber.numberWithBool_(True), "kCBScanOptionAllowDuplicates")
            manager.scanForPeripheralsWithServices_options_(None, options)

    def centralManager_didDiscoverPeripheral_advertisementData_RSSI_(self, manager, peripheral, data, rssi):
        uuid = peripheral.identifier().UUIDString()
        if uuid == TARGET_UUID:
            trap_instance.last_seen = time.time()
            trap_instance.last_rssi = rssi
            
            if rssi < RSSI_THRESHOLD:
                trap_instance.good_signal_start_time = None
                if trap_instance.bad_signal_start_time is None:
                    trap_instance.bad_signal_start_time = time.time()
                elif time.time() - trap_instance.bad_signal_start_time > 3.0:
                    trap_instance.arm_trap()
            else:
                trap_instance.bad_signal_start_time = None
                if trap_instance.good_signal_start_time is None:
                    trap_instance.good_signal_start_time = time.time()
                elif time.time() - trap_instance.good_signal_start_time > 2.0:
                    trap_instance.disarm_trap()

def main():
    mouse_listener = mouse.Listener(on_move=trap_instance.on_move, on_click=trap_instance.on_click, on_scroll=trap_instance.on_scroll)
    keyboard_listener = keyboard.Listener(on_press=trap_instance.on_press)
    mouse_listener.start()
    keyboard_listener.start()

    scanner = BLEScanner.alloc().init()
    manager = CBCentralManager.alloc().initWithDelegate_queue_(scanner, None)
    
    try:
        run_loop = NSRunLoop.currentRunLoop()
        last_print_time = 0
        
        while True:
            run_loop.runMode_beforeDate_("kCFRunLoopDefaultMode", NSDate.dateWithTimeIntervalSinceNow_(0.1))
            
            if trap_instance.triggered_reason:
                print("") 
                trap_instance.execute_trigger()
            
            current_time = time.time()
            time_since_last = current_time - trap_instance.last_seen
            
            if time_since_last > TIMEOUT_SECONDS:
                if trap_instance.last_rssi >= RSSI_THRESHOLD:
                    pass
                else:
                    trap_instance.arm_trap()
            
            if current_time - last_print_time >= 1.0:
                status_code = 0 if trap_instance.armed else 1
                sys.stdout.write(f"\r[sys.bluetooth.daemon] pid: 4892 | heart_beat_status: {status_code} | mem_usage: 0.1%    ")
                sys.stdout.flush()
                last_print_time = current_time
                
    except KeyboardInterrupt:
        manager.stopScan()
        print("\n\nKalkan kapatıldı.")

if __name__ == '__main__':
    main()
