import random

from point import Point
from segment import Segment
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


def test_grid():
    N = 100
    segments = [Segment(Point(-N - i, i), Point(N + i, i)) for i in range(N)]

    assert [] == SweepLine(segments).intersection_points(round=2)

    expected_points = []
    for j in range(1, 10):
        expected_points += [Point(i / (2 * N) + (1 + 4 * j) / 2, i) for i in range(N)]
        new_segments = [
            Segment(Point(2 * i, -N), Point(2 * i + 1, N)) for i in range(1, j + 1)
        ]
        assert (
            expected_points == SweepLine(segments + new_segments).intersection_points()
        )


def test_empty_status():
    segments = [
        Segment(Point(0, 0), Point(1, 1)),
        Segment(Point(5, 5), Point(10, 10)),
        Segment(Point(10, 5), Point(5, 10)),
        Segment(Point(15, 15), Point(16, 16)),
    ]
    assert SweepLine(segments).intersection_points(round=2) == [Point(7.5, 7.5)]


def test_intersection_count_equivalence():
    MAX_SEGMENTS = 100
    random.seed(236719)
    segments = [
        Segment(
            Point(i, -random.random() * MAX_SEGMENTS**2),
            Point(MAX_SEGMENTS**2 + i, random.random() * MAX_SEGMENTS**2),
        )
        for i in range(MAX_SEGMENTS)
    ]

    amount_reported = len(SweepLine(segments).intersection_points())
    amount_counted = SweepLine(segments, report=False).intersection_points()
    assert amount_reported == amount_counted


def test_stress_test():
    MAX_SEGMENTS = 1000
    random.seed(236719)
    segments = [
        Segment(
            Point(i, -random.random() * MAX_SEGMENTS**2),
            Point(MAX_SEGMENTS**2 + i, random.random() * MAX_SEGMENTS**2),
        )
        for i in range(MAX_SEGMENTS)
    ]

    SweepLine(segments).intersection_points()  # Just make sure it runs without error
