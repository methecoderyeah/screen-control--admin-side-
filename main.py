from socketcommands import SocketCommands
import tkinter as tk
from PIL import Image, ImageTk
import GUI
import pandas as pd
import tkinter.simpledialog as sd
from biginput import big_askstring

#pandas user dataframe
df = pd.DataFrame({
    'Users:': [''],
    'Processes': ['']
    })


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

GUI_ = GUI.MainPage(window, df)

#functions
sc = SocketCommands()
def freeze_screens():
    sc.messenger.freeze()
    if GUI_.freeze_screens_button["text"] == "Freeze All Screens":
        GUI_.freeze_screens_button.config(text="Unfreeze Screens")
    elif GUI_.freeze_screens_button["text"] == "Unfreeze Screens":
        GUI_.freeze_screens_button.config(text="Freeze All Screens")
def refresh_buttons():
    sc.messenger.processes()
    thread, messages = sc.receiver.listen_for_3_seconds()
    def finish_refresh():
        thread.join()
        clean = [msg for msg, addr in messages]
        rows = []
        for entry in clean:
            rows.append({
                "Users:": entry.get("Sender", None),
                "Processes": entry.get("Processes", None)
            })
        df = pd.DataFrame(rows)
        df = df.dropna()
        if df.empty:
            df = pd.DataFrame({
                "Users:": [""],
                "Processes": [""]
            })
        GUI_.update_table(df)
    window.after(1500, finish_refresh)
def reset_port():
    password = big_askstring("Change Port", "Password")
    if password:
        port = big_askstring("Change Port", "Enter new port:")
        with open("./socket.txt", "w") as file:
            file.write(port)



GUI_.initialize_freeze_button(freeze_screens)
GUI_.initialize_refresh_button(refresh_buttons)
GUI_.initialize_change_port_button(reset_port)

window.mainloop()
