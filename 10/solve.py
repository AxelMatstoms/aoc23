from collections import deque


NORTH = (0, -1)
EAST = (1, 0)
SOUTH = (0, 1)
WEST = (-1, 0)

CONNECTIONS = {
    "|": {NORTH, SOUTH},
    "-": {EAST, WEST},
    "L": {NORTH, EAST},
    "J": {NORTH, WEST},
    "7": {SOUTH, WEST},
    "F": {SOUTH, EAST},
    ".": set(),
    "S": {NORTH, EAST, SOUTH, WEST},
}

OPPOSITE = {"L": "J", "J": "L", "F": "7", "7": "F"}


def is_connected(grid, p0, p1):
    x0, y0 = p0
    x1, y1 = p1

    dx, dy = x1 - x0, y1 - y0

    return (dx, dy) in CONNECTIONS[grid[y0][x0]] and (-dx, -dy) in CONNECTIONS[
        grid[y1][x1]
    ]


def neighbours(grid, p0, exclude=None):
    if exclude is None:
        exclude = []

    for dx, dy in (NORTH, EAST, SOUTH, WEST):
        p1 = (p0[0] + dx, p0[1] + dy)
        if is_connected(grid, p0, p1) and p1 not in exclude:
            yield p1


def solve_p1(path):
    with open(path) as f:
        grid = [line.strip() for line in f]

    origin = None

    for y, row in enumerate(grid):
        x = row.find("S")
        if x != -1:
            origin = (x, y)

    if origin is None:
        raise ValueError("Grid doesn't contain start point")

    dist = {origin: 0}
    queue = deque([origin])

    while queue:
        p = queue.popleft()
        for n in neighbours(grid, p):
            old_dist = dist.get(n, float("inf"))
            new_dist = dist[p] + 1

            if new_dist < old_dist:
                queue.append(n)
                dist[n] = new_dist

    return max(dist.values())


def solve_p2(path):
    with open(path) as f:
        grid = [line.strip() for line in f]

    origin = None

    for y, row in enumerate(grid):
        x = row.find("S")
        if x != -1:
            origin = (x, y)

    if origin is None:
        raise ValueError("Grid doesn't contain start point")

    queue = deque([origin])
    loop = set()

    while queue:
        p = queue.popleft()
        for n in neighbours(grid, p):
            if n not in loop:
                queue.append(n)
                loop.add(n)

    loop_only = [["."] * len(row) for row in grid]
    for x, y in loop:
        loop_only[y][x] = grid[y][x]

    inside_count = 0

    for row in loop_only:
        inside = False
        edge = ""

        for ch in row:
            if ch == "|":
                inside = not inside
                continue

            if ch in "LJ7F":
                if edge:
                    if ch != OPPOSITE[edge]:
                        inside = not inside

                    edge = ""
                else:
                    edge = ch

                continue

            if inside and ch == ".":
                inside_count += 1

    return inside_count


def main():
    test_grid = ["F-7", "|.|", "L-J"]
    path = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2), (0, 1), (0, 0)]

    for cur, next_ in zip(path, path[1:]):
        assert is_connected(test_grid, cur, next_)
        assert is_connected(test_grid, next_, cur)
        assert not is_connected(test_grid, cur, (1, 1))

    assert solve_p1("example") == 4
    assert solve_p1("example2") == 4
    assert solve_p1("example3") == 8
    print(solve_p1("input"))

    assert solve_p2("example4") == 4
    assert solve_p2("example5") == 8
    assert solve_p2("example6") == 10
    print(solve_p2("input"))


if __name__ == "__main__":
    main()
