class Point:
    PRECISION: int = 5

    x: float
    y: float

    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"

    def __eq__(self, other: "Point") -> bool:
        """
        For testing, we assume all unique points are 1e-3 away from each other.
        """
        return (
            self.rounded().x == other.rounded().x
            and self.rounded().y == other.rounded().y
        )

    def rounded(self, precision=None) -> "Point":
        precision = precision or Point.PRECISION
        return Point(
            round(self.x, precision),
            round(self.y, precision),
        )
