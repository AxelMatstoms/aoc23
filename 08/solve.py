from math import lcm
from itertools import cycle


def solve_p1(path):
    network = {}
    with open(path) as f:
        itr = iter(f)

        instructions = next(itr).strip()
        next(itr)

        for line in itr:
            node, split = line.strip().split(" = ")
            left, right = split.strip("()").split(", ")

            network[node] = (left, right)

    instructions = tuple({"L": 0, "R": 1}[instr] for instr in instructions)

    current = "AAA"
    steps = 0
    for instr in cycle(instructions):
        if current == "ZZZ":
            break

        current = network[current][instr]
        steps += 1

    return steps


def solve_p2(path):
    network = {}
    with open(path) as f:
        itr = iter(f)

        instructions = next(itr).strip()
        next(itr)

        for line in itr:
            node, split = line.strip().split(" = ")
            left, right = split.strip("()").split(", ")

            network[node] = (left, right)

    instructions = tuple({"L": 0, "R": 1}[instr] for instr in instructions)

    step_counts = []

    for node in (node for node in network if node.endswith("A")):
        current = node
        steps = 0
        for instr in cycle(instructions):
            if current.endswith("Z"):
                break

            current = network[current][instr]
            steps += 1

        step_counts.append(steps)

    return lcm(*step_counts)


def main():
    assert solve_p1("example") == 2
    assert solve_p1("example2") == 6
    print(solve_p1("input"))

    assert solve_p2("example3") == 6
    print(solve_p2("input"))


if __name__ == "__main__":
    main()
