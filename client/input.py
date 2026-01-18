import math


class InputHandler:
    def __init__(self, root, net, renderer):
        self.net = net
        self.renderer = renderer
        self.mouse_x = 0
        self.mouse_y = 0

        # текущее состояние клавиш
        self.state = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
            "turret": 'IDLE'
        }

        root.bind("<KeyPress>", self.on_key_press)
        root.bind("<KeyRelease>", self.on_key_release)
        root.bind("<Motion>", self.on_mouse_move)

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
            self.renderer.shake_screen(7)

        elif key == 'p':
            self.renderer.hit_effect()
            

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

    def on_mouse_move(self, event=None):
        tank = self.renderer.player_tank
        if not tank:
            return
        
        if event:
            self.mouse_x = event.x
            self.mouse_y = event.y

        dx = self.mouse_x - tank['x']
        dy = self.mouse_y - tank['y']

        target_angle = math.atan2(dy, dx)
        diff = self.normalize_angle(math.radians(tank['direction']) - target_angle)

        EPS = 0.13

        if abs(diff) < EPS:
            self.state["turret"] = 'IDLE'
        elif diff > 0:
            self.state["turret"] = 'CCW'
        else:
            self.state["turret"] = 'CW'

        self.send_state()

    def send_state(self):
        self.net.send({
            "type": "input",
            "state": self.state
        })

    @staticmethod
    def normalize_angle(a):
        while a > math.pi:
            a -= 2 * math.pi
        while a < -math.pi:
            a += 2 * math.pi
        return a