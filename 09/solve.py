from itertools import pairwise
from functools import reduce
import operator


def central_differences(seq):
    for left, right in pairwise(seq):
        yield right - left


def solve_p1(path):
    with open(path) as f:
        sequences = [[int(num) for num in line.strip().split()] for line in f]

    ans = 0
    for seq in sequences:
        differences = [seq]
        while any(diff for diff in differences[-1]):
            differences.append(list(central_differences(differences[-1])))

        ans += reduce(operator.add, (diffs[-1] for diffs in differences))

    return ans


def solve_p2(path):
    with open(path) as f:
        sequences = [[int(num) for num in line.strip().split()] for line in f]

    ans = 0
    for seq in sequences:
        differences = [seq]
        while any(diff for diff in differences[-1]):
            differences.append(list(central_differences(differences[-1])))

        ans += reduce(operator.add, (((-1) ** i) * diffs[0] for i, diffs in enumerate(differences)))

    return ans


def main():
    assert solve_p1("example") == 114
    print(solve_p1("input"))

    assert solve_p2("example") == 2
    print(solve_p2("input"))


if __name__ == "__main__":
    main()
