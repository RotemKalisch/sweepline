from ex4_helpers import Point, Segment
from sweep_line import SweepLine


def test_sweepline_example1():
    segments = [
        Segment(Point(11.3, 5.1), Point(3.2, 6.9)),
        Segment(Point(4.2, 7.1), Point(2.8, 4.9)),
    ]
    assert SweepLine(segments).intersection_points() == [Point(4.0, 6.2)]
