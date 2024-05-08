# import queue
import heapq

# from dataclasses import dataclass, field


# @dataclass(init=False, order=True)
# class Node:
#     pos: tuple[int, int] = field(compare=False)
#     facing: tuple[int, int] = field(compare=False)
#     path_cost: int = field(compare=False)
#     # parent: "Node" = field(compare=False, repr=False)
#
#     estimated_cost: int
#     straight: int
#
#     # def __init__(self, pos, facing, path_cost, parent, heuristic, straight):
#     def __init__(self, pos, facing, path_cost, heuristic, straight):
#         self.pos = pos
#         self.facing = facing
#         self.path_cost = path_cost
#         # self.parent = parent
#
#         self.estimated_cost = path_cost + heuristic
#         self.straight = straight


# def manhattan(from_, to):
#    return sum(abs(t - f) for f, t in zip(from_, to))
#
#
# def in_bounds(dim, pos):
#    return all(c >= 0 for c in pos) and all(c < d for c, d in zip(pos, dim))


_heuristics = {}


def init_heuristic(grid, name):
    if name in _heuristics:
        return _heuristics[name]  # Dynamic programming :D

    DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    w, h = len(grid[0]), len(grid)
    goal = (w - 1, h - 1)

    costs = [[float("inf") for _ in row] for row in grid]
    costs[h - 1][w - 1] = 0

    # to_visit = queue.PriorityQueue()
    # to_visit.put((0, goal))
    to_visit = [(0, goal)]

    while to_visit:  # not .empty()
        # cost, pos = to_visit.get()
        cost, pos = heapq.heappop(to_visit)

        for delta in DIRECTIONS:
            new_pos = (pos[0] + delta[0], pos[1] + delta[1])
            x, y = new_pos

            # if not in_bounds((w, h), new_pos):
            if x < 0 or y < 0 or x >= w or y >= w:
                continue

            new_cost = cost + grid[pos[1]][pos[0]]

            if new_cost < costs[y][x]:
                costs[y][x] = new_cost
                # to_visit.put((new_cost, new_pos))
                heapq.heappush(to_visit, (new_cost, new_pos))

    _heuristics[name] = costs

    return costs


def solve_p1(path):
    with open(path) as f:
        grid = [[int(cost) for cost in line.strip()] for line in f]

    DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    w, h = len(grid[0]), len(grid)
    goal = (w - 1, h - 1)
    heuristic = init_heuristic(grid, path)

    # ((x, y), (dx, dy), consecutive_in_direction)

    start = ((0, 0), (-1, -1), 0)
    # start_node = Node((0, 0), (-1, -1), 0, heuristic[0][0], 0)
    # start_node = Node((0, 0), (-1, -1), 0, 0, 0)

    # (estimated_remaining, straight, pos, dir, path_cost)
    start_node = (heuristic[0][0], 0, (0, 0), (-1, -1), 0)

    # frontier = queue.PriorityQueue()
    frontier = [start_node]
    # frontier.put(start_node)
    reached = {start: start_node}

    # while not frontier.empty():
    while frontier:
        # node = frontier.get()
        _, node_straight, node_pos, node_dir, node_path_cost = heapq.heappop(frontier)

        if node_pos == goal:
            return node_path_cost

        for facing in DIRECTIONS:
            straight = 1
            if facing == node_dir:
                straight += node_straight

            if straight > 3:
                continue  # Crucibles can't go straight for very far

            # disallow reversing
            if facing == (-node_dir[0], -node_dir[1]):
                continue

            # pos = (node_pos[0] + facing[0], node.pos[1] + facing[1])
            # x, y = pos
            x = node_pos[0] + facing[0]
            y = node_pos[1] + facing[1]
            pos = (x, y)

            # if not in_bounds((w, h), pos):
            if x < 0 or y < 0 or x >= w or y >= h:
                continue

            path_cost = node_path_cost + grid[y][x]
            state = (pos, facing, straight)
            if state not in reached or path_cost < reached[state][4]:
                # child = Node(pos, facing, path_cost, heuristic[y][x], straight)
                # child = Node(pos, facing, path_cost, 0, straight)
                child = (path_cost + heuristic[y][x], straight, pos, facing, path_cost)
                #        + heuristic

                reached[state] = child
                # frontier.put(child)
                heapq.heappush(frontier, child)

    raise ValueError("Could not reach goal node")


def solve_p2(path):
    with open(path) as f:
        grid = [[int(cost) for cost in line.strip()] for line in f]

    DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    w, h = len(grid[0]), len(grid)
    goal = (w - 1, h - 1)
    heuristic = init_heuristic(grid, path)

    # ((x, y), (dx, dy), consecutive_in_direction)

    start_down = ((0, 0), (0, 1), 0)
    start_right = ((0, 0), (1, 0), 0)
    # start_node_down = Node((0, 0), (0, 1), 0, heuristic[0][0], 0)
    # start_node_right = Node((0, 0), (1, 0), 0, heuristic[0][0], 0)
    # start_node_down = Node((0, 0), (0, 1), 0, 0, 0)
    # start_node_right = Node((0, 0), (1, 0), 0, 0, 0)
    # (estimated_remaining, straight, pos, dir, path_cost)
    start_node_down = (heuristic[0][0], 0, (0, 0), (0, 1), 0)
    start_node_right = (heuristic[0][0], 0, (0, 0), (1, 0), 0)

    # frontier = queue.PriorityQueue()
    # frontier.put(start_node_down)
    # frontier.put(start_node_right)
    frontier = [start_node_down, start_node_right]

    reached = {start_down: start_node_down, start_right: start_node_right}

    # while not frontier.empty():
    while frontier:
        # node = frontier.get()
        # node = heapq.heappop(frontier)
        _, node_straight, node_pos, node_dir, node_path_cost = heapq.heappop(frontier)

        if node_pos == goal:
            return node_path_cost

        for facing in DIRECTIONS:
            straight = 1
            if facing == node_dir:
                straight += node_straight

            if straight > 10:
                continue  # Ultra crucibles can go straight for at most 10 tiles

            if node_straight < 4 and facing != node_dir:
                continue  # Ultra crucibles can't turn before they've travelled straight for 4 tiles

            # disallow reversing
            if facing == (-node_dir[0], -node_dir[1]):
                continue

            # pos = (node_pos[0] + facing[0], node_pos[1] + facing[1])
            x = node_pos[0] + facing[0]
            y = node_pos[1] + facing[1]
            # x, y = pos
            pos = (x, y)

            # if not in_bounds((w, h), pos):
            if x < 0 or y < 0 or x >= w or y >= h:
                continue

            path_cost = node_path_cost + grid[y][x]
            state = (pos, facing, straight)
            if state not in reached or path_cost < reached[state][4]:
                # child = Node(pos, facing, path_cost, heuristic[y][x], straight)
                # child = Node(pos, facing, path_cost, 0, straight)
                child = (path_cost + heuristic[y][x], straight, pos, facing, path_cost)

                reached[state] = child
                # frontier.put(child)
                heapq.heappush(frontier, child)

    raise ValueError("Could not reach goal node")


def main():
    # assert solve_p1("example") == 102
    print(solve_p1("input"))

    # assert solve_p2("example") == 94
    print(solve_p2("input"))


if __name__ == "__main__":
    main()
