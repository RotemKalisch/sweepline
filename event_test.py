from ex4_helpers import Segment, Point
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
    global_x: float = 0.0

    def insert(self, segment: Segment) -> None:
        self.append(segment)
        self.sort(key=lambda segment: segment.calculate_y(MockStatus.global_x))

    def swap(self, segment1: Segment, segment2: Segment) -> None:
        index1 = self.index(segment1)
        index2 = self.index(segment2)
        self[index1], self[index2] = self[index2], self[index1]


def test_start_event_handle():
    MockStatus.global_x = 0
    event = StartEvent(x=0, segment=SEGMENT1)
    status = MockStatus([SEGMENT0])
    assert event.handle(status) == [IntersectionEvent(3, SEGMENT0, SEGMENT1)]
    assert list(status) == [SEGMENT0, SEGMENT1]


def test_end_event_handle():
    MockStatus.global_x = 0
    event = EndEvent(x=0, segment=SEGMENT1)
    status = MockStatus([SEGMENT0, SEGMENT1, SEGMENT2])
    assert event.handle(status) == [IntersectionEvent(2.5, SEGMENT0, SEGMENT2)]
    assert list(status) == [SEGMENT0, SEGMENT2]


def test_intersection_event_handle():
    MockStatus.global_x = 2.5
    event = IntersectionEvent(x=2.5, segment1=SEGMENT0, segment2=SEGMENT2)
    status = MockStatus([SEGMENT3, SEGMENT0, SEGMENT2, SEGMENT1])
    future_events = event.handle(status)
    assert list(status) == [SEGMENT3, SEGMENT2, SEGMENT0, SEGMENT1]
    assert future_events == [
        IntersectionEvent(x=5, segment1=SEGMENT3, segment2=SEGMENT2),
        IntersectionEvent(x=3, segment1=SEGMENT0, segment2=SEGMENT1),
    ]
