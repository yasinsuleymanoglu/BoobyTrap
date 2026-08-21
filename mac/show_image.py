import sys
import tkinter as tk
import os

if len(sys.argv) < 2:
    sys.exit(1)
    
ppm_path = sys.argv[1]

if os.path.exists(ppm_path):
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.configure(bg="black")
    
    photo = tk.PhotoImage(file=ppm_path)
    label = tk.Label(root, image=photo, bg="black")
    label.pack(expand=True)
    
    def close_viewer():
        root.destroy()
        root.quit()
        
    # Görüntü ekranda kalma süresi 1500ms'den 2000ms'ye (2 saniye) çıkarıldı
    root.after(2000, close_viewer)
    root.mainloop()

sys.exit(0)
