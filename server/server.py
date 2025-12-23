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

        if message["type"] == "input":
            server.clients[conn]["input_state"] = message["state"]

        elif message["type"] == "shoot":
            tank_id = server.clients[conn]["tank"]
            tank = session.tanks.get(tank_id)
            if tank:
                bullet = tank.shoot()
                if bullet:
                    session.add_bullet(*bullet)

    session.update(server.clients)
    state = session.serialize()
    server.broadcast({"type": "state", "data": state})
    time.sleep(1/session.tick_rate)