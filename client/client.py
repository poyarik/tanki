import tkinter as tk
from render import Renderer
from network import ClientNetwork
from input import InputHandler
from menu import MainMenu

# открываем меню
menu = MainMenu()
menu.run()  # меню блокирует до закрытия

# после закрытия меню настройки уже сохранены в JSON
settings = menu.settings  # можно использовать сохранённые/выбранные игроком значения

name = settings["name"]
ip = settings["ip"]
port = int(settings["port"])
tank = settings["tank"]

root = tk.Tk()
root.title("Танки Оффлайн: Страшные Кони")

net = ClientNetwork(host=ip, port=port)
net.connect()

renderer = Renderer(root, net)

inputs = InputHandler(root, net, renderer)


net.send({"type": "join", "name": name, "tank": tank})

def game_loop():
    # забираем все состояния от сервера
    while not net.incoming.empty():
        msg = net.incoming.get()
        if msg["type"] == "state":
            inputs.on_mouse_move()
            renderer.render(msg["data"])

    root.after(33, game_loop)  # ~30 FPS

game_loop()
root.mainloop()