from abc import abstractmethod
from enum import Enum

from point import Point
from segment import Segment
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

    def future_intersection(
        self, current_x: float, status: Status, bottom_index: int
    ) -> "Event":
        bottom_segment = status[bottom_index]
        top_segment = status[bottom_index + 1]
        intersection_point = bottom_segment.intersection(top_segment)
        if intersection_point is not None and intersection_point.x > current_x:
            return IntersectionEvent(
                x=intersection_point.x,
                segment1=bottom_segment,
                segment2=top_segment,
            )
        else:
            return None


class StartEvent(Event):
    event_type: EventType = EventType.START
    segment: Segment

    def __init__(self, x: float, segment: Segment):
        super().__init__(x)
        self.segment = segment

    def __repr__(self) -> str:
        return f"StartEvent(x={self.x}, segment={self.segment})"

    def __eq__(self, other) -> bool:
        return other.event_type == EventType.START and self.segment == other.segment

    def handle(self, status: Status) -> list[Event]:
        status.x = self.x + Point.EPSILON  # to avoid rounding issues
        future_events = []
        status.add(self.segment)
        index = status.index(self.segment)
        if index > 0:
            candidate = self.future_intersection(status.x, status, index - 1)
            if candidate is not None:
                future_events.append(candidate)
        if index < len(status) - 1:
            candidate = self.future_intersection(status.x, status, index)
            if candidate is not None:
                future_events.append(candidate)
        return future_events


class IntersectionEvent(Event):
    event_type: EventType = EventType.INTERSECTION
    segment1: Segment
    segment2: Segment
    intersection_point: Point

    def __init__(self, x: float, segment1: Segment, segment2: Segment):
        super().__init__(x)
        self.segment1 = segment1  # coming from below
        self.segment2 = segment2  # coming from above
        self.intersection_point = segment1.intersection(segment2)

    def __repr__(self) -> str:
        return f"IntersectionEvent(x={self.x}, segment1={self.segment1}, segment2={self.segment2})"

    def __eq__(self, other) -> bool:
        return (
            other.event_type == EventType.INTERSECTION
            and abs(self.x - other.x) < Point.EPSILON  # sanity
            and self.segment1 == other.segment1
            and self.segment2 == other.segment2
        )

    def handle(self, status: Status) -> list[Event]:
        status.x = self.x - Point.EPSILON  # to avoid rounding issues
        if status.index(self.segment1) > status.index(self.segment2):
            raise ValueError("Segments not swapped correctly in status")
        lower_index = status.index(self.segment1)
        status.swap(self.segment1, self.segment2)
        status.x = self.x + Point.EPSILON  # to avoid rounding issues
        future_events = []
        if lower_index > 0:
            candidate = self.future_intersection(status.x, status, lower_index - 1)
            if candidate is not None:
                future_events.append(candidate)
        upper_index = lower_index + 1
        if upper_index < len(status) - 1:
            candidate = self.future_intersection(status.x, status, upper_index)
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
        status.x = self.x - Point.EPSILON  # to avoid rounding issues
        future_events = []
        index = status.index(self.segment)
        status.remove(self.segment)
        if index > 0 and index < len(status):
            candidate = self.future_intersection(status.x, status, index - 1)
            if candidate is not None:
                future_events.append(candidate)
        return future_events
