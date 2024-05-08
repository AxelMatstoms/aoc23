def parse_game(line):
    game_part, sets_part = line.strip().split(":")

    _, game_id = game_part.split()
    game_id = int(game_id)

    sets = []
    for set_str in sets_part.split(";"):
        set_ = {"red": 0, "green": 0, "blue": 0}
        for ball_desc in set_str.split(", "):
            amt, color = ball_desc.strip().split(" ")
            set_[color] = int(amt)

        sets.append(set_)

    return game_id, sets


def dict_max(dicts):
    max_ = {}
    for d in dicts:
        larger = {k: v for k, v in d.items() if k not in max_ or v > max_[k]}
        max_.update(larger)

    return max_


def solve_p1(path):
    id_sum = 0

    with open(path) as f:
        for line in f:
            game_id, sets = parse_game(line)
            max_ = dict_max(sets)
            possible = max_["red"] <= 12 and max_["green"] <= 13 and max_["blue"] <= 14
            if possible:
                id_sum += game_id

    return id_sum


def solve_p2(path):
    power_sum = 0

    with open(path) as f:
        for line in f:
            game_id, sets = parse_game(line)
            max_ = dict_max(sets)
            power_sum += max_["red"] * max_["green"] * max_["blue"]

    return power_sum


def main():
    assert solve_p1("example") == 8
    print(solve_p1("input"))

    assert solve_p2("example") == 2286
    print(solve_p2("input"))


if __name__ == "__main__":
    main()
