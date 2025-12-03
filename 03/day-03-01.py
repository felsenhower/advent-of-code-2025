import sys


def main():
    result = 0
    with open(sys.argv[1]) as f:
        for line in f:
            line = line.strip()
            num_digits = len(line)
            bank = [int(digit) for digit in line]
            (max_pos, max_value) = max(enumerate(bank), key=lambda x: (x[1], -x[0]))
            if max_pos < num_digits - 1:
                bank[: (max_pos + 1)] = (max_pos + 1) * [0]
                max_value2 = max(bank)
                joltage = max_value * 10 + max_value2
                result += joltage
            else:
                bank[max_pos] = 0
                max_value2 = max(bank)
                joltage = max_value2 * 10 + max_value
                result += joltage
    print(result)


if __name__ == "__main__":
    main()
