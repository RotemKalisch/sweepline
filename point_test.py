from point import Point


def test_point_equality_rounded():
    epsilon = 10**-Point.PRECISION - 10 ** -(Point.PRECISION + 9)
    point1 = Point(1.0, 2.0)
    point2 = Point(1.0 + epsilon / 2, 2.0 - epsilon / 2)
    assert point1 == point2
