from socketcommands import SocketCommands
import tkinter as tk
from PIL import Image, ImageTk
import GUI
import pandas as pd
from biginput import big_askstring
from cryptography.fernet import Fernet
import numpy as np

# ---------------- INITIAL DATAFRAME ----------------
df = pd.DataFrame({
    'Users:': [''],
    'Processes': ['']
})

# ---------------- WINDOW SETUP ----------------
window = tk.Tk()
window.title('Screen Admin Controls')
window.state("zoomed")
window.config(bg="#BFDDF0")

# Icon
icon_img = Image.open("./images/capybara.png")
icon_img = icon_img.resize((64, 64), Image.LANCZOS)
icon_tk = ImageTk.PhotoImage(icon_img)
window.iconphoto(True, icon_tk)

GUI_ = GUI.MainPage(window, df)

# ---------------- SOCKET SETUP ----------------
commander = SocketCommands()
commander.receiver.thread()

# Buffers
tcp_messages = []
pending_image_windows = {}   # user → label widget


# ---------------- IMAGE POPUP ----------------
def open_image_window(user):
    commander.messenger.send_images(user)

    win = tk.Toplevel(window)
    win.title(f"Screen of {user}")
    win.config(bg="#BFDDF0")

    label = tk.Label(win, bg="#BFDDF0")
    label.pack(padx=20, pady=20)

    pending_image_windows[user] = label


# ---------------- TCP MESSAGE HANDLER ----------------
def on_tcp_message(message):
    # Handle incoming image
    if message.get("Command") == "Images":
        user = message.get("Sender")
        rgb = message.get("RGB")

        if user in pending_image_windows:
            label = pending_image_windows[user]

            arr = np.array(rgb, dtype=np.uint8)
            img = Image.fromarray(arr)
            tk_img = ImageTk.PhotoImage(img)

            label.config(image=tk_img)
            label.image = tk_img

        return

    # Otherwise treat as normal Processes message
    tcp_messages.append(message)


commander.receiver.on_message = on_tcp_message


# ---------------- FREEZE BUTTON ----------------
def freeze_all_screens():
    commander.messenger.send_freeze("")
    if GUI_.freeze_screens_button["text"] == "Freeze All Screens":
        GUI_.screens_frozen = True
        GUI_.freeze_screens_button.config(text="Unfreeze Screens")
    else:
        GUI_.screens_frozen = False
        GUI_.freeze_screens_button.config(text="Freeze All Screens")


# ---------------- REFRESH BUTTON ----------------
def refresh_buttons():
    commander.messenger.processes("")

    def finish_refresh():
        if not tcp_messages:
            GUI_.update_table(pd.DataFrame({
                "Users:": [""],
                "Processes": [""]
            }))
            return

        rows = []
        for entry in tcp_messages:
            rows.append({
                "Users:": entry.get("Sender", ""),
                "Processes": entry.get("Processes", "")
            })

        tcp_messages.clear()

        df_new = pd.DataFrame(rows).dropna()

        if df_new.empty:
            df_new = pd.DataFrame({
                "Users:": [""],
                "Processes": [""]
            })

        GUI_.update_table(df_new)

    window.after(800, finish_refresh)


# ---------------- PASSWORD + CHANGE PORT ----------------
cipher = Fernet("uaXbNuTAUXK5o191j94JxiWpCgmBCD3zaft-Ooc2zCg=")
STORED_PASSWORD = "ADMIN_RSegG4sp5BHjDv6KQJFEMmah9Vt3wZ"

def reset_port():
    password = big_askstring("Change Port", "Password")
    if not password:
        return

    if password != STORED_PASSWORD:
        return

    new_port = big_askstring("Change Port", "Enter new port:")
    if not new_port:
        return

    with open("./socket.txt", "w") as file:
        file.write(new_port)

    encrypted_password = cipher.encrypt(password.encode()).decode()

    commander.messenger.send_change_port(encrypted_password, new_port)


# ---------------- GUI BUTTONS ----------------
GUI_.initialize_freeze_button(freeze_all_screens)
GUI_.initialize_refresh_button(refresh_buttons)
GUI_.initialize_change_port_button(reset_port)

# ---------------- ROW CLICK HANDLER ----------------
def on_row_clicked(user):
    open_image_window(user)

GUI_.on_row_clicked = on_row_clicked

window.mainloop()
