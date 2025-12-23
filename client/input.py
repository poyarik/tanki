class InputHandler:
    def __init__(self, root, network):
        self.net = network

        # текущее состояние клавиш
        self.state = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
        }

        root.bind("<KeyPress>", self.on_key_press)
        root.bind("<KeyRelease>", self.on_key_release)

    def on_key_press(self, event):
        key = event.keysym.lower()

        if key == "w":
            self.state["up"] = True
        elif key == "s":
            self.state["down"] = True
        elif key == "a":
            self.state["left"] = True
        elif key == "d":
            self.state["right"] = True
        elif key == "space":
            # стрельба — событие, не состояние
            self.net.send({"type": "shoot"})

        self.send_state()

    def on_key_release(self, event):
        key = event.keysym.lower()

        if key == "w":
            self.state["up"] = False
        elif key == "s":
            self.state["down"] = False
        elif key == "a":
            self.state["left"] = False
        elif key == "d":
            self.state["right"] = False

        self.send_state()

    def send_state(self):
        self.net.send({
            "type": "input",
            "state": self.state
        })