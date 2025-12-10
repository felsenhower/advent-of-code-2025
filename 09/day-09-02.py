import sys
from pathlib import Path
import itertools
import numpy as np
from tqdm import tqdm
from matplotlib.path import Path as Path2
from skimage.draw import polygon

type point = tuple[int, int]

UNKNOWN = -1
EMPTY = 0
RED = 1
GREEN = 2


def get_area(a: point, b: point) -> int:
    ax, ay = a
    bx, by = b
    area = (abs(ax - bx) + 1) * (abs(ay - by) + 1)
    return area


def display(arr: np.ndarray) -> None:
    arr = arr.transpose()
    global RED
    global GREEN
    for row in arr:
        for c in row:
            if c == RED:
                print("#", end="")
            elif c == GREEN:
                print("X", end="")
            elif c == UNKNOWN:
                print("?", end="")
            else:
                print(".", end="")
        print("")


def make_red(arr: np.ndarray, p: point) -> None:
    x, y = p
    arr[x, y] = RED


def make_green(arr: np.ndarray, p: point) -> None:
    x, y = p
    arr[x, y] = GREEN


def make_red_tiles_red(floor: np.ndarray, red_tiles: list[point]) -> None:
    for p in tqdm(red_tiles):
        make_red(floor, p)


def connect_tiles(arr: np.ndarray, a: point, b: point) -> None:
    ax, ay = a
    bx, by = b
    if ax == bx:
        x = ax
        lower_y = min(ay, by)
        upper_y = max(ay, by)
        for y in range(lower_y, upper_y + 1):
            if arr[x, y] in (EMPTY, UNKNOWN):
                make_green(arr, (x, y))
        return
    if ay == by:
        y = ay
        lower_x = min(ax, bx)
        upper_x = max(ax, bx)
        for x in range(lower_x, upper_x + 1):
            if arr[x, y] in (EMPTY, UNKNOWN):
                make_green(arr, (x, y))
        return
    assert False, (
        a,
        b,
    )


def connect_red_tiles_with_green(floor: np.ndarray, red_tiles: list[point]) -> None:
    for a, b in tqdm(list(itertools.pairwise(red_tiles + [red_tiles[0]]))):
        connect_tiles(floor, a, b)


def flood_fill(arr: np.ndarray, start: point, value) -> None:
    width, height = arr.shape
    num_pixels_total = width * height
    max_x, max_y = (width - 1, height - 1)
    start_value = arr[start[0], start[1]]
    point_stack = [start]
    pixels_painted = 0
    while (stack_size := len(point_stack)) > 0:
        p = point_stack.pop()
        if arr[p[0], p[1]] != start_value:
            continue
        arr[p[0], p[1]] = value
        pixels_painted += 1
        print(
            "\rPainted {:3.3f}% of picture; Stack contains {:3.3f}% of picture.".format(
                pixels_painted * 100.0 / num_pixels_total,
                stack_size * 100.0 / num_pixels_total,
            ),
            end="",
        )
        north = (p[0], p[1] - 1)
        south = (p[0], p[1] + 1)
        west = (p[0] - 1, p[1])
        east = (p[0] + 1, p[1])
        for neighbor in (north, south, west, east):
            if not (0 <= neighbor[0] <= max_x):
                continue
            if not (0 <= neighbor[1] <= max_y):
                continue
            if arr[neighbor[0], neighbor[1]] != start_value:
                continue
            point_stack.append(neighbor)
    print("")


def make_outside_empty(floor: np.ndarray) -> None:
    width, height = floor.shape
    max_x, max_y = (width - 1, height - 1)
    flood_fill(floor, (max_x, max_y), EMPTY)


def make_inside_green(floor: np.ndarray) -> None:
    floor[floor == UNKNOWN] = GREEN


def is_rect_completely_inside_polygon(arr: np.ndarray, a: point, b: point) -> bool:
    ax, ay = a
    bx, by = b
    lower_x = min(ax, bx)
    upper_x = max(ax, bx)
    lower_y = min(ay, by)
    upper_y = max(ay, by)
    for x in range(lower_x, upper_x + 1):
        for y in range(lower_y, upper_y + 1):
            if arr[x, y] == EMPTY:
                return False
    return True


def main():
    red_tiles = [
        tuple(int(x) for x in line.strip().split(","))
        for line in Path(sys.argv[1]).read_text().strip().split("\n")
    ]
    max_x = max(red_tiles, key=lambda p: p[0])[0]
    max_y = max(red_tiles, key=lambda p: p[1])[1]
    arr_shape = (max_x + 3, max_y + 3)
    print("Init floor...")
    floor = np.ones(arr_shape, dtype=np.int8) * UNKNOWN
    print("Make tiles red...")
    make_red_tiles_red(floor, red_tiles)
    print("Connect red tiles with green...")
    connect_red_tiles_with_green(floor, red_tiles)
    print("Make outside of polygon empty...")
    make_outside_empty(floor)
    print("Make inside of polygon green...")
    make_inside_green(floor)
    # display(floor)

    max_rect = (0, None, None)
    print("Find largest rectangle...")
    for a, b in tqdm(list(itertools.combinations(red_tiles, 2))):
        area = get_area(a, b)
        if area <= max_rect[0]:
            continue
        if not is_rect_completely_inside_polygon(floor, a, b):
            continue
        max_rect = (area, a, b)
    print(max_rect[0])


if __name__ == "__main__":
    main()
