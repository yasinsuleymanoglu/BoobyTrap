import tkinter as tk
import sys

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
        # Süreler çeyrek saniyeye (250 milisaniye) indirildi!
        root.after(250, update_timer, count-1)
    else:
        label.config(text="Tuzak Devrede!", font=("Helvetica", 50, "bold"), fg="#ff4444")
        
        def close_down():
            sys.exit(0)
            
        # Kapanış hızı da çeyrek saniye
        root.after(250, close_down)
        
# İlk sayının başlama hızı çeyrek saniye
root.after(250, update_timer, 3)
root.mainloop()
