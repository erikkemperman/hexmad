from math import cos
from math import acos
from math import sin
from math import asin
from math import sqrt
from math import degrees
from math import radians


def main():
    lat1, lon1 = [radians(x) for x in [51.923046, 4.476899]]  # Rotterdam
    lat2, lon2 = [radians(x) for x in [53.190727, 5.806451]]  # Leeuwarden

    c1 = cos(lat1)
    c2 = cos(lat2)
    s1 = sin(lat1)
    s2 = sin(lat2)
    h1 = sin(0.5 * (lat2 - lat1))
    h2 = sin(0.5 * (lon2 - lon1))

    epsilon = 2 * asin(sqrt(h1 * h1 + h2 * h2 * c1 * c2))
    dlon = sin(abs(lon2 - lon1)) / sin(epsilon)  # TODO wrong if epsilon nears 0 or pi

    k = 2
    for fraction in [x / k for x in range(0, k + 1)]:
        delta = epsilon * fraction

        cd = cos(delta)
        sd = sin(delta)
        beta1 = asin(s2 * dlon)  # TODO wrong if s2*dlon near -1 or 1 (asin near +- 0.5 pi)
        latx1 = acos(c1 * cd - s1 * sd * cos(beta1))  # TODO wrong if arg near -1 or 1 (acos near 0 or pi)
        check1 = acos(c1 * cd - s1 * sd * sqrt(1 - s2 * s2 * dlon * dlon))
        print(latx1)
        print(check1)

        ce = cos(epsilon - delta)
        se = sin(epsilon - delta)
        beta2 = asin(s1 * dlon)
        latx2 = acos(c2 * ce - s2 * se * cos(beta2))
        check2 = acos(c2 * ce - s2 * se * sqrt(1 - s1 * s1 * dlon * dlon))
        print(latx2)
        print(check2)

        # TODO cos(asin(x)) simplify?

        lont1 = asin(sd * s2 * dlon / sin(latx1))
        lonx1 = min(lon1, lon2) + lont1
        print(lonx1, " (? ", lont1)

        lont2 = asin(se * s1 * dlon / sin(latx2))
        lonx2 = max(lon1, lon2) - lont2
        print(lonx2, " (? ", lont2)

        print('=>', degrees(latx1), degrees(lonx1))
        print('=>', degrees(latx2), degrees(lonx2))
        # TODO criteria to prefer version 1 or 2 for lat and lon?

if __name__ == "__main__":
    main()
