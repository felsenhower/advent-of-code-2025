import sys
from pathlib import Path
import itertools
import numpy as np
from tqdm import tqdm
from matplotlib.path import Path as Path2
from skimage.draw import polygon

type point = tuple[int, int]

RED = 1
GREEN = 2


def get_area(a: point, b: point) -> int:
    ax, ay = a
    bx, by = b
    area = (abs(ax - bx) + 1) * (abs(ay - by) + 1)
    return area


def make_red(arr: np.ndarray, p: point) -> None:
    x, y = p
    arr[x, y] = RED


def make_green(arr: np.ndarray, p: point) -> None:
    x, y = p
    arr[x, y] = GREEN


def connect_tiles(arr: np.ndarray, a: point, b: point) -> None:
    ax, ay = a
    bx, by = b
    if ax == bx:
        x = ax
        lower_y = min(ay, by)
        upper_y = max(ay, by)
        for y in range(lower_y, upper_y + 1):
            if arr[x, y] == 0:
                make_green(arr, (x, y))
        return
    if ay == by:
        y = ay
        lower_x = min(ax, bx)
        upper_x = max(ax, bx)
        for x in range(lower_x, upper_x + 1):
            if arr[x, y] == 0:
                make_green(arr, (x, y))
        return
    assert False, (
        a,
        b,
    )


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
            else:
                print(".", end="")
        print("")


def get_winding_number(s) -> int:
    current_color = 0
    winding_number = 0
    for elem in s:
        if current_color in (RED, GREEN):
            if elem not in (RED, GREEN):
                current_color = elem
        else:
            if elem in (RED, GREEN):
                winding_number += 1
                current_color = elem
    return winding_number


def is_inside_polygon(arr: np.ndarray, p: point) -> bool:
    x, y = p
    current_color = arr[x, y]
    if current_color in (RED, GREEN):
        return True
    assert current_color == 0
    winding_number1 = get_winding_number(arr[: x + 1, y])
    winding_number2 = get_winding_number(arr[x:, y])
    return (winding_number1 % 2 == 1) and (winding_number2 % 2 == 1)


def is_rect_completely_inside_polygon(arr: np.ndarray, a: point, b: point) -> bool:
    ax, ay = a
    bx, by = b
    lower_x = min(ax, bx)
    upper_x = max(ax, bx)
    lower_y = min(ay, by)
    upper_y = max(ay, by)
    for x in range(lower_x, upper_x + 1):
        for y in range(lower_y, upper_y + 1):
            if arr[x, y] == 0:
                return False
    return True


def color_inside_green(arr: np.ndarray) -> np.ndarray:
    inside_tiles = np.zeros(arr.shape, dtype=np.uint8)
    for x in tqdm(range(arr.shape[0]), mininterval=0, miniters=1):
        for y in range(arr.shape[1]):
            if arr[x, y] in (RED, GREEN):
                continue
            if is_inside_polygon(arr, (x, y)):
                inside_tiles[x, y] = GREEN
    return arr + inside_tiles


# def color_inside_green_fast(arr: np.ndarray, red_tiles: list[point]) -> np.ndarray:
#     with tqdm(total=6, mininterval=0, miniters=1) as pbar:
#         xs = np.array([p[0] for p in red_tiles])
#         pbar.update(1)
#         ys = np.array([p[1] for p in red_tiles])
#         pbar.update(1)
#         rr, cc = polygon(xs, ys)
#         pbar.update(1)
#         inside_tiles = np.zeros(arr.shape, dtype=np.uint8)
#         pbar.update(1)
#         inside_tiles[rr, cc] = GREEN
#         pbar.update(1)
#         result = arr + inside_tiles
#         pbar.update(1)
#         return result


def main():
    red_tiles = [
        tuple(int(x) for x in line.strip().split(","))
        for line in Path(sys.argv[1]).read_text().strip().split("\n")
    ]
    max_x = max(red_tiles, key=lambda p: p[0])[0]
    max_y = max(red_tiles, key=lambda p: p[1])[1]
    arr_shape = (max_x + 3, max_y + 3)
    floor = np.zeros(arr_shape, dtype=np.uint8)
    print("Make tiles red...")
    for p in tqdm(red_tiles):
        make_red(floor, p)
    print("Connect red tiles with green...")
    for a, b in tqdm(list(itertools.pairwise(red_tiles + [red_tiles[0]]))):
        connect_tiles(floor, a, b)

    print("Color the inside of the region green...")
    floor = color_inside_green(floor)
    # floor = color_inside_green_fast(floor, red_tiles)
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
