from point import Point
from segment import Segment


def parse_problem(words: list[str], index: int) -> list[Segment]:
    m = int(words[index])
    index += 1
    segments = []

    for i in range(m):
        x1, y1, x2, y2 = map(float, words[index + 4 * i : index + 4 * (i + 1)])
        segments.append(Segment(Point(x1, y1), Point(x2, y2)))

    return segments


def parse_problems(words: list[str]) -> list[list[Segment]]:
    if "-1" != words[-1]:
        raise ValueError("Input file must end with -1!")

    n = int(words[0])
    problems = []

    index = 1
    for _ in range(n):
        problem = parse_problem(words, index)
        index += 1 + len(problem) * 4
        problems.append(problem)

    if index != len(words) - 1:
        raise ValueError("Line index mismatch after parsing all problems!")

    return problems
