import pytest

from point import Point
from segment import Segment


def test_segment_ordered():
    p1 = Point(1, 2)
    p2 = Point(3, 4)
    segment = Segment(p2, p1)
    assert segment.p.x == pytest.approx(p1.x)
    assert segment.q.x == pytest.approx(p2.x)


def test_intersection():
    a = Point(0, 0)
    b = Point(1, 0)
    c = Point(1, 1)
    d = Point(0, 1)

    s1 = Segment(a, c)
    s2 = Segment(b, d)

    expected_intersection = Point(0.5, 0.5)
    actual_intersection = s1.intersection(s2)
    assert actual_intersection is not None
    assert actual_intersection.x == pytest.approx(expected_intersection.x)
    assert actual_intersection.y == pytest.approx(expected_intersection.y)

    assert not Segment(a, b).intersection(Segment(c, d))


def test_segment_calc_y():
    s = Segment(Point(0, -4), Point(2, 4))
    assert s.calculate_y(1) == pytest.approx(0)
