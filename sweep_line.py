from sortedcontainers import SortedList

from ex4_helpers import Point, Segment, intersection
from status import Status
from event import Event, StartEvent, IntersectionEvent, EndEvent


class SweepLine:
    segments: list[Segment]
    events: SortedList[Event]
    status: Status

    def __init__(self, segments: list[Segment]):
        self.segments = segments
        self.event_heap = []
        for i in range(len(self.segments)):
            segment = self.segments[i]
            self.events.insert(StartEvent(x=segment.p.x, segment=segment))
            self.events.insert(EndEvent(x=segment.q.x, segment=segment))
        self.status = Status(self.event_heap[0].x)

    def intersection_points(self) -> list[Point]:
        retval = []
        while len(self.event_heap) > 0:
            event = self.event_heap.pop(0)
            Status.global_x = event.x
            new_events = event.handle(self.status)
            for event in new_events:
                self.event_heap.insert(event)
            if isinstance(event, IntersectionEvent):
                intersection_point = intersection(event.segment1, event.segment2)
                if intersection_point is None:
                    raise ValueError("Intersection event with no intersection!")
                retval.append(intersection_point)
        return retval
