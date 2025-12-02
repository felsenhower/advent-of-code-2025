import sys
from pathlib import Path
from tqdm import tqdm


def is_invalid(_id: int) -> bool:
    id_str = str(_id)
    length = len(id_str)
    for part_length in range(1, length // 2 + 1):
        if length % part_length != 0:
            continue
        part = id_str[:part_length]
        num_parts = length // part_length
        expected_id = num_parts * part
        if expected_id == id_str:
            return True
    return False


def main():
    result = 0
    puzzle = [l.strip() for l in Path(sys.argv[1]).read_text().split(",")]
    for r in tqdm(puzzle):
        (first, second) = [int(x) for x in r.split("-")]
        for i in range(first, second + 1):
            if is_invalid(i):
                result += i
    print(result)


if __name__ == "__main__":
    main()
