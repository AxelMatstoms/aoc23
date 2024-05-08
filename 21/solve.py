from math import ceil
from collections import deque
import heapq


def solve_p1(path, max_dist=64):
    D4_DELTA = ((-1, 0), (0, -1), (1, 0), (0, 1))

    with open(path) as f:
        grid = [line.strip() for line in f]

    w, h = len(grid[0]), len(grid)

    y, row = next(((y, row) for y, row in enumerate(grid) if "S" in row))
    x = row.find("S")

    to_explore = deque([(x, y)])
    dist = {(x, y): 0}

    while to_explore:
        x, y = to_explore.popleft()

        for dx, dy in D4_DELTA:
            cx, cy = x + dx, y + dy
            if cx < 0 or cy < 0 or cx >= w or cy >= h:
                continue

            if grid[cy][cx] == "#":
                continue

            new_dist = dist[(x, y)] + 1
            if new_dist > max_dist:
                continue

            if (cx, cy) not in dist:
                dist[(cx, cy)] = new_dist
                to_explore.append((cx, cy))

    return sum(1 for d in dist.values() if d % 2 == 0)


def bfs(grid, pos, max_dist=float("inf")):
    D4_DELTA = ((-1, 0), (0, -1), (1, 0), (0, 1))
    x0, y0 = pos
    w, h = len(grid[0]), len(grid)

    to_explore = deque([(x0, y0)])
    dist = {(x0, y0): 0}

    while to_explore:
        x, y = to_explore.popleft()

        for dx, dy in D4_DELTA:
            cx, cy = x + dx, y + dy
            if cx < 0 or cy < 0 or cx >= w or cy >= h:
                continue

            if grid[cy][cx] == "#":
                continue

            new_dist = dist[(x, y)] + 1
            if new_dist > max_dist:
                continue

            if (cx, cy) not in dist:
                dist[(cx, cy)] = new_dist
                to_explore.append((cx, cy))

    return dist


def bfs_many_starts(grid, to_explore, max_dist=float("inf")):
    D4_DELTA = ((-1, 0), (0, -1), (1, 0), (0, 1))
    w, h = len(grid[0]), len(grid)

    to_explore = list(to_explore)
    heapq.heapify(to_explore)
    dist = {pos: cost for cost, pos in to_explore}

    while to_explore:
        x, y = heapq.heappop(to_explore)

        for dx, dy in D4_DELTA:
            cx, cy = x + dx, y + dy
            if cx < 0 or cy < 0 or cx >= w or cy >= h:
                continue

            if grid[cy][cx] == "#":
                continue

            new_dist = dist[(x, y)] + 1
            if new_dist > max_dist:
                continue

            if (cx, cy) not in dist:
                dist[(cx, cy)] = new_dist
                heapq.heappush((cx, cy))

    return dist


def reachable(grid, pos, exact_dist):
    dist = bfs(grid, pos, max_dist=exact_dist)
    parity = exact_dist % 2
    return sum(1 for d in dist.values() if d % 2 == parity)


def max_dist(grid, pos):
    dist = bfs(grid, pos)
    return max(dist.values())


def dist_to(grid, orig, dest):
    dist = bfs(grid, orig)
    return dist[dest]


def extra_distance_along_axis(grid, pos, axis):
    x0, y0 = pos
    w, h = len(grid[0]), len(grid)

    if axis == (1, 0):  # East
        start = (0, y0)
        end = (w - 1, y0)
        manhattan = w - 1
    elif axis == (0, 1):  # South
        start = (x0, 0)
        end = (x0, h - 1)
        manhattan = h - 1
    elif axis == (-1, 0):  # West
        start = (w - 1, y0)
        end = (0, y0)
        manhattan = w - 1
    elif axis == (0, -1):  # North
        start = (x0, h - 1)
        end = (x0, 0)
        manhattan = h - 1

    dist = dist_to(grid, start, end)
    penalty = dist - manhattan

    return penalty


def reachable_axis(grid, pos, axis, exact_dist):
    D4_DELTA = ((-1, 0), (0, -1), (1, 0), (0, 1))
    WEST, NORTH, EAST, SOUTH = D4_DELTA

    x0, y0 = pos
    w, h = len(grid[0]), len(grid)

    axis_dim_idx = 0 if axis[0] else 1

    axis_size = (w, h)[axis_dim_idx]
    # Assume it looks like input :)

    if axis == WEST:
        dist_origin = x0
        search_pos = (w - 1, y0)
    elif axis == NORTH:
        dist_origin = y0
        search_pos = (x0, h - 1)
    elif axis == EAST:
        dist_origin = w - x0 - 1
        search_pos = (0, y0)
    elif axis == SOUTH:
        dist_origin = h - y0 - 1
        search_pos = (x0, 0)

    remaining = exact_dist - dist_origin

    remaining_grids = ceil(remaining / axis_size)
    dist_outer = dist_origin + remaining_grids * axis_size + 1
    dist_inner = dist_origin + (remaining_grids - 1) * axis_size + 1

    dist = bfs(grid, search_pos)

    outer_reachable = sum(1



def solve_p2(path, exact_dist=64):
    D4_DELTA = ((-1, 0), (0, -1), (1, 0), (0, 1))

    with open(path) as f:
        grid = [line.strip() for line in f]

    y0, row = next(((y, row) for y, row in enumerate(grid) if "S" in row))
    x0 = row.find("S")
    w, h = len(grid[0]), len(grid)

    if (
        exact_dist <= y0 + 1
        and exact_dist <= x0 + 1
        and exact_dist <= (w - x0)
        and exact_dist <= (h - y0)
    ):
        return reachable(grid, (x0, y0), exact_dist)

    dist = bfs(grid, (x0, y0))
    nw_dist = dist[(0, 0)]
    ne_dist = dist[(w - 1, 0)]
    sw_dist = dist[(0, h - 1)]
    se_dist = dist[(w - 1, h - 1)]

    origin_parity = (x0 + y0) % 2
    full_even = sum(
        (x + y) % 2 == 0 and tile != "#"
        for y, row in enumerate(grid)
        for x, tile in enumerate(row)
    )

    full_odd = sum(
        (x + y) % 2 == 1 and tile != "#"
        for y, row in enumerate(grid)
        for x, tile in enumerate(row)
    )

    print(f"{full_even=} {full_odd=}")
    max_dist_origin = max_dist(grid, (x0, y0))


def main():
    assert solve_p1("example", max_dist=6) == 16
    print(solve_p1("input"))

    assert solve_p2("example", exact_dist=6) == 16
    assert solve_p2("example", exact_dist=10) == 50
    assert solve_p2("example", exact_dist=6) == 16
    assert solve_p2("example", exact_dist=6) == 16
    print(solve_p2("input"))


if __name__ == "__main__":
    main()
