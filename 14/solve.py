from itertools import count
import time
from datetime import timedelta

NORTH = (0, -1)
EAST = (1, 0)
SOUTH = (0, 1)
WEST = (-1, 0)


def solve_p1(path):
    with open(path) as f:
        grid = [list(line.strip()) for line in f]

    return tilt(grid, NORTH)


def iter_helper(wh, direction, dim):
    rev = direction[dim] > 0
    size = wh[dim]

    if rev:
        yield from reversed(range(size))
    else:
        yield from range(size)


def outer_iter(wh, direction):
    dim = 0 if direction[1] else 1
    yield from iter_helper(wh, direction, dim)


def inner_iter(wh, direction):
    dim = 0 if direction[0] else 1
    yield from iter_helper(wh, direction, dim)


def tilt(grid, direction):
    wh = len(grid[0]), len(grid)

    tilt_dim = 0 if direction[0] else 1
    iter_dim = 1 if direction[0] else 0

    rev = direction[tilt_dim] > 0

    flip_dims = bool(direction[0])

    dx, dy = (-direction[0], -direction[1])

    total_load = 0

    for c0 in outer_iter(wh, direction):
        last_free = [0, 0]
        last_free[iter_dim] = c0
        if rev:
            last_free[tilt_dim] = wh[tilt_dim] - 1

        free_x, free_y = last_free

        for c1 in inner_iter(wh, direction):
            x, y = (c1, c0) if flip_dims else (c0, c1)
            ch = grid[y][x]

            if ch == "#":
                free_x, free_y = (x + dx, y + dy)
            elif ch == "O":
                grid[y][x] = "."
                grid[free_y][free_x] = "O"
                total_load += wh[1] - free_y
                free_x += dx
                free_y += dy

    return total_load


def spin(grid):
    tilt(grid, NORTH)
    tilt(grid, WEST)
    tilt(grid, SOUTH)
    total_load = tilt(grid, EAST)

    return total_load, hash(tuple("".join(row) for row in grid))


def spin_cycle(grid):
    grid_copy = [row[:] for row in grid]
    for _ in count():
        yield spin(grid_copy)


def detect_cycle(grid):
    tortoise_itr = spin_cycle(grid)
    hare_itr = spin_cycle(grid)

    next(tortoise_itr)
    tortoise = next(tortoise_itr)  # tortoise starts at index 1
    next(hare_itr)
    next(hare_itr)
    hare = next(hare_itr)  # hare starts at index 2

    while tortoise != hare:
        tortoise = next(tortoise_itr)
        next(hare_itr)
        hare = next(hare_itr)

    mu = 0
    tortoise_itr = spin_cycle(grid)
    tortoise = next(tortoise_itr)  # tortoise goes back to 0

    while tortoise != hare:
        tortoise = next(tortoise_itr)
        hare = next(hare_itr)
        mu += 1

    # tortoise now at start of cycle
    lam = 1

    hare_itr = tortoise_itr
    hare = next(hare_itr)
    while tortoise != hare:
        hare = next(hare_itr)
        lam += 1

    return mu, lam


def load_at_cycle(grid, mu, lam, cycle):
    assert mu < cycle
    itr = spin_cycle(grid)

    for _ in range(mu - 1):
        next(itr)

    cycle_idx = (cycle - mu) % lam
    for _ in range(cycle_idx):
        next(itr)

    load, _ = next(itr)
    return load


def solve_p2(path):
    with open(path) as f:
        grid = [list(line.strip()) for line in f]

    mu, lam = detect_cycle(grid)
    return load_at_cycle(grid, mu, lam, 1000000000)


def main():
    assert solve_p1("example") == 136
    print(solve_p1("input"))

    assert solve_p2("example") == 64
    print(solve_p2("input"))


if __name__ == "__main__":
    main()
