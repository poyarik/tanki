from models import Bullet, Tank

class Session:
    def __init__(self):
        self.tanks = {}
        self.bullets = {}

        self.tick_rate = 30
        self.size_x = 800
        self.size_y = 600

    def add_tank(self, x: int, y: int, direction: int, name: str):
        tank = Tank(x, y, direction, name)
        self.tanks[tank.id] = tank

        return tank.id

    def remove_tank(self, tank_id: int):
        if tank_id in self.tanks:
            del self.tanks[tank_id]

    def add_bullet(self, x: int, y: int, direction: int):
        bullet = Bullet(x, y, direction)
        self.bullets[bullet.id] = bullet

        return bullet.id

    def remove_bullet(self, bullet_id: int):
        if bullet_id in self.bullets:
            del self.bullets[bullet_id]

    def check_collision(self, bullet, tank):
        # простая проверка "попадания"
        if abs(bullet.x - tank.x) < tank.size and abs(bullet.y - tank.y) < tank.size:
            return True
        return False

    def serialize(self):
        return {
            "tanks": [tank.serialize() for tank in self.tanks.values()],
            "bullets": [bullet.serialize() for bullet in self.bullets.values()],
        }

    def update(self):
        for bullet in self.bullets.values():
            bullet.move()
            if bullet.x < 0 or bullet.x > self.size_x or bullet.y < 0 or bullet.y > self.size_y:
                self.remove_bullet(bullet)

            for tank in self.tanks.values():
                if self.check_collision(bullet, tank):
                    tank.take_damage(bullet.damage)
                    self.remove_bullet(bullet)
                    break
