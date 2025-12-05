import sys


def is_in_range(i: int, r: tuple[int, int]) -> bool:
    (lower, upper) = r
    return lower <= i <= upper


def is_fresh(ingredient: int, ranges: list[tuple[int, int]]) -> bool:
    for r in ranges:
        if is_in_range(ingredient, r):
            return True
    return False


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
    result = 0
    for i in ingredients:
        if is_fresh(i, ranges):
            result += 1
    print(result)


if __name__ == "__main__":
    main()
