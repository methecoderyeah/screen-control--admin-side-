import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from pandas_dataframe_to_table import df_to_treeview


class MainPage:
    def __init__(self, window, data):
        self.window = window
        self.ttk_()
        self.stretch_grid()
        self.destroy_all()
        self.build(data)

    def stretch_grid(self):
        for col in range(3):
            self.window.grid_columnconfigure(col, weight=1, uniform="topbar")
        for row in range(30):
            self.window.grid_rowconfigure(row, weight=1)

        self.window.grid_rowconfigure(6, weight=20)

    def destroy_all(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def ttk_(self):
        style = ttk.Style(self.window)
        style.theme_use("default")
        style = ttk.Style(self.window)

        style.configure("Treeview",
            background="#E3F2FD",
            foreground="#000000",
            rowheight=35,
            fieldbackground="#E3F2FD",
            font=("SF Pro Text", 14)
        )

        style.configure("Treeview.Heading",
            background="#8CC0EB",
            foreground="#FFF9D2",
            font=("SF Pro Text", 16, "bold")
        )

        style.map("Treeview",
            background=[("selected", "#8CC0EB")],
            foreground=[("selected", "#FFFFFF")]
        )


    def build(self, data):
        def row_0():
            welcome_label = tk.Label(
                self.window,
                text="Welcome",
                fg="#FFF9D2",
                bg="#BFDDF0",
                font=("SF Pro Text", 100)
            )
            welcome_label.grid(row=0, column=1, pady=(15, 0), sticky="s")

            img_left = Image.open("images/capybara.png")
            img_left = img_left.resize((150, 150), Image.LANCZOS)
            tk_left = ImageTk.PhotoImage(img_left)
            left_label = tk.Label(self.window, image=tk_left, bg="#BFDDF0")
            left_label.image = tk_left
            left_label.grid(row=0, column=0, sticky="s", padx=75)

            img_right = Image.open("images/capybara.png")
            img_right = img_right.transpose(Image.FLIP_LEFT_RIGHT)
            img_right = img_right.resize((150, 150), Image.LANCZOS)
            tk_right = ImageTk.PhotoImage(img_right)
            right_label = tk.Label(self.window, image=tk_right, bg="#BFDDF0")
            right_label.image = tk_right
            right_label.grid(row=0, column=2, sticky="s", padx=75)

        row_0()

        def hr(row):
            bar = tk.Frame(self.window, height=3, bg="#8CC0EB")
            bar.grid(row=row, column=0, columnspan=3, padx=45, sticky="ew")

        hr(1)

        def row_2():
            controls_label = tk.Label(
                self.window,
                text="Controls:",
                fg="#FFF9D2",
                bg="#BFDDF0",
                font=("SF Pro Text", 50)
            )
            controls_label.grid(row=2, column=0, padx=50)

        row_2()

        def controls():
            controls_frame = tk.Frame(self.window, bg="#BFDDF0")
            controls_frame.grid(row=3, column=0, columnspan=3, pady=20, padx=300, sticky="w")

            button_img = Image.open("images/rounded_button.png")
            button_img = button_img.resize((257, 124), Image.LANCZOS)
            button_tk = ImageTk.PhotoImage(button_img)

            def make_button(text, col):
                btn = tk.Button(
                    controls_frame,
                    image=button_tk,
                    text=text,
                    compound="center",
                    fg="#FFF9D2",
                    font=("SF Pro Text", 20),
                    borderwidth=0,
                    highlightthickness=0,
                    bg="#BFDDF0",
                    activebackground="#BFDDF0",
                    width=257,
                    height=124,
                    activeforeground="#E6D86A",
                    padx=25
                )
                btn.image = button_tk
                btn.grid(row=0, column=col)
                return btn

            self.freeze_screens_button = make_button("Freeze All Screens", 0)
            self.refresh_button = make_button("Refresh Data", 1)
            self.change_port_button = make_button("Change Port", 2)

        controls()

        hr(4)

        def row_5():
            screens_label = tk.Label(
                self.window,
                text="Screens:",
                fg="#FFF9D2",
                bg="#BFDDF0",
                font=("SF Pro Text", 50)
            )
            screens_label.grid(row=5, column=0, padx=50)

        row_5()

        def table(data):
            table_widget = df_to_treeview(self.window, data)
            table_widget.grid(row=6, column=0, columnspan=3, padx=50, pady=20, sticky="nsew")
        table(data)
        
    def initialize_freeze_button(self, command):
        self.freeze_screens_button.config(command=command)
    def initialize_refresh_button(self, command):
        self.refresh_button.config(command=command)
    def initialize_change_port_button(self, command):
        self.change_port_button.config(command=command)
