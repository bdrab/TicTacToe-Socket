import socket
import pickle


class Network:
    def __init__(self):
        self.connector = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.136"
        self.port = 5555
        self.server_address = (self.server, self.port)
        self.player_id = self.connect()

    def get_player_id(self):
        return self.player_id

    def connect(self):
        try:
            self.connector.connect(self.server_address)
            return self.connector.recv(2048).decode()
        except socket.error:
            pass

    def send(self, data):
        try:
            self.connector.send(str.encode(data))
            return pickle.loads(self.connector.recv(4096))
        except socket.error:
            pass
