import sys


def wrap_around(position: int) -> int:
    while True:
        if 0 <= position <= 99:
            return position
        if position < 0:
            position = 100 + position
        if position > 99:
            position = position - 100


def main():
    counter = 0
    position = 50
    with open(sys.argv[1]) as f:
        for l in f:
            l = l.strip()
            if not l:
                continue
            direction = l[0]
            distance = int(l[1:])
            difference = (1 if direction == "R" else (-1)) * distance
            position += difference
            position = wrap_around(position)
            if position == 0:
                counter += 1
    print(counter)


if __name__ == "__main__":
    main()
