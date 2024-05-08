def range_overlap(start, span, other_start, other_span):
    new_start = max(start, other_start)
    new_end = min(start + span, other_start + other_span)
    new_span = new_end - new_start

    if new_span <= 0:
        return 0, -1

    return new_start, new_span


def range_subtract(start, span, sub_start, sub_span):
    overlap_start, overlap_span = range_overlap(start, span, sub_start, sub_span)

    if overlap_span == -1:
        return [(start, span)]

    left_start = start
    left_span = overlap_start - left_start

    right_start = overlap_start + overlap_span
    right_span = start + span - overlap_start - overlap_span

    out = []
    if left_span > 0:
        out.append((left_start, left_span))

    if right_span > 0:
        out.append((right_start, right_span))

    return out


class Map:
    def __init__(self, mappings):
        self.mappings = mappings

    def __getitem__(self, idx):
        for dst, src, span in self.mappings:
            if idx < src or idx >= src + span:
                continue

            return dst + (idx - src)

        return idx

    def query_range(self, query_start, query_span):
        for dst, src, span in self.mappings:
            overlap_start, overlap_span = range_overlap(
                src, span, query_start, query_span
            )
            if overlap_span != -1:
                yield dst + (overlap_start - src), overlap_span

        for start, span in self.query_unmapped(query_start, query_span):
            yield start, span

    def query_unmapped(self, query_start, query_span):
        for dst, src, span in self.mappings:
            result = range_subtract(query_start, query_span, src, span)
            if len(result) == 2:
                joined = self.query_unmapped(*result[0])
                joined.extend(self.query_unmapped(*result[1]))

                return joined
            if len(result) == 0:
                return result

            query_start, query_span = result[0]

        return [(query_start, query_span)]

    def __repr__(self):
        mapping_part = ", ".join(
            f"{src}...{src+span-1}=>{dst}...{dst+span-1}"
            for dst, src, span in self.mappings
        )
        return f"Map({mapping_part})"

    @classmethod
    def parse(cls, lines):
        mappings = [tuple(int(v) for v in line.strip().split()) for line in lines]

        return cls(mappings)


def parse_map(itr):
    desc_line = next(itr)
    desc, map_ = desc_line.strip().split(" ")

    assert map_ == "map:"

    from_, to = desc.split("-to-")

    mapping_lines = []
    try:
        while line := next(itr).strip():
            mapping_lines.append(line)
    except StopIteration:
        pass

    return (from_, to, Map.parse(mapping_lines))


def parse_input(f):
    itr = iter(f)

    seeds_line = next(itr)
    seeds_name, seeds_list = seeds_line.split(":")

    assert seeds_name == "seeds"
    seeds = [int(seed) for seed in seeds_list.strip().split()]

    empty = next(itr)
    assert not empty.strip()

    map_meta = {}
    maps = {}
    while True:
        try:
            from_, to, map_ = parse_map(itr)
        except StopIteration:
            break

        map_meta[from_] = to
        maps[from_] = map_

    return (seeds, map_meta, maps)


def solve_p1(path):
    with open(path) as f:
        seeds, map_meta, maps = parse_input(f)

    ans = float("inf")

    for seed in seeds:
        value = seed
        current_type = "seed"

        while current_type in map_meta:
            map_ = maps[current_type]
            value = map_[value]
            current_type = map_meta[current_type]

        assert current_type == "location"
        ans = min(ans, value)

    return ans


def solve_p2(path):
    with open(path) as f:
        seeds, map_meta, maps = parse_input(f)

    ranges = list(zip(seeds[::2], seeds[1::2]))
    current_type = "seed"

    while current_type in map_meta:
        new_ranges = []
        map_ = maps[current_type]
        for start, span in ranges:
            new_ranges.extend(map_.query_range(start, span))

        current_type = map_meta[current_type]
        ranges = new_ranges

    assert current_type == "location"

    ans = min(range_[0] for range_ in ranges)

    return ans


def main():
    assert range_overlap(1, 10, 7, 10) == (7, 4)
    assert range_overlap(1, 10, 3, 3) == (3, 3)
    assert range_overlap(1, 10, 20, 10) == (0, -1)

    assert range_subtract(1, 10, 20, 10) == [(1, 10)]
    assert range_subtract(1, 10, 4, 2) == [(1, 3), (6, 5)]
    assert range_subtract(10, 10, 8, 4) == [(12, 8)]
    assert range_subtract(10, 10, 18, 4) == [(10, 8)]

    assert solve_p1("example") == 35
    print(solve_p1("input"))

    assert solve_p2("example") == 46
    print(solve_p2("input"))


if __name__ == "__main__":
    main()
