import json
import socket
import threading
import time

class SocketCommands:
    def __init__(self):
        self.port = self.get_socket()
        self.messenger = self.Messenger(self)
        self.receiver = self.Receiver(self)

    def get_socket(self):
        with open("./socket.txt", "r") as file:
            return int(file.read().strip())

    class Messenger:
        def __init__(self, parent):
            self.parent = parent
        
        def send_message(self, message):
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(message.encode(), ("<broadcast>", self.parent.port))
            sock.close()

        def freeze(self, target="ALL"):
            data = {
                "Sender": "Screen Control",
                "Target": target,
                "Command": "Freeze"
            }
            self.send_message(json.dumps(data))

        def send_images(self, target="ALL"):
            data = {
                "Sender": "Screen Control",
                "Target": target,
                "Command": "SendImages"
            }
            self.send_message(json.dumps(data))

        def reset_socket(self, new_socket, password):
            data = {
                "Sender": "Screen Control",
                "Command": "ResetSocket",
                "Socket": new_socket,
                "Password": password
            }
            self.send_message(json.dumps(data))

            with open("socket.txt", "w") as file:
                file.write(str(new_socket))
        
        def processes(self, target="ALL"):
            data = {
                "Sender": "Screen Control",
                "Command": "ReProc",
                "Target": target
            }
            self.send_message(json.dumps(data))


    class Receiver:
        def __init__(self, parent):
            self.parent = parent

        def listen_for_3_seconds(self):
            messages = []

            def listener():
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.bind(("", self.parent.port))
                sock.setblocking(False)

                end_time = time.time() + 1

                while time.time() < end_time:
                    try:
                        data, addr = sock.recvfrom(1024)
                        text = data.decode("utf-8")
                        json_data = json.loads(text)
                        messages.append((json_data, addr))
                    except BlockingIOError:
                        pass
                    time.sleep(0.01)

                sock.close()

            thread = threading.Thread(target=listener, daemon=True)
            thread.start()
            return thread, messages

