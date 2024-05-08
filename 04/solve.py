from collections import defaultdict


def parse_card(line):
    card_nr_part, numbers = line.strip().split(": ")
    card_nr = int(card_nr_part.split()[1])

    left, right = numbers.split("|")
    left = set(int(nr) for nr in left.strip().split())
    right = set(int(nr) for nr in right.strip().split())

    return card_nr, left, right


def solve_p1(path):
    ans = 0
    with open(path) as f:
        for line in f:
            _, l, r = parse_card(line)
            both = l & r
            if both:
                ans += 1 << (len(both) - 1)

    return ans


def solve_p2(path):
    cards = []
    with open(path) as f:
        for line in f:
            _, l, r = parse_card(line)
            both = l & r
            cards.append(len(both))

    counts = [1 for _ in cards]

    for i, overlap in enumerate(cards):
        count = counts[i]

        for k in range(i + 1, i + overlap + 1):
            counts[k] += count

    return sum(counts)


def main():
    assert solve_p1("example") == 13
    print(solve_p1("input"))

    assert solve_p2("example") == 30
    print(solve_p2("input"))


if __name__ == "__main__":
    main()
