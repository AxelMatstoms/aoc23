from functools import reduce
from itertools import count
from collections import defaultdict, deque
import operator


def solve_p1(path):
    mod_dests = {}
    mod_type = {}
    with open(path) as f:
        for line in f:
            name, dests = line.strip().split(" -> ")
            if name[0] == "%" or name[0] == "&":
                type_, name = name[0], name[1:]
            else:
                type_ = name

            mod_type[name] = type_

            mod_dests[name] = dests.split(", ")

    # Set conjunction inputs False
    conjunction_inputs = defaultdict(dict)
    flipflop_states = {}
    for mod, dests in mod_dests.items():
        if mod_type[mod] == "%":
            flipflop_states[mod] = False

        for dst in dests:
            if dst in mod_type and mod_type[dst] == "&":
                conjunction_inputs[dst][mod] = False

    counts = [0, 0]
    for _ in range(1000):
        button_signal = ("broadcaster", False, "button")
        signals = deque([button_signal])

        while signals:
            mod, high, origin = signals.popleft()
            counts[int(high)] += 1

            if mod not in mod_type:
                continue

            if mod == "broadcaster":
                signals.extend((dst, high, mod) for dst in mod_dests[mod])
            elif mod_type[mod] == "%" and not high:
                flipflop_states[mod] = not flipflop_states[mod]
                signals.extend(
                    (dst, flipflop_states[mod], mod) for dst in mod_dests[mod]
                )
            elif mod_type[mod] == "&":
                conjunction_inputs[mod][origin] = high
                send_high = not all(conjunction_inputs[mod].values())
                signals.extend((dst, send_high, mod) for dst in mod_dests[mod])

    return counts[0] * counts[1]


def solve_p2(path):
    mod_dests = {}
    mod_type = {}
    with open(path) as f:
        for line in f:
            name, dests = line.strip().split(" -> ")
            if name[0] == "%" or name[0] == "&":
                type_, name = name[0], name[1:]
            else:
                type_ = name

            mod_type[name] = type_

            mod_dests[name] = dests.split(", ")

    # Set conjunction inputs False
    conjunction_inputs = defaultdict(dict)
    flipflop_states = {}
    for mod, dests in mod_dests.items():
        if mod_type[mod] == "%":
            flipflop_states[mod] = False

        for dst in dests:
            if dst in mod_type and mod_type[dst] == "&":
                conjunction_inputs[dst][mod] = False
            if dst == "rx":
                before_rx = mod

    cycles = {mod: 0 for mod in conjunction_inputs[before_rx]}

    found_cycle = False
    for i in count(1):
        button_signal = ("broadcaster", False, "button")
        signals = deque([button_signal])

        if found_cycle:
            break

        while signals:
            mod, high, origin = signals.popleft()

            if mod not in mod_type:
                continue

            if mod == before_rx and high:
                if cycles[origin] == 0:
                    cycles[origin] = i
                if all(cycle for cycle in cycles.values()):
                    found_cycle = True
                    break

            if mod == "broadcaster":
                signals.extend((dst, high, mod) for dst in mod_dests[mod])
            elif mod_type[mod] == "%" and not high:
                flipflop_states[mod] = not flipflop_states[mod]
                signals.extend(
                    (dst, flipflop_states[mod], mod) for dst in mod_dests[mod]
                )
            elif mod_type[mod] == "&":
                conjunction_inputs[mod][origin] = high
                send_high = not all(conjunction_inputs[mod].values())
                signals.extend((dst, send_high, mod) for dst in mod_dests[mod])

    return reduce(operator.mul, cycles.values())


def main():
    assert solve_p1("example") == 32000000
    assert solve_p1("example2") == 11687500
    print(solve_p1("input"))

    print(solve_p2("input"))


if __name__ == "__main__":
    main()
