from abc import abstractclass, abstracmethod
from enum import Enum
import heapq

from sortedcontainers import SortedList

from ex4_helpers import Point, Segment, intersection


class SweeplineStatus:
    global_x: float = 0.0

    class StatusNode:
        segment: Segment
        less_than_id: (
            int | None
        )  # Optional marker to swap two segments. Added robustness to floating point errors.

        def __init__(self, segment: Segment):
            self.segment = segment

        def __eq__(self, other: "SweeplineStatus.StatusNode") -> bool:
            return self.segment.id == other.segment.id

        def __lt__(self, other: "SweeplineStatus.StatusNode") -> bool:
            if self.sweepline_status.less_than_id == other.id:
                return True
            else:
                return self.segment.calculate_y(
                    SweeplineStatus.global_x
                ) < other.segment.calculate_y(SweeplineStatus.global_x)

    status: SortedList[StatusNode]

    def __init__(self, initial_x: float):
        SweeplineStatus.global_x = initial_x

    def insert(self, segment: Segment) -> None:
        self.status.add(SweeplineStatus.StatusNode(segment))

    def remove(self, segment: Segment) -> None:
        self.status.remove(SweeplineStatus.StatusNode(segment))

    def index(self, segment: Segment) -> int:
        return self.status.bisect_left(SweeplineStatus.StatusNode(segment))

    def swap(self, segment1, segment2) -> None:
        """
        Assuming segment1 > segment2 up until now, and from now segmetn1 < segment2.
        """
        if segment2.a() < segment1.a():
            raise ValueError("Segments are not in expected order for swap")
        node = SweeplineStatus.StatusNode(segment1)
        self.status.remove(node)
        node.less_than_id = segment2.id
        self.status.add(node)
        node.less_than_id = None


class EventType(Enum):
    """
    Represents the type of event in the sweep line algorithm.

    We prioritize start > intersection > end, so that edge cases of intersections on a start/end points are reported correctly.
    The exercise stated this shouldn't happen, but the thought counts :)
    """

    START = 1
    INTERSECTION = 2
    END = 3


@abstractclass
class SweeplineEvent:
    """
    A sweep line event. Each one
    """

    x: float

    def __init__(self, x: float):
        self.x = x

    def __le__(self, other: "SweeplineEvent") -> bool:
        if self.x != other.x:
            return self.x < other.x
        return self.event_type.value < other.event_type.value

    @abstracmethod
    def handle(self) -> list["SweeplineEvent"]:
        pass


class StartEvent(SweeplineEvent):
    event_type: EventType = EventType.START
    segment: Segment

    def __init__(self, x: float, segment: Segment):
        super().__init__(x)
        self.segment = segment

    def handle(self, status: SweeplineStatus) -> list[SweeplineEvent]:
        status.insert(self.segment)
        return []


class IntersectionEvent(SweeplineEvent):
    event_type: EventType = EventType.INTERSECTION
    segment1: Segment
    segment2: Segment
    intersection_point: Point

    def __init__(self, x: float, segment1: Segment, segment2: Segment):
        super().__init__(x)
        self.segment1 = segment1  # coming from above
        self.segment2 = segment2  # coming from below

    def future_intersection(self, top_segment, bottom_segment) -> SweeplineEvent | None:
        intersection_point = intersection(top_segment, bottom_segment)
        if (
            intersection_point is not None
            and intersection_point.x > self.sweepline.current_x
        ):
            return IntersectionEvent(
                sweepline=self.sweepline,
                x=intersection_point.x,
                segment1=top_segment,
                segment2=bottom_segment,
            )
        else:
            return None

    def handle(self, status: SweeplineStatus) -> list[SweeplineEvent]:
        future_events = []
        status.swap(self.segment1, self.segment2)
        lower_index = status.index(self.segment1)
        if lower_index > 0:
            candidate_segment_index = self.sweepline.status[
                lower_index - 1
            ].segment_index
            candidate = self.future_intersection(
                self.segment1_index, candidate_segment_index
            )
            if candidate is not None:
                future_events.append(candidate)
        upper_index = self.sweepline.status.index(self.segment2)
        if upper_index < len(self.sweepline.status) - 1:
            candidate_segment_index = self.sweepline.status[
                upper_index + 1
            ].segment_index
            candidate = self.future_intersection(
                candidate_segment_index, self.segment2_index
            )
            if candidate is not None:
                future_events.append(candidate)
        return future_events


class EndEvent(SweeplineEvent):
    event_type: EventType = EventType.END
    segment_index: int

    def __init__(self, sweepline: "Sweepline", x: float, segment_index: int):
        super().__init__(x, sweepline)
        self.event_type = EventType.END
        self.segment_index = segment_index

    def handle(self) -> list[SweeplineEvent]:
        self.sweepline.status.remove(self.segment_index)
        return []


class Sweepline:
    segments: list[Segment]
    event_heap: list[Point]
    status: SweeplineStatus
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
        self.status = SweeplineStatus(self.event_heap[0].x)

    def intersection_points(self) -> list[Point]:
        retval = []
        while len(self.event_heap) > 0:
            event = heapq.heappop(self.event_heap)
            new_events = event.handle()
            for event in new_events:
                heapq.heappush(self.event_heap, event)
            if isinstance(event, IntersectionEvent):
                intersection_point = intersection(event.segment1, event.segment2)
                if intersection_point is None:
                    raise ValueError("Intersection event with no intersection!")
                retval.append(intersection_point)
        return retval
