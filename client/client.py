import socket
from protocol import encode, decode
from network import ClientNetwork

net = ClientNetwork()
net.connect()

net.send({"cmd": "join", "name": "poyarik"})

while True:
    command = input("Введите команду: ")
    if command == "quit":
        break
    net.send({"cmd": command})

net.disconnect()