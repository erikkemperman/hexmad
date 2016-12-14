
"""
Given a latitude LAT and longitude LON and a radius RAD, construct a grid of
(approximately) hexagonal cells.

The radius RAD is the distance from a cell's center to each of its vertices;
the distance between a cell's center and its edges is RAD * sqrt(3)/2.

The cells are indexed from the origin (index X = 0) outward, counter-clockwise
along "rings".

The 1st ring has 6 cells: X = 1, ..., X = 6
The 2nd ring has 12 cells: X = 7, ..., X = 18
...
The Rth ring has 6R cells: X = 3R(R-1) + 1, ..., X = 3R(R+1)

Let's divide each ring in 6 segments, so each segment in the Rth ring has R cells.

Let's denote the index of the first cell, in the first segment, in the Rth ring: X(R,0,0), for R in (0, ...).
Let's denote the index of the first cell, in the Sth segment, in the Rth ring: X(R,S,0), for S in [0,6).
Let's denote the index of the Tth cell, in the Sth segment, in the Rth ring: X(R,S,T), for T in [0,R).

Now, given an arbitrary X > 0, we can compute R, S, and T as follows:

R  =  floor( 1/2 + srqt( 1/3 * (X-1) + 1/4 ) )
S  =  floor( (X-1)/R ) - 3(R-1)
T  =  (X - 1) % R

"""

from math import floor
from math import sqrt


def assert_index(x: int, r: int = -1, exception: bool = True):
    """
    TODO
    :param x:
    :param r:
    :param exception:
    :return:
    """
    if x < 0 or (r == 0 and x != 0) or (r > 0 and (x < 3 * r * (r - 1) + 1 or x > 3 * r * (r + 1))):
        if exception:
            raise ValueError('Illegal index: %s' % ('%d' % x if r < 0 else '%d for R=%d' % (x, r)))
        return False
    return True


def assert_polar(r: int, s: int = 0, t: int = 0, exception: bool = True):
    """
    TODO
    :param r:
    :param s:
    :param t:
    :param exception:
    :return:
    """
    if r < 0 or (r == 0 and (s != 0 or t != 0)) or (r > 0 and (s < 0 or s >= 6 or t < 0 or t >= r)):
        if exception:
            raise ValueError('Illegal co-ordinates: (%d, %d, %d)' % (r, s, t))
        return False
    return True


def index(r: int, s: int = 0, t: int = 0):
    """
    Given R, S and T co-ordinates, find the index X of the hexagonal cell in the array
    :param r:
    :param s:
    :param t:
    :return:
    """
    return 0 if r == 0 else r * (3 * (r - 1) + s) + t + 1


def ring(x: int):
    return 0 if x == 0 else floor(0.5 + sqrt((x - 1) / 3 + 0.25))


def segment(x: int, r: int = -1):
    if r < 0:
        r = ring(x)
    return 0 if r == 0 else (x - 1) // r - 3 * (r - 1)


def tranche(x: int, r: int = -1):
    if r < 0:
        r = ring(x)
    return 0 if r == 0 else (x - 1) % r


def polar(x: int, r: int = -1):
    """
    Given index X, find the R, S and T co-ordinates.
    :param x:
    :param r:
    :return:
    """
    if x == 0:
        return 0, 0, 0
    x -= 1
    if r < 0:
        r = floor(0.5 + sqrt(x / 3 + 0.25))
    s = (x // r) - (3 * (r - 1))
    t = x % r
    return r, s, t


def lateral_prev_index(x: int):
    """
        TODO
        :param x:
        :return:
        """
    if x == 0:
        return []
    r = ring(x)
    xl = 3 * r * (r - 1) + 1
    if x == xl:
        return [xl + 6 * r - 1]
    return [x - 1]


def lateral_next_index(x: int):
    """
        TODO
        :param x:
        :return:
        """
    if x == 0:
        return []
    r = ring(x)
    xh = 3 * r * (r + 1)
    if x == xh:
        return [xh - 6 * r + 1]
    return [x + 1]


def lateral_prev_polar(r: int, s: int = 0, t: int = 0):
    """
    TODO
    :param r:
    :param s:
    :param t:
    :return:
    """
    if r == 0:
        return []
    sp = s
    tp = t - 1
    if tp < 0:
        tp += r
        sp -= 1
        if sp < 0:
            sp += 6
    return [(r, sp, tp)]


def lateral_next_polar(r: int, s: int = 0, t: int = 0):
    """
    TODO
    :param r:
    :param s:
    :param t:
    :return:
    """
    if r == 0:
        return []
    sn = s
    tn = t + 1
    if tn >= r:
        tn -= r
        sn += 1
        if sn >= 6:
            sn -= 6
    return [(r, sn, tn)]


def radial_prev_index(x: int, r: int = -1):
    """
    TODO
    :param x:
    :param r:
    :return:
    """
    if x == 0:
        return []
    if x <= 6:
        return [0]
    r, s, t = polar(x, r)
    r -= 1
    y = x - 6 * r - s
    if t == 0:
        return [y]
    if s == 5 and t == r:
        return [y - 1, y - 6 * r]
    return [y - 1, y]


def radial_next_index(x: int, r: int = -1):
    """
    TODO
    :param x:
    :param r:
    :return:
    """
    if x == 0:
        return [1, 2, 3, 4, 5, 6]
    r, s, t = polar(x, r)
    y = x + 6 * r + s
    if t == 0:
        return [y + (5 + 6 * r if s == 0 else -1), y, y + 1]
    return [y, y + 1]


def radial_prev_polar(r: int, s: int = 0, t: int = 0):
    """
    TODO
    :param r:
    :param s:
    :param t:
    :return:
    """
    if r == 0:
        return []
    if r == 1:
        return [(0, 0, 0)]
    r -= 1
    if t == 0:
        return [(r, s, 0)]
    if t == r:
        return [(r, s, t - 1), (r, 0 if s == 5 else s + 1, 0)]
    return [(r, s, t - 1), (r, s, t)]


def radial_next_polar(r: int, s: int = 0, t: int = 0):
    """
    TODO
    :param r:
    :param s:
    :param t:
    :return:
    """
    if r == 0:
        return [(1, s, 0) for s in range(0, 6)]
    r += 1
    if t == 0:
        return [(r, 5 if s == 0 else s - 1, r - 1), (r, s, 0), (r, s, 1)]
    return [(r, s, t), (r, s, t + 1)]
