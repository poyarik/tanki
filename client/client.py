import tkinter as tk
from render import Renderer
from network import ClientNetwork
from input import InputHandler

name = input("Enter your name: ")

root = tk.Tk()
root.title("Танки Оффлайн: Страшные Кони")

renderer = Renderer(root)
net = ClientNetwork()
net.connect()

inputs = InputHandler(root, net)


net.send({"type": "join", "name": name})

def game_loop():
    # забираем все состояния от сервера
    while not net.incoming.empty():
        msg = net.incoming.get()
        if msg["type"] == "state":
            renderer.render(msg["data"])

    root.after(33, game_loop)  # ~30 FPS

game_loop()
root.mainloop()