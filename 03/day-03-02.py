import sys
from tqdm import tqdm
from pathlib import Path


def get_joltage(switches: list[int]) -> int:
    joltage = 0
    factor = 1
    for digit in reversed(switches):
        joltage += factor * digit
        factor *= 10
    return joltage


def main():
    result = 0
    num_switches = 12
    with open(sys.argv[1]) as f:
        for line in f:
            switches = []
            line = line.strip()
            num_digits = len(line)
            bank = [int(digit) for digit in line]
            for i in range(num_switches):
                end_index = num_digits - num_switches + i
                (max_pos, max_value) = max(
                    enumerate(bank[: (end_index + 1)]), key=lambda x: x[1]
                )
                bank[: (max_pos + 1)] = (max_pos + 1) * [0]
                switches.append(max_value)
            joltage = get_joltage(switches)
            result += joltage
    print(result)


if __name__ == "__main__":
    main()
