from game import Session
from models import Tank
from network import ServerNetwork
import time

move_commands = ['up', 'down', 'left', 'right', 'shoot']

session = Session()

server = ServerNetwork(session=session)
server.start()


while True:
    while not server.message_queue.empty():
        conn, message = server.message_queue.get()
        print("Сообщение от", server.clients[conn], ":", message)

        if message.get("cmd") in move_commands:
            tank_id = server.clients[conn]["tank"]
            if tank_id is not None:
                tank = session.tanks.get(tank_id)
                if tank:
                    if message["cmd"] == "up":
                        tank.move(0, -1)
                    elif message["cmd"] == "down":
                        tank.move(0, 1)
                    elif message["cmd"] == "left":
                        tank.move(-1, 0)
                    elif message["cmd"] == "right":
                        tank.move(1, 0)
                    elif message["cmd"] == "shoot":
                        session.add_bullet(*tank.shoot())

    session.update()
    state = session.serialize()
    print(state)
    time.sleep(1)