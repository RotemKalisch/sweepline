from sortedcontainers import SortedList

from point import Point
from segment import Segment
from status import Status
from event import Event, StartEvent, IntersectionEvent, EndEvent


class SweepLine:
    segments: list[Segment]
    events: SortedList[Event]
    status: Status
    count: bool

    def __init__(self, segments: list[Segment], report: bool = True):
        self.segments = segments
        self.events = SortedList([])
        for i in range(len(self.segments)):
            segment = self.segments[i]
            self.events.add(StartEvent(x=segment.p.x, segment=segment))
            self.events.add(EndEvent(x=segment.q.x, segment=segment))
        self.status = Status(self.events[0].x)
        self.report = report

    def intersection_points(self, round: int | None = None) -> list[Point] | int:
        retval = [] if self.report else 0
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
                if self.report:
                    retval.append(intersection_point)
                else:
                    retval += 1
        if self.report and round is not None:
            retval = [p.rounded(round) for p in retval]
        return retval
