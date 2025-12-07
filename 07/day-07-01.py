import sys


def main():
    num_splits = 0
    with open(sys.argv[1]) as f:
        beam_positions = None
        for i, line in enumerate(f):
            line = line.strip()
            if i == 0:
                start_pos = line.find("S")
                beam_positions = {start_pos}
                continue
            splitter_positions = [j for j, x in enumerate(line) if x == "^"]
            if not splitter_positions:
                continue
            assert beam_positions is not None
            new_beam_positions = set()
            for splitter_pos in splitter_positions:
                if splitter_pos in beam_positions:
                    num_splits += 1
                    beam_positions.remove(splitter_pos)
                    beam_positions.add(splitter_pos - 1)
                    beam_positions.add(splitter_pos + 1)
        print(num_splits)


if __name__ == "__main__":
    main()
