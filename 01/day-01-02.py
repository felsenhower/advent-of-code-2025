import sys


def add(position: int, difference: int) -> (int, int):
    zero_count = 0
    sign = 1 if difference > 0 else -1
    abs_diff = difference if difference > 0 else -difference
    for i in range(abs_diff):
        position += sign
        if position == -1:
            position = 99
        if position == 100:
            position = 0
        if position == 0:
            zero_count += 1
    return position, zero_count


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
            position, zero_clicks = add(position, difference)
            counter += zero_clicks
    print(counter)


if __name__ == "__main__":
    main()
