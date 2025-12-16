from sortedcontainers import SortedList

from point import Point
from segment import Segment
from status import Status
from event import Event, StartEvent, IntersectionEvent, EndEvent


class SweepLine:
    segments: list[Segment]
    events: SortedList[Event]
    status: Status

    def __init__(self, segments: list[Segment]):
        self.segments = segments
        self.events = SortedList([])
        for i in range(len(self.segments)):
            segment = self.segments[i]
            self.events.add(StartEvent(x=segment.p.x, segment=segment))
            self.events.add(EndEvent(x=segment.q.x, segment=segment))
        self.status = Status(self.events[0].x)

    def intersection_points(self, round: int | None = None) -> list[Point]:
        retval = []
        while len(self.events) > 0:
            event = self.events.pop(0)
            new_events = event.handle(self.status)
            for new_event in new_events:
                if new_event not in self.events:
                    self.events.add(new_event)
            if isinstance(event, IntersectionEvent):
                intersection_point = event.intersection_point
                if intersection_point is None:
                    raise ValueError("Intersection event with no intersection!")
                retval.append(intersection_point)
        if round is not None:
            retval = [p.rounded(round) for p in retval]
        return retval
