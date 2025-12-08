from itertools import count

from point import Point


class Segment:
    id_generator = count()

    id: int
    p: Point
    q: Point

    def __init__(self, p: Point, q: Point):
        self.id = next(Segment.id_generator)
        if p.x > q.x:
            p, q = q, p
        self.p = p
        self.q = q

    # line: y = ax + b. it is guaranteed that the line is not vertical (a is finite)
    def a(self) -> float:
        return (self.p.y - self.q.y) / (self.p.x - self.q.x)

    def b(self) -> float:
        return self.p.y - (self.a() * self.p.x)

    def calculate_y(self, x: Point) -> float:
        if x < self.p.x or x > self.q.x:
            raise ValueError("calculate_y out of bounds")
        return self.a() * x + self.b()

    def __eq__(self, other: "Segment") -> bool:
        return (
            self.id == other.id
        )  # We never copy segments, this is for validations only.

    def __repr__(self) -> str:
        return f"Segment({self.p}, {self.q})"


def is_left_turn(a: Point, b: Point, c: Point) -> bool:
    x1 = a.x
    x2 = b.x
    x3 = c.x
    y1 = a.y
    y2 = b.y
    y3 = c.y
    return ((x1 * (y2 - y3)) + (x2 * (y3 - y1)) + (x3 * (y1 - y2))) > 0


def intersection(s1: Segment, s2: Segment) -> Point | None:
    if (is_left_turn(s1.p, s1.q, s2.p) != is_left_turn(s1.p, s1.q, s2.q)) and (
        is_left_turn(s2.p, s2.q, s1.p) != is_left_turn(s2.p, s2.q, s1.q)
    ):
        a1 = s1.a()
        a2 = s2.a()

        b1 = s1.b()
        b2 = s2.b()

        # commutation consistency: sort by a (then by b)
        if a1 > a2 or (a1 == a2 and b1 > b2):
            a1, a2 = a2, a1
            b1, b2 = b2, b1

        # a1 x + b1 = y
        # a2 x + b2 = y
        # (a1 - a2)x + (b1-b2) = 0
        # x = (b2-b1)/(a1-a2)
        x = (b2 - b1) / (a1 - a2)
        y = a1 * x + b1

        if min(s1.p.x, s1.q.x) <= x and x <= max(s1.p.x, s1.q.x):
            return Point(x, y)
    return None


def intersects(s1: Segment, s2: Segment) -> bool:
    return intersection(s1, s2) is not None
