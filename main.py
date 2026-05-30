import win32api
import win32service
import win32con
import win32event
import win32serviceutil
import socket
import json
import tkinter as tk

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
#use https://colorhunt.co/palette/fff9d2ffebccbfddf08cc0eb as the color palatte for this
window = tk.Tk()
window.title('Screen Admin Controls')
window.state("zoomed")
icon = tk.PhotoImage(file="./images/capybara.png")
window.iconphoto(True, icon)
window.config(bg="#BFDDF0")

#main page:
controls_label = tk.Label(text="Controls:", fg="#FFF9D2")
controls_label.pack()

window.mainloop()