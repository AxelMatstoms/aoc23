import math


def f_inv(max_time, dist, branch=-1):
    return max_time / 2 + branch * ((-dist + max_time * max_time / 4) ** 0.5)


def solve_p1(path):
    with open(path) as f:
        itr = iter(f)
        time_line = next(itr)
        dist_line = next(itr)

    times = [int(t) for t in time_line.split(":")[1].strip().split()]
    dists = [int(d) for d in dist_line.split(":")[1].strip().split()]

    ans = 1
    eps = 0.00001
    for time, dist in zip(times, dists):
        lo = f_inv(time, dist, branch=-1)
        hi = f_inv(time, dist, branch=1)
        ans *= math.floor(hi - eps) - math.ceil(lo + eps) + 1

    return ans


def solve_p2(path):
    with open(path) as f:
        itr = iter(f)
        time_line = next(itr)
        dist_line = next(itr)

    time = int("".join(time_line.split(":")[1].strip().split()))
    dist = int("".join(dist_line.split(":")[1].strip().split()))

    ans = 1
    eps = 0.00001
    lo = f_inv(time, dist, branch=-1)
    hi = f_inv(time, dist, branch=1)
    ans *= math.floor(hi - eps) - math.ceil(lo + eps) + 1

    return ans


def main():
    assert solve_p1("example") == 288
    print(solve_p1("input"))

    assert solve_p2("example") == 71503
    print(solve_p2("input"))


if __name__ == "__main__":
    main()
