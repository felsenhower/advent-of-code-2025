import sys
import numpy as np
import sympy as sp
import pulp
from pulp import PULP_CBC_CMD
from tqdm import tqdm

type IndicatorLightDiagram = tuple[bool]
type ButtonWiringSchematic = tuple[int]
type JoltageRequirements = tuple[int]
type Machine = tuple[
    IndicatorLightDiagram, list[ButtonWiringSchematics], JoltageRequirements
]


def get_linear(machine: Machine) -> tuple[sp.Matrix, sp.Matrix]:
    _, button_wiring_schematics, joltage_requirements = machine
    joltages = np.array(joltage_requirements, dtype=np.int32)
    buttons = np.zeros(
        (len(button_wiring_schematics), len(joltage_requirements)), dtype=np.int32
    )
    for i, schematic in enumerate(button_wiring_schematics):
        for j in schematic:
            buttons[i, j] = 1
    return sp.Matrix(buttons.transpose()), sp.Matrix(joltages)


def solve_linear(
    A: sp.Matrix,
    b: sp.Matrix,
) -> sp.Matrix:
    m, n = A.shape
    prob = pulp.LpProblem("int_lin_eq_min_sum", pulp.LpMinimize)
    x = [pulp.LpVariable(f"x_{i}", lowBound=0, cat="Integer") for i in range(n)]
    prob += pulp.lpSum(x)
    for row in range(m):
        prob += pulp.lpSum(int(A[row, col]) * x[col] for col in range(n)) == int(
            b[row, 0]
        )
    prob.solve(PULP_CBC_CMD(msg=0))
    status = pulp.LpStatus.get(prob.status, None)
    assert status == "Optimal"
    sol = sp.Matrix([int(round(v.varValue)) for v in x])
    return sol


def get_solution(machine: Machine) -> int:
    A, b = get_linear(machine)
    x = solve_linear(A, b)
    return sum(x)


def main():
    machines = []
    with open(sys.argv[1]) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(" ")
            indicator_light_diagram = None
            button_wiring_schematics = []
            joltage_requirements = None
            for part in parts:
                part_kind = part[0]
                part = part[1:-1]
                assert part_kind in "[({"
                if part_kind == "[":
                    indicator_light_diagram = tuple(
                        map(lambda x: True if x == "#" else False, part)
                    )
                elif part_kind == "(":
                    button_wiring_schematics.append(
                        tuple(int(x) for x in part.split(","))
                    )
                else:
                    joltage_requirements = tuple(int(x) for x in part.split(","))
            assert indicator_light_diagram is not None
            assert len(button_wiring_schematics) >= 1
            assert joltage_requirements is not None
            machines.append(
                (
                    indicator_light_diagram,
                    button_wiring_schematics,
                    joltage_requirements,
                )
            )

    result = 0
    for machine in tqdm(machines):
        solution = get_solution(machine)
        result += solution

    print("")
    print(result)


if __name__ == "__main__":
    main()
