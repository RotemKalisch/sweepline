from ex4_helpers import Point, Segment
from sweep_line import SweepLine

from hw4 import parse_problems


def test_parser_example():
    input_path = "./input.txt"
    with open(input_path, "r") as f:
        problems = parse_problems(f.readlines())

    assert str(problems) == str(
        [
            [
                Segment(Point(3.2, 6.9), Point(11.3, 5.1)),
                Segment(Point(2.8, 4.9), Point(4.2, 7.1)),
            ],
            [
                Segment(Point(9.6, 59.6), Point(21.2, 49.9)),
                Segment(Point(10.1, 20.1), Point(60.2, 49.8)),
                Segment(Point(60.4, 19.7), Point(69.9, 41.2)),
                Segment(Point(9.8, 40.1), Point(60.2, 70.2)),
                Segment(Point(20.9, 72.1), Point(40.5, 20.1)),
                Segment(Point(40.6, 70.2), Point(49.7, 20.3)),
            ],
            [
                Segment(Point(0.1, 4.9), Point(6.1, 11.2)),
                Segment(Point(1.1, 6.9), Point(5.5, 8.1)),
                Segment(Point(1.9, 9.1), Point(5.1, 6.2)),
            ],
        ]
    )
