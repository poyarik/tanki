from game import Session
from models import Tank
from network import ServerNetwork
import time
from maps import load_map

move_commands = ['up', 'down', 'left', 'right', 'shoot']

map = load_map("maps/dust3.txt")

session = Session(map)

server = ServerNetwork(session=session)
server.start()


while True:
    #start = time.time()
    while not server.message_queue.empty():
        conn, message = server.message_queue.get()

        if message["type"] == "input":
            try:
                server.clients[conn]["input_state"] = message["state"]
            except KeyError:
                pass

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
    #end = time.time()

    #print(f"Server tick time: {(end-start)*1000:.2f} ms")
    time.sleep(1/session.tick_rate)