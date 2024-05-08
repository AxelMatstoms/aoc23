import math
import functools


def verify_solution(record, groups):
    chunks = record.replace(".", " ").split()
    return len(chunks) == len(groups) and all(
        len(chunk) == group for chunk, group in zip(chunks, groups)
    )


def verify_prefix(pattern, groups):
    chunk = 0
    cur_group = -1
    for ch in pattern:
        group_size = 0 if cur_group >= len(groups) else groups[cur_group]

        if ch == ".":
            if chunk and chunk != group_size:
                return False
            chunk = 0
        elif ch == "#":
            if chunk == 0:
                cur_group += 1
            chunk += 1
        elif ch == "?":
            return chunk <= group_size
        else:
            raise ValueError(f"Unexpected character in input: {ch}")

    group_size = 0 if cur_group >= len(groups) else groups[cur_group]

    return chunk <= group_size


def preprocess_longest(pattern, groups):
    max_group = max(groups)
    ret_pattern = list(pattern)
    chunk = 0
    for i, ch in enumerate(pattern):
        if ch == ".":
            chunk = 0
        elif ch == "?":
            if chunk == max_group:
                ret_pattern[i] = "."
                if i - chunk - 1 >= 0:
                    ret_pattern[i - chunk - 1] = "."
            chunk = 0
        elif ch == "#":
            chunk += 1

    return "".join(ret_pattern)


def preprocess_pattern(pattern, groups):
    pattern = preprocess_longest(pattern, groups)

    ret_pattern = list(pattern)
    for i, ch in enumerate(pattern):
        if ch == "?":
            ret_pattern[i] = "#"
            if_broken = verify_prefix(ret_pattern, groups)

            ret_pattern[i] = "."
            if_operational = verify_prefix(ret_pattern, groups)

            if if_broken and if_operational:
                ret_pattern[i] = "?"
            elif if_broken and not if_operational:
                ret_pattern[i] = "#"
            elif not if_broken and if_operational:
                ret_pattern[i] = "."
            else:
                raise ValueError("No substitution matches groups")

    return "".join(ret_pattern)


@functools.cache
def solve_chunk_dac(chunk, groups):
    # base case len(groups) <= 1?
    if not chunk:
        return int(not groups)

    if len(groups) == 0:
        ret = int(all(ch != "#" for ch in chunk))
        return ret

    if len(groups) == 1:
        leftmost = chunk.find("#")
        rightmost = chunk.rfind("#")

        if leftmost == -1 and rightmost == -1:
            return max(0, len(chunk) - groups[0] + 1)

        min_size = rightmost - leftmost + 1
        if groups[0] < min_size:
            return 0

        leftmost_start = max(0, rightmost - groups[0] + 1)
        rightmost_start = min(leftmost, len(chunk) - groups[0])

        wiggle = rightmost_start - leftmost_start

        if wiggle < 0:
            return 0

        return wiggle + 1

    min_broken = chunk.count("#")
    max_broken = len(chunk) - len(groups) + 1
    if sum(groups) not in range(min_broken, max_broken + 1):
        return 0

    middle = len(chunk) // 2

    lsplit = chunk.rfind("?", 0, middle + 1)
    rsplit = chunk.find("?", middle)

    # base case no more ?
    if lsplit == -1 and rsplit == -1:
        ret = int(verify_solution(chunk, groups))
        return ret

    # -1 should always be furthest from the middle?
    if abs(lsplit - middle) < abs(rsplit - middle):
        split = lsplit
    else:
        split = rsplit

    left = chunk[:split]
    right = chunk[split + 1 :]
    combined = f"{left}#{right}"

    count = solve_chunk_dac(combined, groups)

    for n in range(0, len(groups) + 1):
        count += solve_chunk_dac(left, groups[:n]) * solve_chunk_dac(right, groups[n:])

    return count


@functools.cache
def solve(chunks, groups):
    if not chunks:
        return int(not groups)

    chunk = chunks[0]

    count = 0

    min_groups = len(groups) if len(chunks) == 1 else 0
    min_sum = chunk.count("#")

    for n in range(min_groups, len(groups) + 1):
        min_chunk_size = sum(groups[:n]) + n - 1

        if len(chunk) < min_chunk_size:
            break

        if sum(groups[:n]) < min_sum:
            continue

        chunk_count = solve_chunk_dac(chunk, groups[:n])
        if chunk_count:
            count += chunk_count * solve(chunks[1:], groups[n:])

    return count


def to_chunks(pattern):
    return tuple(pattern.replace(".", " ").split())


def solve_p1(path):
    count = 0
    with open(path) as f:
        for line in f:
            pattern, groups = line.strip().split(" ")
            groups = tuple(int(g) for g in groups.split(","))
            pattern = preprocess_pattern(pattern, groups)
            count += solve(to_chunks(pattern), groups)

    return count


def solve_p2(path):
    total = 0
    with open(path) as f:
        lines = list(f)

    for i, line in enumerate(lines):
        pattern, groups = line.strip().split(" ")
        groups = tuple(int(g) for g in groups.split(","))
        long_groups = groups * 5
        long_pattern = preprocess_pattern("?".join([pattern] * 5), long_groups)
        count = solve(to_chunks(long_pattern), long_groups)
        print(f"{i + 1}/{len(lines)} {pattern}, {groups}, {count}")

        total += count

    return total


def main():
    assert verify_solution("#.#.###", (1, 1, 3))
    assert verify_solution(".#...#....###.", (1, 1, 3))
    assert verify_solution(".#.###.#.######", (1, 3, 1, 6))
    assert verify_solution("####.#...#...", (4, 1, 1))
    assert verify_solution("#....######..#####.", (1, 6, 5))
    assert verify_solution(".###.##....#", (3, 2, 1))

    assert verify_prefix("?#?#?#?#?#?#?#?", (1, 3, 1, 6))
    assert verify_prefix(".#?#?#?#?#?#?#?", (1, 3, 1, 6))
    assert verify_prefix(".#.#?#?#?#?#?#?", (1, 3, 1, 6))
    assert verify_prefix(".#.###?#?#?#?#?", (1, 3, 1, 6))
    assert verify_prefix(".#.###.#?#?#?#?", (1, 3, 1, 6))
    assert verify_prefix(".#.###.#.#?#?#?", (1, 3, 1, 6))
    assert verify_prefix(".#.###.#.###?#?", (1, 3, 1, 6))
    assert verify_prefix(".#.###.#.#####?", (1, 3, 1, 6))
    assert verify_prefix(".#.###.#.######", (1, 3, 1, 6))

    assert not verify_prefix("##?#?#?#?#?#?#?", (1, 3, 1, 6))
    assert not verify_prefix(".###?#?#?#?#?#?", (1, 3, 1, 6))
    assert not verify_prefix(".#.#.#?#?#?#?#?", (1, 3, 1, 6))
    assert not verify_prefix(".#.#####?#?#?#?", (1, 3, 1, 6))
    assert not verify_prefix(".#.###.###?#?#?", (1, 3, 1, 6))
    assert not verify_prefix(".#.###.#.#.#?#?", (1, 3, 1, 6))
    assert not verify_prefix(".#.###.#.###.#?", (1, 3, 1, 6))
    assert not verify_prefix(".#.###.#.#####.", (1, 3, 1, 6))

    assert verify_prefix("..#..#####.", (1, 5))

    assert solve_chunk_dac("?", (3,)) == 0
    assert solve_chunk_dac("#", (3,)) == 0
    assert solve_chunk_dac("?.???.?", ()) == 1
    assert solve_chunk_dac("?#.?#?.", ()) == 0
    assert solve_chunk_dac("???#???#???", (7,)) == 3
    assert solve_chunk_dac("?#???#?", (7,)) == 1
    assert solve_chunk_dac("##?#?", (2, 1)) == 1
    assert solve_chunk_dac("##???", (2, 1)) == 2
    assert solve_chunk_dac("?###????????", (3, 2, 1)) == 10
    assert solve_chunk_dac("?#?#?#?#?#?#?#?", (1, 3, 1, 6)) == 1

    assert (
        solve_chunk_dac(
            "?###??????????###??????????###??????????###??????????###????????",
            (3, 2, 1, 3, 2, 1, 3, 2, 1, 3, 2, 1, 3, 2, 1),
        )
        == 506250
    )

    assert solve_p1("example") == 21
    print(solve_p1("input"))

    print(solve_p2("example"))
    assert solve_p2("example") == 525152
    print(solve_p2("input"))


if __name__ == "__main__":
    main()
