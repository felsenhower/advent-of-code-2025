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


def merge_circuits(circuits: dict[point, list[point]], a: point, b: point) -> None:
    if circuits[a] is circuits[b]:
        return
    b_circuits = circuits[b].copy()
    for p in b_circuits:
        circuits[a].append(p)
        circuits[p] = circuits[a]
    assert circuits[a] is circuits[b]


def get_all_circuits(
    points: list[point], circuits: dict[point, list[point]]
) -> list[list[point]]:
    result = []
    points = set(points)
    while len(points) > 0:
        p = points.pop()
        c = circuits[p]
        result.append(c)
        for p2 in c:
            if p2 in points:
                points.remove(p2)
    return result


def main():
    points = [
        tuple(int(x) for x in line.strip().split(","))
        for line in Path(sys.argv[1]).read_text().strip().split("\n")
    ]

    # This is a bit weird, but I guess it's what the puzzle says...
    num_connections = 1000 if len(points) > 20 else 10

    distances = []
    circuits = {coord: [coord] for coord in points}
    for a, b in itertools.combinations(points, 2):
        dist = distance(a, b)
        distances.append((dist, a, b))
    distances.sort()
    for i, (dist, a, b) in enumerate(distances):
        merge_circuits(circuits, a, b)
        if i + 1 == num_connections:
            break
    circuits_list = get_all_circuits(points, circuits)
    circuit_lengths = [len(c) for c in circuits_list]
    circuit_lengths.sort()
    circuit_lengths.reverse()
    result = prod(circuit_lengths[:3])
    print(result)


if __name__ == "__main__":
    main()
