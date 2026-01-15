from time import time
from models import Bullet, Tank
import random

class Session:
    def __init__(self, map):
        self.tanks = {}
        self.bullets = {}
        self.map = map
        #self.gamemode = gamemode TODO
        self.tile_size = 40

        self.tick_rate = 30
        self.size_x = 1200
        self.size_y = 600
        self.respawn_time = 5  # секунд до респауна

        self.spawn_points = []
        for y, row in enumerate(map):
            for x, tile in enumerate(row):
                if tile == "S":
                    self.spawn_points.append((x*self.tile_size + self.tile_size/2,
                                              y*self.tile_size + self.tile_size/2))
                    
    def find_spawn_for_tank(self):
        # выбираем случайную свободную точку
        free_points = self.spawn_points.copy()
        
        # исключаем точки, занятые другими танками
        for tank in self.tanks.values():
            free_points = [p for p in free_points if (abs(p[0]-tank.x) > tank.size and abs(p[1]-tank.y) > tank.size)]

        if not free_points:
            # если все точки заняты — спавним в центре
            x, y = self.size_x / 2, self.size_y / 2
        else:
            x, y = random.choice(free_points)

        return x, y

    def add_tank(self, name: str, tank_type: str):
        x, y = self.find_spawn_for_tank()
        tank = Tank(x, y, 0, name, tank_type)
        self.tanks[tank.id] = tank

        return tank.id

    def remove_tank(self, tank_id: int):
        if tank_id in self.tanks:
            del self.tanks[tank_id]

    def add_bullet(self, *args):
        bullet = Bullet(*args)
        self.bullets[bullet.id] = bullet

        return bullet.id

    def remove_bullet(self, bullet_id: int):
        if bullet_id in self.bullets:
            del self.bullets[bullet_id]

    def check_collision(self, bullet, tank):
        # простая проверка "попадания"
        half = tank.size / 2

        if (
            abs(bullet.x - tank.x) <= half and
            abs(bullet.y - tank.y) <= half
        ):
            return True
        
        return False
    
    def is_passable(self, x, y, buffer=0):
        """
        Проверка, можно ли пройти в координату (x, y)
        buffer = половина размера танка, чтобы не оставалось щелей
        """
        tile_x = int(x // self.tile_size)
        tile_y = int(y // self.tile_size)

        if tile_y < 0 or tile_y >= len(self.map):
            return False
        if tile_x < 0 or tile_x >= len(self.map[0]):
            return False

        # проверяем все тайлы, которые может занимать танк с радиусом buffer
        left = int((x - buffer) // self.tile_size)
        right = int((x + buffer) // self.tile_size)
        top = int((y - buffer) // self.tile_size)
        bottom = int((y + buffer) // self.tile_size)

        for ty in range(top, bottom+1):
            for tx in range(left, right+1):
                if 0 <= ty < len(self.map) and 0 <= tx < len(self.map[0]):
                    if self.map[ty][tx] in ("#", "~"):
                        return False
                else:
                    return False  # за пределами карты тоже нельзя

        return True

    def serialize(self, clients):
        score = []
        for info in clients.values():
            score.append([info["name"], info["score"]])
            
        score.sort(key=lambda x: x[0])

        print(score)

        return {
            "tanks": [tank.serialize() for tank in self.tanks.values()],
            "bullets": [bullet.serialize() for bullet in self.bullets.values()],
            "score": score
        }

    def update(self, clients):
        to_remove = []
        for bullet in self.bullets.values():
            bullet.move()

            # проверка выхода за пределы карты
            if bullet.x < 0 or bullet.x > self.size_x or bullet.y < 0 or bullet.y > self.size_y:
                to_remove.append(bullet.id)
                continue

            # проверка столкновения со стеной
            tile_x = int(bullet.x // self.tile_size)
            tile_y = int(bullet.y // self.tile_size)
            if 0 <= tile_y < len(self.map) and 0 <= tile_x < len(self.map[0]):
                if self.map[tile_y][tile_x] == "#":
                    to_remove.append(bullet.id)
                    continue

            # проверка попадания в танки
            for tank in self.tanks.values():
                if self.check_collision(bullet, tank):
                    tank.take_damage(bullet.damage)
                    if not tank.is_alive:
                        shooting_tank = bullet.owner
                        for info in clients.values():
                            if info["tank"] == shooting_tank.id:
                                info["score"] += 1
                    to_remove.append(bullet.id)
                    break

        for bullet_id in to_remove:
            self.remove_bullet(bullet_id)

        for conn, info in clients.items():
            tank_id = info["tank"]
            tank = self.tanks.get(tank_id)
            if not tank:
                continue

            if not tank.is_alive:
                if time() - tank.death_time >= self.respawn_time:
                    x, y = self.find_spawn_for_tank()
                    if x and y:
                        tank.x = x
                        tank.y = y
                        tank.hp = tank.max_hp
                        tank.is_alive = True
                        tank.death_time = None
                continue

            state = info["input_state"]

            dx = int(state["right"]) - int(state["left"])
            dy = int(state["down"]) - int(state["up"])

            if dx != 0 or dy != 0:
                new_x = tank.x + dx * tank.speed
                new_y = tank.y + dy * tank.speed
                half = tank.size / 2

                if self.is_passable(new_x, new_y, buffer=half):
                    tank.x = new_x
                    tank.y = new_y
                else:
                    # проверяем только по X
                    if self.is_passable(new_x, tank.y, buffer=half):
                        tank.x = new_x
                    # проверяем только по Y
                    if self.is_passable(tank.x, new_y, buffer=half):
                        tank.y = new_y

            turret_dir = state["turret"]
            tank.rotate_turret(turret_dir)
