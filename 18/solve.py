from itertools import product, groupby


def solve_p1(path):
    DIRECTIONS = {"U": (0, -1), "D": (0, 1), "R": (1, 0), "L": (-1, 0)}

    dig_plan = []
    with open(path) as f:
        for line in f:
            direction, count, color = line.split()
            count = int(count)
            color = color.strip("()")
            dig_plan.append((direction, count, color))

    x, y = 0, 0

    edge = {(0, 0)}
    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0

    for direction, count, _ in dig_plan:
        dx, dy = DIRECTIONS[direction]
        next_x = x + dx * count
        next_y = y + dy * count

        x_step = dx if dx else 1
        y_step = dy if dy else 1
        x_coords = range(x + dx, next_x + x_step, x_step)
        y_coords = range(y + dy, next_y + y_step, y_step)
        edge.update(product(x_coords, y_coords))

        x, y = next_x, next_y
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)

    def in_bounds(p):
        x, y = p
        return x >= min_x and x <= max_x and y >= min_y and y <= max_y

    def almost_in_bounds(p):
        x, y = p
        return x >= min_x - 1 and x <= max_x + 1 and y >= min_y - 1 and y <= max_y + 1

    assert in_bounds((min_x, min_y))
    assert in_bounds((max_x, max_y))
    assert not in_bounds((min_x - 1, min_y))
    assert not in_bounds((min_x, min_y - 1))
    assert not in_bounds((max_x + 1, max_y))
    assert not in_bounds((max_x, max_y + 1))

    seed = (min_x - 1, min_y - 1)
    visited = {seed}
    outside = set()

    to_visit = [seed]
    while to_visit:
        p = to_visit.pop()

        for dx, dy in DIRECTIONS.values():
            p1 = (p[0] + dx, p[1] + dy)
            if p1 in edge:
                continue

            if not almost_in_bounds(p1):
                continue

            if in_bounds(p1):
                outside.add(p1)

            if p1 not in visited:
                visited.add(p1)
                to_visit.append(p1)

    w = max_x - min_x + 1
    h = max_y - min_y + 1

    return w * h - len(outside)


def by_rect(corners):
    prev = None

    for corner in corners:
        if prev is None:
            prev = corner
            continue

        rect = (prev, corner)
        prev = None
        yield rect


def solve_p2(path):
    DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    x, y = 0, 0
    corners = []
    with open(path) as f:
        for line in f:
            _, _, color = line.split()
            color = color.strip("#()")
            direction = int(color[-1])
            count = int(color[:-1], 16)

            dx, dy = DIRECTIONS[direction]
            x += dx * count
            y += dy * count
            corners.append((x, y))

    corners.sort(key=lambda xy: (xy[1], xy[0]))
    corners_by_row = [
        (y, [x for x, _ in itr]) for y, itr in groupby(corners, lambda xy: xy[1])
    ]

    rect_y = corners_by_row[0][0]
    rects = list(by_rect(corners_by_row[0][1]))
    area = 0

    for y, row_corners in corners_by_row[1:]:
        h = y - rect_y  # don't count current row
        rect_y = y

        # fixed cyclomatic complexity by making the code more complex
        area += h * sum(r - l + 1 for l, r in rects)

        rect_idx = 0
        for l, r in by_rect(row_corners):
            for i, rect in enumerate(rects[rect_idx:], rect_idx):
                if r < rect[0]:
                    rects.insert(i, (l, r))
                    rect_idx = i
                    break
                if l == rect[0] and r == rect[1]:
                    area += r - l + 1
                    del rects[i]
                    rect_idx = i
                    break
                elif l == rect[0]:
                    area += r - rect[0]
                    rects[i] = (r, rect[1])
                    rect_idx = i
                    break
                elif r == rect[0]:
                    rects[i] = (l, rect[1])
                    rect_idx = i
                    break
                elif l == rect[1]:
                    rects[i] = (rect[0], r)
                    rect_idx = i
                    break
                elif r == rect[1]:
                    area += rect[1] - l
                    rects[i] = (rect[0], l)
                    rect_idx = i
                    break
                elif l > rect[0] and l < rect[1] and r > rect[0] and r < rect[1]:
                    area += r - l - 1
                    rects[i] = (rect[0], l)
                    rects.insert(i + 1, (r, rect[1]))
                    rect_idx = i + 1
                    break
            else:
                rects.append((l, r))
                rect_idx = i + 2

        # join rectangles that are adjacent
        i = 0
        while i < len(rects) - 1:
            left = rects[i]
            right = rects[i + 1]
            if left[1] == right[0]:
                del rects[i + 1]
                rects[i] = (left[0], right[1])
            else:
                i += 1

    return area


def main():
    assert solve_p1("example") == 62
    print(solve_p1("input"))

    assert solve_p2("example") == 952408144115
    print(solve_p2("input"))


if __name__ == "__main__":
    main()
