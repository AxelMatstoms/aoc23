def HASH(to_hash):
    ret = 0
    for ch in to_hash:
        ret += ord(ch)
        ret *= 17
        ret &= 0xFF

    return ret


def solve_p1(path):
    with open(path) as f:
        init_seq = f.read().strip()

    steps = init_seq.split(",")

    return sum(HASH(step) for step in steps)


def print_hashmap(hashmap):
    for i, box in enumerate(hashmap):
        if not box:
            continue

        contents = " ".join(f"[{label} {focal}]" for label, focal in box)
        print(f"Box {i}: {contents}")


def solve_p2(path):
    with open(path) as f:
        init_seq = f.read().strip()

    steps = init_seq.split(",")

    hashmap = [[] for _ in range(256)]

    for step in steps:
        sep = "=" if "=" in step else "-"
        label, op, focal = step.partition(sep)
        if focal:
            focal = int(focal)

        slot = HASH(label)
        box = hashmap[slot]

        try:
            idx = next(i for i, (l, _) in enumerate(box) if l == label)
            present = True
        except StopIteration:
            present = False

        if op == "-":
            if present:
                del box[idx]
        elif op == "=":
            if present:
                box[idx] = (label, focal)
            else:
                box.append((label, focal))

    focusing_power = 0
    for i, box in enumerate(hashmap):
        for k, (_, focal) in enumerate(box):
            focusing_power += (i + 1) * (k + 1) * focal

    return focusing_power


def main():
    assert solve_p1("example") == 1320
    print(solve_p1("input"))

    assert solve_p2("example") == 145
    print(solve_p2("input"))


if __name__ == "__main__":
    main()
