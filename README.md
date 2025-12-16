# sweepline

This is my implementation of the sweep line algorithm, as part of "Computational Geometry" course (num. 236719) at the Technion.
The sweep line algorithm counts and reports all intersection points given a set of segments.

The `Point` and `Segment` classes are the ones that were given to us in the supplementary python module, and the rest were written by me.
For the BST I used `sortedcontainers.SortedList`.

The entire codebase is tested, run the tests using `pytest`.

Key implementation assumptions (from the exercise itself):
1. No two segments intersect in more than one point.
2. No three segments (or more) intersect in one point.
3. No numerical errors should occur when using floating point numbers. That is, segment endpoints are well separated, as well as intersections of segments, and events
of the algorithm are separated enough along the x axis.

