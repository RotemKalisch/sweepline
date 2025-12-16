import sys

from parser import parse_problems
from sweep_line import SweepLine


def main():
    if len(sys.argv) != 2:
        raise TypeError("Only expected argument is input file path!")

    with open(sys.argv[1], "r") as f:
        problems = parse_problems(f.readlines())

    results = [
        SweepLine(problem, report=False).intersection_points() for problem in problems
    ]
    for result in results:
        print(result)


if __name__ == "__main__":
    main()
