from socketcommands import SocketCommands
import tkinter as tk
from PIL import Image, ImageTk
import GUI
import pandas as pd
from biginput import big_askstring
from cryptography.fernet import Fernet

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

# Buffer for incoming TCP messages
tcp_messages = []

def on_tcp_message(message):
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

    # Check password
    if password != STORED_PASSWORD:
        return

    # Ask for new port
    new_port = big_askstring("Change Port", "Enter new port:")
    if not new_port:
        return

    # Save new port locally
    with open("./socket.txt", "w") as file:
        file.write(new_port)

    # Encrypt password for sending to clients
    encrypted_password = cipher.encrypt(password.encode()).decode()

    # Send ChangePort command with 2 arguments
    commander.messenger.send_change_port(encrypted_password, new_port)


# ---------------- GUI BUTTONS ----------------
GUI_.initialize_freeze_button(freeze_all_screens)
GUI_.initialize_refresh_button(refresh_buttons)
GUI_.initialize_change_port_button(reset_port)

window.mainloop()
