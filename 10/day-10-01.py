import sys
import random

type IndicatorLightDiagram = tuple[bool]
type ButtonWiringSchematic = tuple[int]
type JoltageRequirements = tuple[int]
type Machine = tuple[
    IndicatorLightDiagram, list[ButtonWiringSchematics], JoltageRequirements
]


def improve_solution(machine: Machine, previous_best: int | None) -> int | None:
    indicator_light_diagram, button_wiring_schematics, _ = machine
    lights_initial = [False for _ in indicator_light_diagram]
    lights_final = list(indicator_light_diagram)
    lights = lights_initial
    result = []
    result_length = 0
    while lights != lights_final:
        result_length += 1
        if previous_best is not None and previous_best <= result_length:
            return None
        button_press = random.choice(button_wiring_schematics)
        result.append(button_press)
        for i in button_press:
            lights[i] = not lights[i]
    return result_length


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

    best_solutions = [None] * len(machines)
    iteration = 0
    try:
        while True:
            for i, machine in enumerate(machines):
                solution = improve_solution(machine, best_solutions[i])
                if solution is None:
                    continue
                best_solutions[i] = solution
            result = sum(best_solutions)
            print(f"\rCurrent best solution: {result}; Iteration: {iteration}", end="")
            iteration += 1
    except KeyboardInterrupt:
        print("")


if __name__ == "__main__":
    main()
