import sys
from random import shuffle


def ranges_union(
    range1: tuple[int, int], range2: tuple[int, int]
) -> list[tuple[int, int]]:
    (lower1, upper1) = range1
    (lower2, upper2) = range2
    if range1 == range2:
        return [range1]
    if upper1 < lower2:
        # already disjoint
        return [range1, range2]
    if upper2 < lower1:
        # already disjoint
        return [range1, range2]
    if lower1 <= lower2 <= upper2 <= upper1:
        # range2 completely inside range1
        return [range1]
    if lower2 <= lower1 <= upper1 <= upper2:
        # range1 completely inside range2
        return [range2]
    if lower1 <= lower2 <= upper1 <= upper2:
        # overlapping
        return [(lower1, upper2)]
    if lower2 <= lower1 <= upper2 <= upper1:
        # overlapping
        return [(lower2, upper1)]

    assert False, ("Well how did this happen?", range1, range2)


def simplify_range_list_maybe_sorta_thing(
    ranges: list[tuple[int, int]],
) -> list[tuple[int, int]]:
    assert len(ranges) >= 2
    ranges = ranges.copy()
    shuffle(ranges)
    r1 = ranges.pop()
    r2 = ranges.pop()
    result = ranges_union(r1, r2)
    while len(ranges) > 0:
        r1 = ranges.pop()
        r2 = result.pop()
        result += ranges_union(r1, r2)
    return result


def main():
    ranges = []
    ingredients = []
    with open(sys.argv[1]) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if "-" in line:
                ranges.append(tuple(int(x) for x in line.split("-")))
            else:
                ingredients.append(int(line))
    # This might be one of the conceptually most cursed things I've ever written...
    result_before = None
    for attempt in range(1, 200000):
        ranges2 = simplify_range_list_maybe_sorta_thing(ranges)
        result = 0
        for lower, upper in ranges:
            result += upper - lower + 1
        print(f"\r{result=}; {attempt=}", end="")
        if result_before != result:
            print("")
        result_before = result
        ranges = ranges2
        attempt += 1
    print("")
    print(f"The result is maybe maybe {result}, but I don't really know tbh...")


if __name__ == "__main__":
    main()
