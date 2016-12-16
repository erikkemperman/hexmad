from math import cos
from math import acos
from math import sin
from math import asin
from math import sqrt
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

    k = 2
    for fraction in [x / k for x in range(0, k + 1)]:
        delta = epsilon * fraction
        cd = cos(delta)
        sd = sin(delta)
        dlon = sin(abs(lon2 - lon1)) / sin(epsilon)

        beta1 = asin(s2 * dlon)
        latx1 = acos(c1 * cd - s1 * sd * cos(beta1))

        beta2 = asin(s1 * dlon)
        latx2 = acos(c2 * cos(epsilon - delta) - s2 * sin(epsilon - delta) * cos(beta2))

        # TODO cos(asin(x)) simplify
        # determine latx1 vs latx2

        # TODO lonx
        print()







if __name__ == "__main__":
    main()