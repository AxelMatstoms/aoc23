def next_numeric(line, index=0):
    for i, ch in enumerate(line[index:], start=index):
        if ch.isnumeric():
            return i

    raise IndexError("No numeric character found")


def next_nonnumeric(line, index=0):
    for i, ch in enumerate(line[index:], start=index):
        if not ch.isnumeric():
            return i

    raise IndexError("No numeric character found")


def find_all_numbers(line):
    numbers = []
    idx = 0
    while idx < len(line):
        try:
            start = next_numeric(line, index=idx)
        except IndexError:
            break

        try:
            end = next_nonnumeric(line, index=start)
        except IndexError:
            end = len(line)

        idx = end
        number = int(line[start:end])
        numbers.append((start, number))

    return numbers


def find_symbol_adjacent(line, y):
    D8_DELTA = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for x, ch in enumerate(line):
        if ch != "." and not ch.isnumeric():
            yield from ((x + dx, y + dy) for dx, dy in D8_DELTA)


def solve_p1(path):
    with open(path) as f:
        grid = [line.strip() for line in f]

    numbers = []
    symbol_adjacent = set()
    for y, line in enumerate(grid):
        symbol_adjacent |= set(find_symbol_adjacent(line, y))

        for x, num in find_all_numbers(line):
            numbers.append((x, y, num))

    part_numbers = [
        num
        for x0, y, num in numbers
        if any((x0 + dx, y) in symbol_adjacent for dx in range(len(str(num))))
    ]

    return sum(part_numbers)


def solve_p2(path):
    with open(path) as f:
        grid = [line.strip() for line in f]

    numbers = []
    potential_gears = []
    for y, line in enumerate(grid):
        for x, num in find_all_numbers(line):
            numbers.append((x, y, num))
        potential_gears.extend((x, y) for x, ch in enumerate(line) if ch == "*")

    num_map = {}
    for x0, y, num in numbers:
        for dx in range(len(str(num))):
            num_map[(x0 + dx, y)] = num

    total_gear_ratio = 0
    D8_DELTA = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for gx, gy in potential_gears:
        neighbors = set(
            num_map[(gx + dx, gy + dy)]
            for dx, dy in D8_DELTA
            if (gx + dx, gy + dy) in num_map
        )

        if len(neighbors) == 2:
            a, b = neighbors
            total_gear_ratio += a * b

    return total_gear_ratio


def main():
    assert next_numeric("abc123") == 3
    assert next_nonnumeric("012abc") == 3
    assert next_numeric("012abc345", index=3) == 6
    assert next_nonnumeric("abc012def", index=3) == 6

    assert find_all_numbers("123*456....*789") == [(0, 123), (4, 456), (12, 789)]

    assert solve_p1("example") == 4361
    print(solve_p1("input"))

    assert solve_p2("example") == 467835
    print(solve_p2("input"))


if __name__ == "__main__":
    main()
