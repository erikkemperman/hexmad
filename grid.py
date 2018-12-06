import argparse
import MySQLdb

from math import pi
from math import degrees
from math import radians
from math import sqrt
from math import nan



from config import Config
from model import geometry


def generate_grid(city, rings, latitude, longitude, radius):
    try:
        db = MySQLdb.connect(host=Config.DB_HOST, user=Config.DB_USER, passwd=Config.DB_PASS, db=Config.DB_NAME)
        cursor = db.cursor()
    except Exception as e:
        print(e)
        return

    # print('Generating grid for ' + args.c + '...')

    latitude = radians(latitude)
    longitude = radians(longitude)

    rho = radius / Config.EARTH_RADIUS(latitude)  # radius in radians
    rho_lng = 1.5 * rho
    rho_lat = 0.5 * sqrt(3) * rho

    mid = rings - 1
    dim = 2 * rings - 1
    lats = [latitude] * dim
    lngs = [longitude] * dim

    for j in range(1, rings):
        rj = rho_lng * j
        lngs[mid - j] = longitude - rj
        lngs[mid + j] = longitude + rj
        # TODO check if longs in range

    for k in range(1, rings):
        rk = rho_lat * k
        lats[mid - k] = latitude - rk
        lats[mid + k] = latitude + rk
        # TODO check if lats in range

    print('window.bla = [')
    for k in range(0, dim):
        if k % 2 == 0:
            for j in range(1, dim, 2):
                print('{ lat: %f, lng: %f },' % (degrees(lats[k]), degrees(lngs[j])))
        else:
            for j in range(0, dim, 2):
                print('{ lat: %f, lng: %f },' % (degrees(lats[k]), degrees(lngs[j])))
    print(']')
    return

    index = 0
    try:
        cursor.execute(Config.DB_GRID_INSERT % (
            city,
            index, 0, 0, 0,
            degrees(latitude), degrees(longitude),
            latitude, longitude,
            radius
        ))
        for j in range(1, rings):
            for s in range(0, 6):
                for t in range(0, j):
                    index += 1

                    cursor.execute(Config.DB_GRID_INSERT % (
                        city,
                        index, j, s, t,
                        latitude, longitude,
                        radians(latitude), radians(longitude),
                        radius
                    ))
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
    finally:
        cursor.close()
        db.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate grid for given city')
    parser.add_argument('-c', default=Config.GRID_NAME, type=str, help='Name of the city')
    parser.add_argument('-n', default=Config.GRID_RINGS, type=int, help='Number of rings')
    parser.add_argument('-l', default=Config.GRID_ORIGIN_LAT, type=int, help='Origin latitude')
    parser.add_argument('-m', default=Config.GRID_ORIGIN_LNG, type=int, help='Origin longitude')
    parser.add_argument('-r', default=Config.GRID_RADIUS, type=int, help='Radius of cells')

    args = parser.parse_args()

    args.c = args.c.lower().replace(' ', '_')

    generate_grid(args.c, args.n, args.l, args.m, args.r)





