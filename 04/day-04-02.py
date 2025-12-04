import sys
from pathlib import Path
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view


def main():
    puzzle = np.array(
        [
            [1 if digit == "@" else 0 for digit in line.strip()]
            for line in Path(sys.argv[1]).read_text().strip().split("\n")
        ]
    )
    puzzle = np.pad(puzzle, 1, mode="constant", constant_values=0)
    result = 0
    while True:
        rolls_to_remove = []
        for i, wrow in enumerate(sliding_window_view(puzzle, (3, 3))):
            for j, window in enumerate(wrow):
                if window[1, 1] and window.sum() < 5:
                    rolls_to_remove.append((i, j))
        if len(rolls_to_remove) == 0:
            break
        result += len(rolls_to_remove)
        for i, j in rolls_to_remove:
            puzzle[i + 1, j + 1] = 0
    print(result)


if __name__ == "__main__":
    main()
