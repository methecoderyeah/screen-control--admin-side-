import tkinter as tk
from PIL import ImageTk, Image

class MainPage:
    def __init__(self, window):
        self.window = window
        self.stretch_grid()
        self.destroy_all()
        self.build()
        
    
    #setup
    def stretch_grid(self):
        for col in range(3):
            self.window.grid_columnconfigure(col, weight=1, uniform="topbar")
        for row in range(30):
            self.window.grid_rowconfigure(row, weight=1)
    def destroy_all(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    #actual window
    def build(self):
        def row_0():
            def welcome_text():
                welcome_label = tk.Label(
                        self.window,
                        text="Welcome",
                        fg="#FFF9D2",
                        bg="#BFDDF0",
                        font=("SF Pro Text", 100))
                welcome_label.grid(row=0, column=1, pady=(15, 0), sticky="s")
            welcome_text()
            
            def right_capybara():
                img_left = Image.open("images/capybara.png")
                img_left = img_left.resize((150, 150), Image.LANCZOS)
                tk_left = ImageTk.PhotoImage(img_left)
                capybara_1_label = tk.Label(self.window, 
                                            image=tk_left, 
                                            bg="#BFDDF0")
                capybara_1_label.image = tk_left
                capybara_1_label.grid(row=0, column=0, sticky="s", padx=75)
            right_capybara()

            def left_capybara():
                img_right = Image.open("images/capybara.png")
                img_right = img_right.transpose(Image.FLIP_LEFT_RIGHT)
                img_right = img_right.resize((150, 150), Image.LANCZOS)
                tk_right = ImageTk.PhotoImage(img_right)
                capybara_2_label = tk.Label(self.window, 
                                            image=tk_right, 
                                            bg="#BFDDF0")
                capybara_2_label.image = tk_right
                capybara_2_label.grid(row=0, column=2, sticky="s", padx=75)
            left_capybara()
        row_0()

        def hr():
            hr_ = tk.Frame(self.window, 
                           height=5, 
                           bg="#8CC0EB")
            hr_.grid(row=1, column=0, columnspan=3, padx=45, sticky="ew")
        hr()
        
        def row_2():
            controls_label = tk.Label(
                self.window,
                text="Controls:",
                fg="#FFF9D2",
                bg="#BFDDF0",
                font=("SF Pro Text", 50))
            controls_label.grid(row=2, column=0, padx=50)
        row_2()

