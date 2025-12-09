import sys
from pathlib import Path
import math
import itertools
from math import prod

type point = tuple[int, int, int]


def distance(a: point, b: point) -> float:
    ax, ay, az = a
    bx, by, bz = b
    cx, cy, cz = (ax - bx, ay - by, az - bz)
    return math.sqrt(cx**2 + cy**2 + cz**2)


def merge_circuits(
    circuits: dict[point, list[point]], a: point, b: point
) -> list[point]:
    if circuits[a] is circuits[b]:
        return circuits[a]
    b_circuits = circuits[b].copy()
    for p in b_circuits:
        circuits[a].append(p)
        circuits[p] = circuits[a]
    assert circuits[a] is circuits[b]
    return circuits[a]


def main():
    points = [
        tuple(int(x) for x in line.strip().split(","))
        for line in Path(sys.argv[1]).read_text().strip().split("\n")
    ]

    distances = []
    circuits = {coord: [coord] for coord in points}
    for a, b in itertools.combinations(points, 2):
        dist = distance(a, b)
        distances.append((dist, a, b))
    distances.sort()
    for i, (dist, a, b) in enumerate(distances):
        merged = merge_circuits(circuits, a, b)
        print(a, b)
        if len(merged) == len(points):
            result = a[0] * b[0]
            print(result)
            return


if __name__ == "__main__":
    main()
