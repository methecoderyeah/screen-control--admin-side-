import json
import socket

class SocketCommands:
    def __init__(self):
        self.port = self.get_socket()
        self.messenger = self.Messenger(self)

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
            json_data = json.dumps(data)
            self.send_message(json_data)

        def send_images(self, target):
            data = {
                "Sender": "Screen Control",
                "Target": target,
                "Command": "Send Images"
            }
            json_data = json.dumps(data)
            self.send_message(json_data)

        def reset_socket(self, new_socket, password):
            data = {
                "Sender": "Screen Control",
                "Command": "Reset Socket",
                "Socket" : new_socket,
                "Password": password
            }
            json_data = json.dumps(data)
            self.send_message(json_data)

    class Receiver:
        pass
