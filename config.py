from math import sqrt
from math import asin
from math import sin
from math import cos
from math import radians


class Config:

    GRID_NAME = 'san_diego'
    GRID_ORIGIN_LAT = 32.738514
    GRID_ORIGIN_LNG = -117.147240

    """
    # San Diego car2go area 1
    GRID_LAT_MIN = 32.699732
    GRID_LAT_MAX = 32.780718
    GRID_LNG_MIN = -117.203953
    GRID_LNG_MAX = -117.109841
    GRID_RINGS = 16
    GRID_RADIUS = 100
    """

    # San Diego downtown
    GRID_LAT_MIN = 32.704497
    GRID_LAT_MAX = 32.723174
    GRID_LNG_MIN = -117.176669
    GRID_LNG_MAX = -117.147550
    GRID_RINGS = 16
    GRID_RADIUS = 100

    DB_HOST = 'localhost'
    DB_NAME = 'kahlen_poi'
    DB_USER = 'kahlen_poi'

    DB_GRID_INSERT = """
        REPLACE INTO %s_grid (
            id, ring, segment, tab,
            latitude_deg, longitude_deg,
            latitude_rad, longitude_rad,
            radius
        ) VALUES (
            %d, %d, %d, %d,
            %f, %f,
            %f, %f,
            %d
        )
    """

    EARTH_EQUATORIAL_RADIUS = 6378137.0
    EARTH_POLAR_RADIUS = 6356752.3
    EARTH_MEAN_RADIUS = 6371008.8

    @staticmethod
    def EARTH_RADIUS(latitude):
        lat = radians(latitude)
        a2 = Config.EARTH_EQUATORIAL_RADIUS
        a2 *= a2
        b2 = Config.EARTH_POLAR_RADIUS
        b2 *= b2
        ac = cos(lat)
        ac *= a2
        ac *= ac
        bs = sin(lat)
        bs *= b2
        bs *= bs
        return sqrt((a2 * ac + b2 * bs) / (ac + bs))

    @staticmethod
    def EARTH_DISTANCE(lat1, lon1, lat2, lon2, radius = EARTH_MEAN_RADIUS):
        c1 = cos(lat1)
        c2 = cos(lat2)
        h1 = sin(0.5 * (lat2 - lat1))
        h2 = sin(0.5 * (lon2 - lon1))

        return 2 * asin(sqrt(h1 * h1 + h2 * h2 * c1 * c2)) * radius
