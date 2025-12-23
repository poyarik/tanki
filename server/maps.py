def load_map(filename):
    with open(filename, "r") as f:
        lines = [line.strip() for line in f.readlines()]
    grid = [list(line) for line in lines]
    return grid