from ex4_helpers import Segment, Point
from event import StartEvent, IntersectionEvent, EndEvent


RANDOM_SEGMENTS = [
    Segment(Point(1, 2), Point(3, 4)),
    Segment(Point(0, 0), Point(1, 2)),
    Segment(Point(2, 2), Point(4, -2)),
    Segment(Point(4, 6), Point(2, 0)),
]


class MockStatus(list):
    global_x: float = 0.0

    def insert(self, segment: Segment) -> None:
        self.append(segment)

    def swap(self, segment1: Segment, segment2: Segment) -> None:
        index1 = self.index(segment1)
        index2 = self.index(segment2)
        self[index1], self[index2] = self[index2], self[index1]


def test_start_event_handle():
    new_segment = Segment(Point(0, 1), Point(2, 7))
    event = StartEvent(x=0, segment=new_segment)
    status = MockStatus(RANDOM_SEGMENTS.copy())
    assert event.handle(status) == []
    assert len(status) == len(RANDOM_SEGMENTS) + 1
    assert list(status) == RANDOM_SEGMENTS + [new_segment]


def test_end_event_handle():
    removed_segment = RANDOM_SEGMENTS[1]
    event = EndEvent(x=0, segment=removed_segment)
    status = MockStatus(RANDOM_SEGMENTS.copy())
    assert event.handle(status) == []
    assert len(status) == len(RANDOM_SEGMENTS) - 1
    assert removed_segment not in status


def test_intersection_event_handle():
    segment1 = Segment(Point(0, 0), Point(4, 4))
    segment2 = Segment(Point(0, 4), Point(4, 0))
    event = IntersectionEvent(x=2, segment1=segment1, segment2=segment2)
    status = MockStatus([segment1] + RANDOM_SEGMENTS + [segment2])
    status.global_x = 2.0
    future_events = event.handle(status)
    assert list(status) == [segment2] + RANDOM_SEGMENTS + [segment1]
    assert future_events == [
        IntersectionEvent(x=3, segment1=segment1, segment2=RANDOM_SEGMENTS[-1])
    ]
