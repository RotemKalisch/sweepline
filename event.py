from abc import abstractmethod
from enum import Enum

from ex4_helpers import Point, Segment, intersection
from status import Status


class EventType(Enum):
    """
    Represents the type of event in the sweep line algorithm.

    We prioritize start > intersection > end, so that edge cases of intersections on a start/end points are reported correctly.
    The exercise stated this shouldn't happen, but the thought counts :)
    """

    START = 1
    INTERSECTION = 2
    END = 3


class Event:
    """
    A sweep line event. Each one
    """

    x: float

    def __init__(self, x: float):
        self.x = x

    def __lt__(self, other: "Event") -> bool:
        if self.x != other.x:
            return self.x < other.x
        return self.event_type.value < other.event_type.value

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def __eq__(self, other) -> bool:
        pass

    @abstractmethod
    def handle(self, status: Status) -> list["Event"]:
        pass


class StartEvent(Event):
    event_type: EventType = EventType.START
    segment: Segment

    def __init__(self, x: float, segment: Segment):
        super().__init__(x)
        self.segment = segment

    def __repr__(self) -> str:
        return f"StartEvent(x={self.x}, segment={self.segment})"

    def __eq__(self, other) -> bool:
        assert (
            other.event_type == EventType.START_EVENT and self.segment == other.segment
        )

    def handle(self, status: Status) -> list[Event]:
        status.insert(self.segment)
        return []


class IntersectionEvent(Event):
    event_type: EventType = EventType.INTERSECTION
    segment1: Segment
    segment2: Segment
    intersection_point: Point

    def __init__(self, x: float, segment1: Segment, segment2: Segment):
        super().__init__(x)
        self.segment1 = segment1  # coming from above
        self.segment2 = segment2  # coming from below

    def __repr__(self) -> str:
        return f"IntersectionEvent(x={self.x}, segment1={self.segment1}, segment2={self.segment2})"

    def __eq__(self, other) -> bool:
        return (
            other.event_type == EventType.INTERSECTION
            and self.segment1 == other.segment1
            and self.segment2 == other.segment2
        )

    def future_intersection(
        self, current_x: float, top_segment, bottom_segment
    ) -> Event | None:
        intersection_point = intersection(top_segment, bottom_segment)
        if intersection_point is not None and intersection_point.x > current_x:
            return IntersectionEvent(
                x=intersection_point.x,
                segment1=top_segment,
                segment2=bottom_segment,
            )
        else:
            return None

    def handle(self, status: Status) -> list[Event]:
        status.swap(self.segment1, self.segment2)
        future_events = []
        lower_index = status.index(self.segment1)
        if lower_index > 0:
            candidate = self.future_intersection(
                status.global_x, self.segment1, status[lower_index - 1]
            )
            if candidate is not None:
                future_events.append(candidate)
        upper_index = status.index(self.segment2)
        if upper_index < len(status) - 1:
            candidate = self.future_intersection(
                status.global_x, status[upper_index + 1], self.segment2
            )
            if candidate is not None:
                future_events.append(candidate)
        return future_events


class EndEvent(Event):
    event_type: EventType = EventType.END
    segment: Segment

    def __init__(self, x: float, segment: Segment):
        super().__init__(x)
        self.event_type = EventType.END
        self.segment = segment

    def __repr__(self) -> str:
        return f"EndEvent(x={self.x}, segment={self.segment})"

    def __eq__(self, other) -> bool:
        return other.event_type == EventType.END and self.segment == other.segment

    def handle(self, status: Status) -> list[Event]:
        status.remove(self.segment)
        return []
