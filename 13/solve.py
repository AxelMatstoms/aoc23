def reflect(point, reflect):
    return 2 * reflect - point - 1


def is_reflected(grid, r, axis=0):
    h = len(grid)
    w = len(grid[0])
    wh = (w, h)

    # update loop range
    from_ = [0, 0]
    to = [w, h]

    from_[axis] = max(0, reflect(wh[axis] - 1, r))
    to[axis] = min(wh[axis], reflect(0, r))
    # to[axis] = r

    for y in range(from_[1], to[1]):
        for x in range(from_[0], to[0]):
            xy = (x, y)
            reflected = reflect(xy[axis], r)
            rx, ry = tuple(reflected if axis == i else xy[i] for i in range(2))

            if rx < 0 or ry < 0:
                # should not happen
                continue

            if grid[y][x] != grid[ry][rx]:
                return False

    return True


def is_reflected_smudged(grid, r, axis=0):
    h = len(grid)
    w = len(grid[0])
    wh = (w, h)

    # update loop range
    from_ = [0, 0]
    to = [w, h]

    from_[axis] = max(0, reflect(wh[axis] - 1, r))
    # to[axis] = min(wh[axis], reflect(0, r))
    to[axis] = r

    one_wrong = False

    for y in range(from_[1], to[1]):
        for x in range(from_[0], to[0]):
            xy = (x, y)
            reflected = reflect(xy[axis], r)
            rx, ry = tuple(reflected if axis == i else xy[i] for i in range(2))

            if rx < 0 or ry < 0:
                # should not happen
                continue

            if grid[y][x] != grid[ry][rx]:
                if one_wrong:
                    return False
                one_wrong = True

    return one_wrong


def read_grids(itr):
    grid = []
    for row in itr:
        row = row.strip()

        if not row:
            yield grid
            grid = []
        else:
            grid.append(row.strip())

    yield grid


def solve_p1(path):
    with open(path) as f:
        grids = list(read_grids(iter(f)))

    ans = 0

    for grid in grids:
        h = len(grid)
        w = len(grid[0])

        assert all(len(row) == w for row in grid)

        for x in range(1, w):
            if is_reflected(grid, x, axis=0):
                ans += x

        for y in range(1, h):
            if is_reflected(grid, y, axis=1):
                ans += 100 * y

    return ans


def solve_p2(path):
    with open(path) as f:
        grids = list(read_grids(iter(f)))

    ans = 0

    for grid in grids:
        h = len(grid)
        w = len(grid[0])

        assert all(len(row) == w for row in grid)

        for x in range(1, w):
            if is_reflected_smudged(grid, x, axis=0):
                ans += x

        for y in range(1, h):
            if is_reflected_smudged(grid, y, axis=1):
                ans += 100 * y

    return ans


def main():
    assert reflect(4, 5) == 5
    assert reflect(3, 5) == 6
    assert reflect(2, 5) == 7
    assert reflect(1, 5) == 8

    assert solve_p1("example") == 405
    print(solve_p1("input"))

    test_grid = ["#.......", ".#......", "..#.....", "..#.....", ".#....#.", "#......."]

    assert is_reflected_smudged(test_grid, 3, axis=1)

    assert solve_p2("example") == 400
    assert solve_p2("example2") == 300
    print(solve_p2("input"))


if __name__ == "__main__":
    main()
