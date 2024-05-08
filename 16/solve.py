from collections import deque
from itertools import chain


def tiles_energized(grid, beam_pos, beam_dir):
    def in_bounds(pos):
        x, y = pos
        return x >= 0 and y >= 0 and x < len(grid[0]) and y < len(grid)

    # ((x, y), (vx, vy))
    explored = {(beam_pos, beam_dir)}
    energized = {beam_pos}
    queue = deque([(beam_pos, beam_dir)])

    while queue:
        (x, y), (vx, vy) = queue.popleft()

        tile = grid[y][x]
        neighbours = []

        if tile == ".":
            neighbours.append(((x + vx, y + vy), (vx, vy)))
        elif tile == "/":
            new_vx, new_vy = (-vy, -vx)
            neighbours.append(((x + new_vx, y + new_vy), (new_vx, new_vy)))
        elif tile == "\\":
            new_vx, new_vy = (vy, vx)
            neighbours.append(((x + new_vx, y + new_vy), (new_vx, new_vy)))
        elif tile == "|":
            if vy:
                neighbours.append(((x + vx, y + vy), (vx, vy)))
            else:
                neighbours.append(((x, y - 1), (0, -1)))
                neighbours.append(((x, y + 1), (0, 1)))
        elif tile == "-":
            if vx:
                neighbours.append(((x + vx, y + vy), (vx, vy)))
            else:
                neighbours.append(((x - 1, y), (-1, 0)))
                neighbours.append(((x + 1, y), (1, 0)))

        for pos, vel in neighbours:
            if not in_bounds(pos) or (pos, vel) in explored:
                continue

            energized.add(pos)
            explored.add((pos, vel))
            queue.append((pos, vel))

    return len(energized)


def solve_p1(path):
    with open(path) as f:
        grid = [line.strip() for line in f]

    return tiles_energized(grid, (0, 0), (1, 0))


def solve_p2(path):
    with open(path) as f:
        grid = [line.strip() for line in f]

    w, h = (len(grid[0]), len(grid))

    north_edge = (((x, 0), (0, 1)) for x in range(w))
    east_edge = (((w - 1, y), (-1, 0)) for y in range(h))
    south_edge = (((x, h - 1), (0, -1)) for x in range(w))
    west_edge = (((0, y), (1, 0)) for y in range(h))

    return max(
        tiles_energized(grid, *beam)
        for beam in chain(north_edge, east_edge, south_edge, west_edge)
    )


def main():
    assert solve_p1("example") == 46
    print(solve_p1("input"))

    assert solve_p2("example") == 51
    print(solve_p2("input"))


if __name__ == "__main__":
    main()
