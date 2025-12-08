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

    def intersection(self, other: "Segment") -> Point | None:
        if (
            is_left_turn(self.p, self.q, other.p)
            != is_left_turn(self.p, self.q, other.q)
        ) and (
            is_left_turn(other.p, other.q, self.p)
            != is_left_turn(other.p, other.q, self.q)
        ):
            a1 = self.a()
            a2 = other.a()

            b1 = self.b()
            b2 = other.b()

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

            if min(self.p.x, self.q.x) <= x and x <= max(self.p.x, self.q.x):
                return Point(x, y)
        return None


def is_left_turn(a: Point, b: Point, c: Point) -> bool:
    x1 = a.x
    x2 = b.x
    x3 = c.x
    y1 = a.y
    y2 = b.y
    y3 = c.y
    return ((x1 * (y2 - y3)) + (x2 * (y3 - y1)) + (x3 * (y1 - y2))) > 0
