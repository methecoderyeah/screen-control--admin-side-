import socket
import tkinter as tk
from PIL import Image, ImageTk
import GUI
import pandas as pd

#pandas user dataframe
df = pd.DataFrame({
    'Users:': ["Yaoyu"],
    'Processes': [["edge", "GUI", "MCE", "Visual Studio Code"]],
    'More': ["Button Will Go Here Eventually."]})

#socket commands

#send commands
def send(command):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    message = command.encode("utf-8")
    s.sendto(message, ("<broadcast>", port)) #change this to change port

#recieve images and name of user
def listen():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", port)) #change this to change port

    print(f"Listening for UDP broadcasts on port {port}...")

    while True:
        data, addr = s.recvfrom(port)
        message = data.decode("utf-8")
        print(f"Received from {addr}: {message}")

port = 4467

#  ~~GUI~~~

#window setup:
window = tk.Tk()
window.title('Screen Admin Controls')
window.state("zoomed")
window.config(bg="#BFDDF0")

# Load icon using PIL
icon_img = Image.open("./images/capybara.png")
icon_img = icon_img.resize((64, 64), Image.LANCZOS)
icon_tk = ImageTk.PhotoImage(icon_img)
window.iconphoto(True, icon_tk)

GUI.MainPage(window, df)

window.mainloop()
