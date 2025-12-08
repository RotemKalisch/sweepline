from point import Point, is_left_turn


def test_point_equality_rounded():
    epsilon = 10**-Point.PRECISION - 10 ** -(Point.PRECISION + 9)
    point1 = Point(1.0, 2.0)
    point2 = Point(1.0 + epsilon / 2, 2.0 - epsilon / 2)
    assert point1 == point2


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
