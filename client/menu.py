import tkinter as tk
from tkinter import messagebox
import json
import os

SETTINGS_FILE = "settings.json"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    # стандартные настройки
    return {
        "name": "Player",
        "ip": "127.0.0.1",
        "port": 12345,
        "tank": "medium"
    }

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

class MainMenu:
    def __init__(self):
        self.settings = load_settings()

        self.root = tk.Tk()
        self.root.title("World Of Tangens")
        self.root.geometry("400x500")

        tk.Label(self.root, text="Имя игрока:").pack(pady=5)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack(pady=5)
        self.name_entry.insert(0, self.settings.get("name", "Player"))

        tk.Label(self.root, text="Сервер IP:").pack(pady=5)
        self.ip_entry = tk.Entry(self.root)
        self.ip_entry.pack(pady=5)
        self.ip_entry.insert(0, self.settings.get("ip", "127.0.0.1"))

        tk.Label(self.root, text="Порт:").pack(pady=5)
        self.port_entry = tk.Entry(self.root)
        self.port_entry.pack(pady=5)
        self.port_entry.insert(0, str(self.settings.get("port", 12345)))

        tk.Label(self.root, text="Выбор танка:").pack(pady=5)
        self.tank_var = tk.StringVar(value=self.settings.get("tank", "light"))
        tanks = ["light", "medium", "heavy"]
        for t in tanks:
            tk.Radiobutton(self.root, text=t.capitalize(), variable=self.tank_var, value=t).pack(anchor="w")

        tk.Button(self.root, text="Старт", command=self.start_game).pack(pady=20)

    def start_game(self):
        name = self.name_entry.get()
        ip = self.ip_entry.get()
        port = self.port_entry.get()
        tank = self.tank_var.get()


        if not name:
            messagebox.showerror("Ошибка", "Введите имя игрока")
            return

        # сохраняем настройки
        save_settings({
            "name": name,
            "ip": ip,
            "port": int(port),
            "tank": tank
        })

        self.settings = {
            "name": name,
            "ip": ip,
            "port": int(port),
            "tank": tank
        }

        # тут можно вызывать функцию запуска клиента
        # start_client(name, ip, int(port), color)
        print("Запуск игры с данными:", name, ip, port, tank)
        self.root.destroy()

    def run(self):
        self.root.mainloop()

