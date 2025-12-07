import sys


def main():
    with open(sys.argv[1]) as f:
        beam_numbers = None
        for i, line in enumerate(f):
            line = line.strip()
            if i == 0:
                start_pos = line.find("S")
                beam_numbers = len(line) * [0]
                beam_numbers[start_pos] = 1
                continue
            splitter_positions = {j for j, x in enumerate(line) if x == "^"}
            for j in range(len(beam_numbers)):
                num_beams = beam_numbers[j]
                if num_beams == 0:
                    continue
                if j in splitter_positions:
                    beam_numbers[j - 1] += num_beams
                    beam_numbers[j + 1] += num_beams
                    beam_numbers[j] = 0
    print(sum(beam_numbers))


if __name__ == "__main__":
    main()
