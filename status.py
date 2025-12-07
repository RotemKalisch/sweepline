from sortedcontainers import SortedList

from ex4_helpers import Segment


class Status:
    global_x: float = 0.0

    class Node:
        segment: Segment
        less_than_id: (
            int | None
        )  # Optional marker to swap two segments. Added robustness to floating point errors.

        def __init__(self, segment: Segment):
            self.segment = segment
            self.less_than_id = None

        def __repr__(self) -> str:
            return f"Node(segment={self.segment}, less_than_id={self.less_than_id})"

        def __eq__(self, other: "Status.Node") -> bool:
            return self.segment.id == other.segment.id

        def __lt__(self, other: "Status.Node") -> bool:
            if self.less_than_id == other.segment.id:
                return True
            else:
                return self.segment.calculate_y(
                    Status.global_x
                ) < other.segment.calculate_y(Status.global_x)

    bst: SortedList[Node]

    def __init__(self, initial_x: float, segments: list[Segment] = []):
        Status.global_x = initial_x
        self.bst = SortedList()
        for segment in segments:
            self.insert(segment)

    def __iter__(self):
        return (node.segment for node in self.bst)

    def __len__(self) -> int:
        return len(self.bst)

    def __getitem__(self, index: int) -> Segment:
        return self.bst[index].segment

    def __repr__(self) -> str:
        return f"Status(global_x={Status.global_x}, bst={self.bst})"

    def is_ordered(self) -> bool:  # for validations
        for i in range(1, len(self.bst)):
            if not self.bst[i - 1] < self.bst[i]:
                return False
        return True

    def insert(self, segment: Segment) -> None:
        self.bst.add(Status.Node(segment))

    def remove(self, segment: Segment) -> None:
        self.bst.remove(Status.Node(segment))

    def index(self, segment: Segment) -> int:
        return self.bst.index(Status.Node(segment))

    def swap(self, segment1, segment2) -> None:
        """
        Assuming segment1 < segment2 up until now, and from now segment1 > segment2.
        """
        if segment2.a() > segment1.a():
            raise ValueError("Segments are not in expected order for swap")
        node = Status.Node(segment2)
        self.bst.remove(node)
        node.less_than_id = segment1.id
        self.bst.add(node)
        node.less_than_id = None
