import json

def encode(mes):
    return (json.dumps(mes) + '\n').encode()

def decode(mes):
    return json.loads(mes.decode())