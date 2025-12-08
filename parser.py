from point import Point
from ex4_helpers import Segment


def parse_problem(lines: list[str], line_index: int) -> list[Segment]:
    m = int(lines[line_index].strip())
    segments = []

    for i in range(m):
        x1, y1, x2, y2 = map(float, lines[line_index + 1 + i].strip().split())
        segments.append(Segment(Point(x1, y1), Point(x2, y2)))

    return segments


def parse_problems(lines: list[str]) -> list[list[Segment]]:
    if "-1" != lines[-1].strip():
        raise ValueError("Input file must end with -1!")

    n = int(lines[0].strip())
    problems = []

    line_index = 1
    for _ in range(n):
        problem = parse_problem(lines, line_index)
        line_index += 1 + len(problem)
        problems.append(problem)

    if line_index != len(lines) - 1:
        raise ValueError("Line index mismatch after parsing all problems!")

    return problems
