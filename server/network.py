# server/network.py
import socket
import threading
from protocol import encode, decode
from queue import Queue

class ServerNetwork:
    def __init__(self, host="127.0.0.1", port=5555, session=None):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen()
        self.clients = {}  # conn -> addr
        self.lock = threading.Lock()
        self.message_queue = Queue()
        self.session = session

    def start(self):
        threading.Thread(target=self.accept_clients, daemon=True).start()
        print(f"Сервер запущен на {self.host}:{self.port}")

    def accept_clients(self):
        while True:
            conn, addr = self.server.accept()
            with self.lock:
                self.clients[conn] = {"addr": addr, "name": None, "tank": None}
            print("Подключился:", addr)
            threading.Thread(target=self.handle_client, args=(conn,), daemon=True).start()

    def handle_client(self, conn):
        buffer = ""
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                buffer += data.decode()
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    message = decode(line.encode())
                    self.on_message(conn, message)
        finally:
            with self.lock:
                if conn in self.clients:
                    print("Отключился:", self.clients[conn])
                    tank_id = self.clients[conn]["tank"]
                    if tank_id is not None:
                        self.session.remove_tank(tank_id)
                    del self.clients[conn]
            conn.close()

    def send(self, conn, message: dict):
        try:
            conn.sendall(encode(message))
        except:
            pass  # клиент мог отключиться

    def broadcast(self, message: dict):
        with self.lock:
            for conn in list(self.clients):
                self.send(conn, message)

    def on_message(self, conn, message: dict):
        if "type" not in message:
            return
        cmd = message["type"]
        if cmd == "join":
            self.clients[conn]["name"] = message.get("name", "Unknown")
            tank_id = self.session.add_tank(200, 200, 0, self.clients[conn]["name"])
            self.clients[conn]["tank"] = tank_id
            self.clients[conn]["input_state"] = {
                "up": False,
                "down": False,
                "left": False,
                "right": False
            }


        self.message_queue.put((conn, message))
