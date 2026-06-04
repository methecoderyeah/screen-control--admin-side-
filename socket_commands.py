import socket
import json
import threading

class SocketCommands:
    def __init__(self):
        self.port = self.find_port()
        self.clients = []  # connected data-channel clients
        self.control_clients = []  # connected control-channel clients (port 2359)

        self.on_message = None  # callback for main.py

        self.messenger = self.Messenger(self)
        self.receiver = self.Receiver(self)

    def find_port(self):
        with open("socket.txt", "r") as file:
            return int(file.read())

    # ---------------------- MESSENGER ----------------------
    class Messenger:
        def __init__(self, parent):
            self.parent = parent

        def send_message(self, message):
            dead = []
            for client in self.parent.clients:
                try:
                    client.sendall(message.encode())
                except:
                    dead.append(client)

            for dc in dead:
                self.parent.clients.remove(dc)

            print("Sent:", message)

        def send_freeze(self, target):
            data = {
                "Sender": "ScreenFreezer",
                "Target": target if target else "ALL",
                "Command": "Freeze"
            }
            self.send_message(json.dumps(data))

        def send_images(self, target):
            data = {
                "Sender": "ScreenFreezer",
                "Target": target,
                "Command": "Images"
            }
            self.send_message(json.dumps(data))

        def processes(self, target):
            data = {
                "Sender": "ScreenFreezer",
                "Target": target if target else "ALL",
                "Command": "Processes"
            }
            self.send_message(json.dumps(data))

        def send_change_port(self, new_port):
            data = {
                "Sender": "ScreenFreezer",
                "Target": "ALL",
                "Command": "ChangePort",
                "NewPort": new_port
            }

            # Always send ChangePort on TCP port 2359
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.connect(("127.0.0.1", 2359))
                sock.sendall(json.dumps(data).encode())
            finally:
                sock.close()

            print("Sent ChangePort:", new_port)

    # ---------------------- RECEIVER ----------------------
    class Receiver:
        def __init__(self, parent):
            self.parent = parent

        # ---- DATA SERVER (Freeze, Processes, Images) ----
        def start_data_server(self):
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind(("0.0.0.0", self.parent.port))
            server.listen()

            print(f"Data TCP server listening on port {self.parent.port}")

            while True:
                client_socket, addr = server.accept()
                print("Data client connected:", addr)
                self.parent.clients.append(client_socket)

                threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, False),
                    daemon=True
                ).start()

        # ---- CONTROL SERVER (ChangePort) ----
        def start_control_server(self):
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind(("0.0.0.0", 2359))
            server.listen()

            print("Control TCP server listening on port 2359")

            while True:
                client_socket, addr = server.accept()
                print("Control client connected:", addr)
                self.parent.control_clients.append(client_socket)

                threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, True),
                    daemon=True
                ).start()

        # ---- MESSAGE HANDLER ----
        def handle_client(self, client_socket, is_control):
            while True:
                try:
                    data = client_socket.recv(4096)
                    if not data:
                        break

                    try:
                        message = json.loads(data.decode())
                        print("Received:", message)

                        # Pass message to main.py
                        if self.parent.on_message:
                            self.parent.on_message(message)

                    except:
                        print("Invalid JSON:", data)

                except:
                    break

            client_socket.close()

            if is_control:
                self.parent.control_clients.remove(client_socket)
                print("Control client disconnected")
            else:
                self.parent.clients.remove(client_socket)
                print("Data client disconnected")

        # ---- START BOTH SERVERS ----
        def thread(self):
            threading.Thread(target=self.start_data_server, daemon=True).start()
            threading.Thread(target=self.start_control_server, daemon=True).start()
