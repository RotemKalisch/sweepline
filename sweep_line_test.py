from ex4_helpers import Point, Segment
from sweep_line import SweepLine


def test_sweep_line_example1():
    segments = [
        Segment(Point(11.3, 5.1), Point(3.2, 6.9)),
        Segment(Point(4.2, 7.1), Point(2.8, 4.9)),
    ]
    assert SweepLine(segments).intersection_points(round=2) == [
        Point(3.96, 6.73),
    ]


def test_sweep_line_example2():
    segments = [
        Segment(Point(21.2, 49.9), Point(9.6, 56.9)),
        Segment(Point(10.1, 20.1), Point(60.2, 49.8)),
        Segment(Point(69.9, 41.2), Point(60.4, 19.7)),
        Segment(Point(9.8, 40.1), Point(60.2, 70.2)),
        Segment(Point(20.9, 72.1), Point(40.5, 20.1)),
        Segment(Point(49.7, 20.3), Point(40.6, 70.2)),
    ]
    assert SweepLine(segments).intersection_points(round=2) == [
        Point(28.71, 51.39),
        Point(34.95, 34.83),
        Point(42.53, 59.64),
        Point(45.87, 41.30),
    ]


def test_sweep_line_example3():
    segments = [
        Segment(Point(0.1, 4.9), Point(6.1, 11.2)),
        Segment(Point(5.5, 8.1), Point(1.1, 6.9)),
        Segment(Point(5.1, 6.2), Point(1.9, 9.1)),
    ]

    assert SweepLine(segments).intersection_points(round=2) == [
        Point(2.32, 7.23),
        Point(3.08, 8.03),
        Point(3.58, 7.58),
    ]
