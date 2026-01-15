from math import cos, radians, sin

import time

class Tank:
    _id_counter = 1

    def __init__(self, x: int, y: int, direction: int, name: str, tank_type: str):
        self.id = Tank._id_counter
        Tank._id_counter += 1


        self.x = x
        self.y = y
        self.is_alive = True
        self.direction = direction  # 0-360 градусов, куда смотрит танк
        self.name = name
        self.tank_type = tank_type
        self.next_shot_time = 0
        self.death_time = None

        if tank_type == "medium":
            self.max_hp = 100
            self.speed = 5
            self.size = 38
            self.barrel_length = 30  # длина ствола для выстрела
            self.rotation_speed = 5  # скорость поворота танка
            self.fire_rate = 0.5  # секунд между выстрелами
            self.damage = 10

        elif tank_type == "heavy":
            self.max_hp = 150
            self.speed = 3
            self.size = 76
            self.barrel_length = 60  # длина ствола для выстрела
            self.rotation_speed = 3  # скорость поворота танка
            self.fire_rate = 1.0  # секунд между выстрелами
            self.damage = 20

        elif tank_type == "light":
            self.max_hp = 70
            self.speed = 7
            self.size = 30
            self.barrel_length = 20  # длина ствола для выстрела
            self.rotation_speed = 7  # скорость поворота танка
            self.fire_rate = 0.2  # секунд между выстрелами
            self.damage = 10

        self.hp = self.max_hp

    def can_shoot(self):
        return time.time() >= self.next_shot_time

    def take_damage(self, dmg: int):
        if not self.is_alive:
            return
        self.hp -= dmg
        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False
            self.death_time = time.time()



    def shoot(self):
        if not self.is_alive or not self.can_shoot():
            return None
        # Возвращаем координаты выстрела, чтобы сервер создал пулю

        spawn_x = self.x + cos(radians(self.direction)) * self.barrel_length
        spawn_y = self.y + sin(radians(self.direction)) * self.barrel_length

        self.next_shot_time = time.time() + self.fire_rate

        return (spawn_x, spawn_y, self.direction, self, self.damage)

    def rotate_turret(self, angle: float):
        if not self.is_alive:
            return
        
        if angle == 'CW':
            self.direction += self.rotation_speed
        elif angle == 'CCW':
            self.direction -= self.rotation_speed

    def serialize(self):
        # для отправки клиенту
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "direction": self.direction,
            "size": self.size,
            "hp": self.hp,
            "alive": self.is_alive,
            "name": self.name,
            "barrel_length": self.barrel_length
        }
    

class Bullet:
    _id_counter = 1

    def __init__(self, x: int, y: int, direction: int, onwner: Tank, damage=10):
        self.id = Bullet._id_counter
        Bullet._id_counter += 1

        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 15
        self.damage = damage
        self.owner = Tank

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
    