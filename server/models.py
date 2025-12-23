from math import cos, radians, sin


class Tank:
    _id_counter = 1

    def __init__(self, x: int, y: int, direction: int, name: str):
        self.id = Tank._id_counter
        Tank._id_counter += 1

        self.x = x
        self.y = y
        self.hp = 100
        self.speed = 5
        self.direction = direction  # 0-360 градусов, куда смотрит танк
        self.is_alive = True
        self.size = 10
        self.name = name

    def move(self, dx: int, dy: int):
        if not self.is_alive:
            return
        self.x += dx * self.speed
        self.y += dy * self.speed


    def take_damage(self, dmg: int):
        if not self.is_alive:
            return
        self.hp -= dmg
        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False

    def shoot(self):
        if not self.is_alive:
            return None
        # Возвращаем координаты выстрела, чтобы сервер создал пулю
        return (self.x, self.y, self.direction)

    def serialize(self):
        # для отправки клиенту
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "direction": self.direction,
            "hp": self.hp,
            "alive": self.is_alive,
            "name": self.name
        }
    

class Bullet:
    _id_counter = 1

    def __init__(self, x: int, y: int, direction: int):
        self.id = Bullet._id_counter
        Bullet._id_counter += 1

        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 10
        self.damage = 10

    def move(self):
        self.x += self.speed * cos(radians(self.direction))
        self.y += self.speed * sin(radians(self.direction))

    def serialize(self):
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "direction": self.direction
        }
    