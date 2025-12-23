# client/network.py
import socket
import threading
from protocol import encode, decode
from queue import Queue

class ClientNetwork:
    def __init__(self, host="127.0.0.1", port=5555):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.incoming = Queue()  # очередь входящих сообщений

    def connect(self):
        self.client.connect((self.host, self.port))
        threading.Thread(target=self.listen, daemon=True).start()

    def listen(self):
        buffer = ""
        try:
            while True:
                data = self.client.recv(1024)
                if not data:
                    break
                buffer += data.decode()
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    message = decode(line.encode())
                    self.incoming.put(message)
        except:
            pass

    def send(self, message: dict):
        try:
            self.client.sendall(encode(message))
        except:
            pass

    def disconnect(self):
        self.client.close()
