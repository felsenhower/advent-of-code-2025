import sys
from pathlib import Path
import itertools

type point = tuple[int, int]


def get_area(a: point, b: point) -> int:
    ax, ay = a
    bx, by = b
    area = (abs(ax - bx) + 1) * (abs(ay - by) + 1)
    return area


def main():
    points = [
        tuple(int(x) for x in line.strip().split(","))
        for line in Path(sys.argv[1]).read_text().strip().split("\n")
    ]
    max_rect = (0, None, None)
    for a, b in itertools.combinations(points, 2):
        area = get_area(a, b)
        if area > max_rect[0]:
            max_rect = (area, a, b)
    print(max_rect[0])


if __name__ == "__main__":
    main()
