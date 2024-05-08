import operator


def parse_workflows(itr):
    workflows = {}
    for line in itr:
        line = line.strip()

        if not line:
            break

        name, rules_part = line.split("{")
        rules_split = rules_part.strip("}").split(",")
        rules = []
        for rule in rules_split:
            if ":" in rule:
                condition, send_to = rule.split(":")
                attr = condition[0]
                op = condition[1]
                thresh = int(condition[2:])

                rules.append((attr, op, thresh, send_to))
            else:
                rules.append(("x", ">", float("-inf"), rule))  # always true

        workflows[name] = rules

    return workflows


def parse_parts(itr):
    parts = []
    for line in itr:
        part = {}

        for assignment in line.strip().strip("{}").split(","):
            name, _, value = assignment.partition("=")
            part[name] = int(value)

        parts.append(part)

    return parts


def solve_p1(path):
    CONDITION = {"<": operator.lt, ">": operator.gt}

    with open(path) as f:
        itr = iter(f)
        workflows = parse_workflows(itr)
        parts = parse_parts(itr)

    xmas_sum = 0

    for part in parts:
        workflow = "in"
        while workflow != "R" and workflow != "A":
            rules = workflows[workflow]
            for name, op, thresh, send_to in rules:
                if CONDITION[op](part[name], thresh):
                    workflow = send_to
                    break

        if workflow == "A":
            xmas_sum += sum(part.values())

    return xmas_sum


def pass_constraint(constraint, name, op, thresh):
    ret = {**constraint}

    min_, max_ = constraint[name]
    if op == ">":
        min_ = max(thresh + 1, min_)
    elif op == "<":
        max_ = min(thresh - 1, max_)

    ret[name] = (min_, max_)

    return ret


def fail_constraint(constraint, name, op, thresh):
    ret = {**constraint}

    min_, max_ = constraint[name]
    if op == ">":
        max_ = min(thresh, max_)
    elif op == "<":
        min_ = max(thresh, min_)

    ret[name] = (min_, max_)

    return ret


def impossible(constraint):
    return any(min_ > max_ for min_, max_ in constraint.values())


def cardinality(constraint):
    cardinality = 1
    for min_, max_ in constraint.values():
        cardinality *= max(0, max_ - min_ + 1)

    return cardinality

def intersect(constraints):
    ret = {"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)}
    for constraint in constraints:
        for name, (min_, max_) in constraint.items():
            pass


def solve_p2(path):
    with open(path) as f:
        itr = iter(f)
        workflows = parse_workflows(itr)

    # Step 1: Pray that the graph is acyclic
    init_constraint = {"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)}
    start_node = "in"

    accepted = []

    to_visit = [(start_node, init_constraint)]

    # Step 2: Search paths through graph, adjusting constraints as necessary
    while to_visit:
        node, constraint = to_visit.pop()

        if node == "R":
            continue
        if node == "A":
            accepted.append(constraint)
            continue

        rules = workflows[node]
        for name, op, thresh, send_to in rules:
            pass_ = pass_constraint(constraint, name, op, thresh)
            constraint = fail_constraint(constraint, name, op, thresh)

            if not impossible(pass_):
                to_visit.append((send_to, pass_))

            if impossible(constraint):
                break

    # Step 3: Pray there is no overlap so we don't have to use PIE
    return sum(cardinality(constraint) for constraint in accepted)


def main():
    assert solve_p1("example") == 19114
    print(solve_p1("input"))

    assert solve_p2("example") == 167409079868000
    print(solve_p2("input"))


if __name__ == "__main__":
    main()
