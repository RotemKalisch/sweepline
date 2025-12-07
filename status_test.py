from ex4_helpers import Point, Segment
from status import Status

from random import shuffle


def test_status_construction():
    segments = [Segment(Point(0, 0), Point(2, i)) for i in range(5)]
    status = Status(initial_x=1)
    insertion_order = list(range(len(segments)))
    shuffle(insertion_order)
    for i in insertion_order:
        status.add(segments[i])
    assert len(status) == 5
    for i in range(len(status)):
        assert status[i] == segments[i]
        assert status.index(segments[i]) == i


def test_status_removal():
    segments = [Segment(Point(0, 0), Point(2, i)) for i in range(5)]
    status = Status(initial_x=1, segments=segments)
    removal_order = list(range(len(segments)))
    shuffle(removal_order)
    for i, j in enumerate(removal_order):
        status.remove(segments[j])
        assert len(status) == len(segments) - 1 - i
        assert status.is_ordered()
    assert len(status) == 0


def test_status_swap():
    segments = [Segment(Point(0, 0), Point(2, 2)), Segment(Point(0, 2), Point(2, 0))]
    status = Status(initial_x=0, segments=segments)
    assert list(status) == segments
    status.global_x = 1.0
    status.swap(segments[0], segments[1])
    assert list(status) == list(reversed(segments))
