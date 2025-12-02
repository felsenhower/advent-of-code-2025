import sys
from pathlib import Path


def main():
    result = 0
    puzzle = [l.strip() for l in Path(sys.argv[1]).read_text().split(",")]
    for r in puzzle:
        (first, second) = [int(x) for x in r.split("-")]
        for i in range(first, second + 1):
            j = str(i)
            if len(j) % 2 != 0:
                continue
            first_half = j[: (len(j) // 2)]
            second_half = j[(len(j) // 2) :]
            if first_half != second_half:
                continue
            result += i
    print(result)


if __name__ == "__main__":
    main()
