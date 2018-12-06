import argparse
import MySQLdb

from math import ceil
from math import degrees
from math import radians
from math import sqrt
from math import nan

from config import Config
from model import geometry


def generate_grid():
    try:
        db = MySQLdb.connect(host=Config.DB_HOST, user=Config.DB_USER, passwd=Config.DB_PASS, db=Config.DB_NAME)
        cursor = db.cursor()
    except Exception as e:
        print(e)
        return

    # print('Generating grid for ' + args.c + '...')

    latmin = radians(Config.GRID_LAT_MIN)
    latmax = radians(Config.GRID_LAT_MAX)
    latmid = 0.5 * (latmin + latmax)
    lngmin = radians(Config.GRID_LNG_MIN)
    lngmax = radians(Config.GRID_LNG_MAX)
    lngmid = 0.5 * (lngmin + lngmax)

    rho = Config.GRID_RADIUS / Config.EARTH_MEAN_RADIUS  # Config.EARTH_RADIUS(latmid)  # radius in radians

    rho_lat = 0.5 * sqrt(3) * rho
    rho_lng = 1.5 * rho

    dimlat = ceil((latmax - latmin) / rho_lat)
    dimlng = ceil((lngmax - lngmin) / rho_lng)

    lats = [nan] * (dimlat + 1)
    lngs = [nan] * (dimlng + 1)

    for k in range(0, dimlat + 1):
        lats[k] = latmin + k * rho_lat

    for k in range(0, dimlng + 1):
        lngs[k] = lngmin + k * rho_lng

    """
    print('window.bla = [')
    for k in range(0, dimlat + 1):
        if k % 2 == 0:
            for j in range(1, dimlng + 1, 2):
                print('{ lat: %f, lng: %f },' % (degrees(lats[k]), degrees(lngs[j])))
        else:
            for j in range(0, dimlng + 1, 2):
                print('{ lat: %f, lng: %f },' % (degrees(lats[k]), degrees(lngs[j])))
    print(']')

    """

    m1 = dimlat // 2
    m2 = dimlng // 2

    print('first', Config.EARTH_DISTANCE(lats[0], lngs[1], lats[1], lngs[2]))

    return

    try:
        cursor.execute(Config.DB_GRID_INSERT % (
            city,
            index,
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
    generate_grid()





