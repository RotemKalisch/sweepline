import heapq

from ex4_helpers import Point, Segment, intersection
from status import Status
from event import StartEvent, IntersectionEvent, EndEvent


class Sweepline:
    segments: list[Segment]
    event_heap: list[Point]
    status: Status
    swap: None

    def __init__(self, segments: list[Segment]):
        self.segments = segments
        self.event_heap = []
        for i in range(len(self.segments)):
            heapq.heappush(
                self.event_heap,
                StartEvent(x=self.segments[i].p.x),
            )
            heapq.heappush(
                self.event_heap,
                EndEvent(x=self.segments[i].q.x),
            )
        self.status = Status(self.event_heap[0].x)

    def intersection_points(self) -> list[Point]:
        retval = []
        while len(self.event_heap) > 0:
            event = heapq.heappop(self.event_heap)
            self.status.global_x = event.x
            new_events = event.handle()
            for event in new_events:
                heapq.heappush(self.event_heap, event)
            if isinstance(event, IntersectionEvent):
                intersection_point = intersection(event.segment1, event.segment2)
                if intersection_point is None:
                    raise ValueError("Intersection event with no intersection!")
                retval.append(intersection_point)
        return retval
