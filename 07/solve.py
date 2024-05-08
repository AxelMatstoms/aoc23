def label_to_num(label):
    if label.isnumeric():
        return int(label)

    LABELS = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}

    return LABELS[label]


def hand_type(hand):
    counts = [0] * 15
    for label in hand:
        counts[label] += 1

    counts.sort(reverse=True)

    if counts[0] == 5:  # five of a kind
        hand_type = 6
    elif counts[0] == 4:  # four of a kind
        hand_type = 5
    elif counts[0] == 3 and counts[1] == 2:  # full house
        hand_type = 4
    elif counts[0] == 3:  # three of a kind
        hand_type = 3
    elif counts[0] == 2 and counts[1] == 2:  # two pairs
        hand_type = 2
    elif counts[0] == 2:  # one pair
        hand_type = 1
    else:  # high card
        hand_type = 0

    return hand_type


def label_to_num_wild(label):
    if label.isnumeric():
        return int(label)

    LABELS = {"T": 10, "J": 1, "Q": 12, "K": 13, "A": 14}

    return LABELS[label]


def hand_type_wild(hand):
    counts = [0] * 15
    for label in hand:
        counts[label] += 1

    jokers = counts[1]
    counts[1] = 0

    counts.sort(reverse=True)
    counts[0] += jokers

    if counts[0] == 5:  # five of a kind
        hand_type = 6
    elif counts[0] == 4:  # four of a kind
        hand_type = 5
    elif counts[0] == 3 and counts[1] == 2:  # full house
        hand_type = 4
    elif counts[0] == 3:  # three of a kind
        hand_type = 3
    elif counts[0] == 2 and counts[1] == 2:  # two pairs
        hand_type = 2
    elif counts[0] == 2:  # one pair
        hand_type = 1
    else:  # high card
        hand_type = 0

    return hand_type


def solve_p1(path):
    hands = []
    with open(path) as f:
        for line in f:
            hand, bid = line.strip().split()
            hand = tuple(label_to_num(label) for label in hand)
            hands.append((hand_type(hand), hand, int(bid)))

    hands.sort()

    return sum((i + 1) * bid for i, (_, _, bid) in enumerate(hands))


def solve_p2(path):
    hands = []
    with open(path) as f:
        for line in f:
            hand, bid = line.strip().split()
            hand = tuple(label_to_num_wild(label) for label in hand)
            hands.append((hand_type_wild(hand), hand, int(bid)))

    hands.sort()

    return sum((i + 1) * bid for i, (_, _, bid) in enumerate(hands))


def main():
    assert solve_p1("example") == 6440
    print(solve_p1("input"))

    assert solve_p2("example") == 5905
    print(solve_p2("input"))


if __name__ == "__main__":
    main()
