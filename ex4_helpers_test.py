import pytest

from point import Point
from ex4_helpers import Segment, is_left_turn, intersection, intersects


def test_segment_ordered():
    p1 = Point(1, 2)
    p2 = Point(3, 4)
    segment = Segment(p2, p1)
    assert segment.p.x == pytest.approx(p1.x)
    assert segment.q.x == pytest.approx(p2.x)


def test_is_left_turn():
    a = Point(0, 0)
    b = Point(1, 0)
    c = Point(1, 1)
    d = Point(0, 1)

    assert is_left_turn(a, b, c)
    assert is_left_turn(b, c, d)
    assert is_left_turn(c, d, a)
    assert is_left_turn(d, a, b)
    assert not is_left_turn(d, c, b)
    assert not is_left_turn(c, b, a)
    assert not is_left_turn(b, a, d)
    assert not is_left_turn(a, d, c)


def test_intersection():
    a = Point(0, 0)
    b = Point(1, 0)
    c = Point(1, 1)
    d = Point(0, 1)

    s1 = Segment(a, c)
    s2 = Segment(b, d)

    expected_intersection = Point(0.5, 0.5)
    actual_intersection = intersection(s1, s2)
    assert actual_intersection is not None
    assert actual_intersection.x == pytest.approx(expected_intersection.x)
    assert actual_intersection.y == pytest.approx(expected_intersection.y)

    assert intersects(s1, s2)
    assert intersects(s2, s1)

    assert not intersects(Segment(a, b), Segment(c, d))


def test_segment_calc_y():
    s = Segment(Point(0, -4), Point(2, 4))
    assert s.calculate_y(1) == pytest.approx(0)
