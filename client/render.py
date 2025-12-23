import tkinter as tk

class Renderer:
    def __init__(self, root, width=800, height=600):
        self.root = root
        self.width = width
        self.height = height

        self.canvas = tk.Canvas(
            root,
            width=width,
            height=height,
            bg="black"
        )
        self.canvas.pack()


    def render(self, state: dict):
        """
        state = {
            "tanks": [...],
            "bullets": [...]
        }
        """
        self.canvas.delete("all")

        self.draw_tanks(state.get("tanks", []))
        self.draw_bullets(state.get("bullets", []))

    def draw_tanks(self, tanks):
        for tank in tanks:
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
                fill="green"
            )

            # имя игрока
            self.canvas.create_text(
                x, y - 25,
                text=name,
                fill="white"
            )

            # hp
            self.canvas.create_text(
                x, y + 25,
                text=f"HP: {hp}",
                fill="red"
            )

    def draw_bullets(self, bullets):
        for bullet in bullets:
            x = bullet["x"]
            y = bullet["y"]

            self.canvas.create_oval(
                x - 4, y - 4,
                x + 4, y + 4,
                fill="yellow"
            )
