""" convexhull.py

Calculate the convex hull of a set of n 2D points in O(n log n) time.
Taken from Berg et al., Computational Geometry, Springer-Verlag, 1997.
Emits output as EPS file.

When run from the command line, it generates a random set of points
inside a square of given length and finds the convex hull for those,
emitting the result as an EPS file.
Usage:
    convexhull.py <numPoints> <squareLength> <outFile>

Dinu C. Gherman
"""
# helpers


def _myDet(p, q, r):
    """ Calculate determinant of a special matrix with three 2D points.

    The sign, - or +, determines the side (right or left, respectively) on which
    the point r lies when measured against a directed vector from p to q.
    """
    # We use Sarrus' Rule to calculate the determinant
    # (could also use the Numeric package...)
    sum1 = q[0] * r[1] + p[0] * q[1] + r[0] * p[1]
    sum2 = q[0] * p[1] + r[0] * q[1] + p[0] * r[1]
    return sum1 - sum2


def _isRightTurn((p, q, r)):
    "Do the vectors pq:qr form a right turn, or not?"
    assert p != q and q != r and p != r
    return _myDet(p, q, r) < 0


def _isPointInPolygon(r, P):
    "Is point r inside a given polygon P?"
    # We assume that the polygon is a list of points, listed clockwise
    for i in xrange(len(P) - 1):
        p, q = P[i], P[i + 1]
        if not _isRightTurn((p, q, r)):
            return 0  # Out!
    return 1  # It's within!


def convexHull(P):
    "Calculate the convex hull of a set of points."

    # Get a local list copy of the points and sort them lexically
    points = map(None, P)
    points.sort()

    # Build upper half of the hull
    upper = [points[0], points[1]]
    for p in points[2:]:
        upper.append(p)
        while len(upper) > 2 and not _isRightTurn(upper[-3:]):
            del upper[-2]

    # Build lower half of the hull
    points.reverse()
    lower = [points[0], points[1]]
    for p in points[2:]:
        lower.append(p)
        while len(lower) > 2 and not _isRightTurn(lower[-3:]):
            del lower[-2]

    # Remove duplicates
    del lower[0]
    del lower[-1]

    # Concatenate both halves and return
    return tuple(upper + lower)
