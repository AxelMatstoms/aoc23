from itertools import accumulate, combinations


def get_offset(coords, expansion=1):
    size = max(coords) + 1
    empty_coords = set(range(size)) - coords

    expansions = (expansion if c in empty_coords else 0 for c in range(size))
    offset = accumulate(expansions)

    return list(offset)


def solve_p1(path):
    galaxies = []
    with open(path) as f:
        for y, line in enumerate(f):
            galaxies.extend((x, y) for x, ch in enumerate(line.strip()) if ch == "#")

    x_coords = set(xy[0] for xy in galaxies)
    y_coords = set(xy[1] for xy in galaxies)

    offset_x = get_offset(x_coords)
    offset_y = get_offset(y_coords)

    galaxies_shifted = [(x + offset_x[x], y + offset_y[y]) for x, y in galaxies]

    total_dist = 0
    for (x0, y0), (x1, y1) in combinations(galaxies_shifted, 2):
        dist = abs(x1 - x0) + abs(y1 - y0)
        total_dist += dist

    return total_dist


def solve_p2(path, expansion=1000000):
    galaxies = []
    with open(path) as f:
        for y, line in enumerate(f):
            galaxies.extend((x, y) for x, ch in enumerate(line.strip()) if ch == "#")

    x_coords = set(xy[0] for xy in galaxies)
    y_coords = set(xy[1] for xy in galaxies)

    offset_x = get_offset(x_coords, expansion=expansion-1)
    offset_y = get_offset(y_coords, expansion=expansion-1)

    galaxies_shifted = [(x + offset_x[x], y + offset_y[y]) for x, y in galaxies]

    total_dist = 0
    for (x0, y0), (x1, y1) in combinations(galaxies_shifted, 2):
        dist = abs(x1 - x0) + abs(y1 - y0)
        total_dist += dist

    return total_dist


def main():
    assert solve_p1("example") == 374
    print(solve_p1("input"))

    assert solve_p2("example", expansion=10) == 1030
    assert solve_p2("example", expansion=100) == 8410
    print(solve_p2("input"))


if __name__ == "__main__":
    main()
