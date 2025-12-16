from point import Point
from segment import Segment
from event import StartEvent, IntersectionEvent, EndEvent


SEGMENT0 = Segment(Point(0, -6), Point(8, 18))
SEGMENT1 = Segment(Point(0, 0), Point(4, 4))
SEGMENT2 = Segment(Point(0, 4), Point(5, -1))
SEGMENT3 = Segment(Point(0, -1), Point(6, -1))

# intersections:
# 0, 1: (3, 3)
# 0, 2: (2.5, 1.5)
# 1, 2: (2, 2)
# 3, 0: (3.333, 4)
# 3, 1: (4, 4)
# 3, 2: (0, 4)


class MockStatus(list):
    x: float

    def __init__(self, initial_x: float, segments: list[Segment] = []) -> None:
        self.x = float(initial_x)
        super().__init__(segments)

    def add(self, segment: Segment) -> None:
        self.append(segment)
        self.sort(key=lambda segment: segment.calculate_y(self.x))

    def swap(self, segment1: Segment, segment2: Segment) -> None:
        index1 = self.index(segment1)
        index2 = self.index(segment2)
        self[index1], self[index2] = self[index2], self[index1]


def test_start_event_handle():
    status = MockStatus(0, [SEGMENT0])
    event = StartEvent(x=0, segment=SEGMENT1)
    assert event.handle(status) == [IntersectionEvent(3, SEGMENT0, SEGMENT1)]
    assert list(status) == [SEGMENT0, SEGMENT1]


def test_end_event_handle():
    status = MockStatus(0, [SEGMENT0, SEGMENT1, SEGMENT2])
    event = EndEvent(x=0, segment=SEGMENT1)
    assert event.handle(status) == [IntersectionEvent(2.5, SEGMENT0, SEGMENT2)]
    assert list(status) == [SEGMENT0, SEGMENT2]


def test_intersection_event_handle():
    status = MockStatus(2.5, [SEGMENT3, SEGMENT0, SEGMENT2, SEGMENT1])
    event = IntersectionEvent(x=2.5, segment1=SEGMENT0, segment2=SEGMENT2)
    future_events = event.handle(status)
    assert list(status) == [SEGMENT3, SEGMENT2, SEGMENT0, SEGMENT1]
    assert future_events == [
        IntersectionEvent(x=5, segment1=SEGMENT3, segment2=SEGMENT2),
        IntersectionEvent(x=3, segment1=SEGMENT0, segment2=SEGMENT1),
    ]
