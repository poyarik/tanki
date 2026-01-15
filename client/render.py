import tkinter as tk
from math import cos, sin, radians

class Renderer:
    def __init__(self, root, net, width=1200, height=600):
        self.root = root
        self.net = net
        self.width = width
        self.height = height
        self.tile_size = 40
        self.rendered = False

        self.player_tank = None

        self.canvas = tk.Canvas(
            root,
            width=width,
            height=height,
            bg="black"
        )
        self.canvas.pack()


    def draw_map1(self, map):
        for y, row in enumerate(map):
            for x, tile in enumerate(row):
                if tile in ("#", "~"):
                    color = {"#": "gray", "~": "blue"}[tile]
                    self.canvas.create_rectangle(
                        x*self.tile_size, y*self.tile_size,
                        (x+1)*self.tile_size, (y+1)*self.tile_size,
                        fill=color, outline=""
                    )

    def draw_map2(self, map):
        block_size = 4  # размер блока внутри тайла (4×4)
        mini_tile = self.tile_size / block_size

        for y, row in enumerate(map):
            for x, tile in enumerate(row):
                if tile == ".":
                    for i in range(block_size):
                        for j in range(block_size):
                            # рисуем только половину блоков шахматкой
                            if (i + j) % 2 == 0:
                                self.canvas.create_rectangle(
                                    x*self.tile_size + i*mini_tile,
                                    y*self.tile_size + j*mini_tile,
                                    x*self.tile_size + (i+1)*mini_tile,
                                    y*self.tile_size + (j+1)*mini_tile,
                                    fill="green",
                                    outline="",
                                    tags="dynamic"
                                )




    def render(self, state: dict):
        """
        state = {
            "tanks": [...],
            "bullets": [...]
        }
        """
        self.canvas.delete("dynamic")

        if not self.rendered:
            self.draw_map1(self.net.map)
            self.rendered = True

        self.draw_tanks(state.get("tanks", []))
        self.draw_bullets(state.get("bullets", []))
        self.draw_map2(self.net.map)
        self.draw_score(state["score"])

    def draw_tanks(self, tanks):
        for tank in tanks:
            if tank['id'] == self.net.tank_id:
                self.player_tank = tank

            x = tank["x"]
            y = tank["y"]
            size = tank.get("size", 10)
            name = tank.get("name", "")
            hp = tank["hp"]

            self.canvas.create_rectangle(
                x - size // 2,
                y - size // 2,
                x + size // 2,
                y + size // 2,
                fill="#f39c12",
                tags="dynamic"
            )

            barrel_x = x + cos(radians(tank["direction"])) * tank["barrel_length"]
            barrel_y = y + sin(radians(tank["direction"])) * tank["barrel_length"]

            self.canvas.create_line(x, y, barrel_x, barrel_y, fill="gray", width=5, tags="dynamic")

            # имя игрока
            self.canvas.create_text(
                x, y - 25,
                text=name,
                fill="white",
                tags="dynamic"
            )

            # hp
            self.canvas.create_text(
                x, y + 25,
                text=f"HP: {hp}",
                fill="red",
                tags="dynamic"
            )

    def draw_bullets(self, bullets):
        for bullet in bullets:
            x = bullet["x"]
            y = bullet["y"]

            self.canvas.create_oval(
                x - 4, y - 4,
                x + 4, y + 4,
                fill="yellow",
                tags="dynamic"
            )

    def draw_score(self, score):
        text = ""
        for player in score:
            text += f"{player[0]}: {player[1]}\n"

        self.canvas.create_text(
            200, 200,
            text=text,
            fill="white",
            font=("Arial", 16),
            tags="dynamic"
        )