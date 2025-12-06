import sys
from pathlib import Path
from math import prod


def solve_problem(problem: list[str]) -> int:
    operands = [int(x) for x in problem[:-1]]
    operator = problem[-1]
    match operator:
        case "*":
            return prod(operands)
        case "+":
            return sum(operands)
        case _:
            assert False, f'Unexpected operator "{operator}".'
    print(operands, operator)


def main():
    puzzle = [
        line.strip().split()
        for line in Path(sys.argv[1]).read_text().strip().split("\n")
    ]
    problems = list(map(list, zip(*puzzle)))
    result = 0
    for problem in problems:
        solution = solve_problem(problem)
        result += solution
    print(result)


if __name__ == "__main__":
    main()
