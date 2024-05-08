def solve_p1(path):
    DIRECTIONS = {"U": (0, -1), "D": (0, 1), "R": (1, 0), "L": (-1, 0)}

    x, y = 0, 0
    boundary = 0
    inner = 0
    with open(path) as f:
        for line in f:
            # Ignore color for part 1
            direction, count, _ = line.split()
            count = int(count)

            # Update boundary area, excluding current tile
            boundary += count

            # Update inner area with shoelace formula
            dx, dy = DIRECTIONS[direction]
            x1, y1 = x + dx * count, y + dy * count
            inner += x * y1 - x1 * y
            x, y = x1, y1

    # Pick's theorem
    return abs(inner) // 2 + boundary // 2 + 1


def solve_p2(path):
    DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    x, y = 0, 0
    boundary = 0
    inner = 0
    with open(path) as f:
        for line in f:
            color = line.split()[2].strip("#()")

            # Parse "color" to get count, direction
            count = int(color[:-1], 16)
            direction = int(color[-1])

            # Update boundary area, excluding current tile
            boundary += count

            # Update inner area with shoelace formula
            dx, dy = DIRECTIONS[direction]
            x1, y1 = x + dx * count, y + dy * count
            inner += x * y1 - x1 * y
            x, y = x1, y1

    # Pick's theorem
    return abs(inner) // 2 + boundary // 2 + 1


def main():
    assert solve_p1("example2") == 4
    assert solve_p1("example") == 62
    print(solve_p1("input"))

    assert solve_p2("example") == 952408144115
    print(solve_p2("input"))


if __name__ == "__main__":
    main()
