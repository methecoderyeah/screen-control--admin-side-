import tkinter.simpledialog as sd
import tkinter as tk

class BigInput(sd._QueryString):
    def body(self, master):
        # Make window bigger
        self.geometry("450x200")

        tk.Label(master, text=self.prompt, font=("SF Pro Text", 20)).pack(pady=20)

        self.entry = tk.Entry(master, font=("SF Pro Text", 18), width=25)
        self.entry.pack(pady=10)
        return self.entry
    
def big_askstring(title, prompt):
    root = tk._default_root
    return BigInput(title, prompt, parent=root).result