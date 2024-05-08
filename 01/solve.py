def solve_p1(path):
    ans = 0
    with open(path) as f:
        for line in f:
            digits = [int(ch) for ch in line if ch.isdigit()]
            first = digits[0]
            last = digits[-1]

            ans += 10 * first + last

    return ans


def solve_p2(path):
    ans = 0
    with open(path) as f:
        for line in f:
            digit_lut = {
                "one": 1,
                "two": 2,
                "three": 3,
                "four": 4,
                "five": 5,
                "six": 6,
                "seven": 7,
                "eight": 8,
                "nine": 9,
                "1": 1,
                "2": 2,
                "3": 3,
                "4": 4,
                "5": 5,
                "6": 6,
                "7": 7,
                "8": 8,
                "9": 9,
            }
            first = min(
                (
                    (idx, num)
                    for name, num in digit_lut.items()
                    if (idx := line.find(name)) != -1
                )
            )[1]
            last = max(
                (
                    (idx, num)
                    for name, num in digit_lut.items()
                    if (idx := line.rfind(name)) != -1
                )
            )[1]

            ans += 10 * first + last

    return ans


def main():
    assert solve_p1("example") == 142
    print(solve_p1("input"))

    assert solve_p2("example2") == 281
    print(solve_p2("input"))


if __name__ == "__main__":
    main()
