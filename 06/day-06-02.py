import sys
from pathlib import Path
from math import prod


def solve_problem(problem: tuple[str, list[int]]) -> int:
    operator, operands = problem
    match operator:
        case "*":
            return prod(operands)
        case "+":
            return sum(operands)
        case _:
            assert False, f'Unexpected operator "{operator}".'


def main():
    lines = []
    with open(sys.argv[1]) as f:
        for line in f:
            if not line.strip():
                continue
            line = line[:-1]
            lines.append(line)
    operators = lines[-1].strip().split()
    lines = [(line[::-1] + " ") for line in reversed(lines[:-1])]
    line_len = len(lines[0])
    num_lines = len(lines)
    problems = []
    operands = []
    for i in range(line_len):
        is_empty_column = set(line[i] for line in lines) == {" "}
        if is_empty_column:
            operator = operators.pop()
            problems.append((operator, operands))
            operands = []
            continue
        digits = []
        for j in range(num_lines):
            digit = lines[j][i]
            if digit != " ":
                digits.append(int(digit))
        operand = 0
        factor = 1
        for digit in digits:
            operand += factor * digit
            factor *= 10
        operands.append(operand)
    result = 0
    for problem in problems:
        solution = solve_problem(problem)
        result += solution
    print(result)


if __name__ == "__main__":
    main()
