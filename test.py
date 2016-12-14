import requests
import json


KEY = "AIzaSyAgEC4HM4HaUCY-lPomO7uvp5zxbNlb3ZE"
BASE = "https://maps.googleapis.com/maps/api/place/"
SEARCH = BASE + "nearbysearch/json?key=%s&location=%s,%s&radius=%s"
DETAIL = BASE + "details/json?key=%s&placeid=%s"

LAT = 51.915341
LON = 4.527612
RAD = 50


def get_search_ids(lat, lon, rad):
    url = SEARCH % (KEY, lat, lon, rad)
    try:
        request = requests.get(url)
    except Exception as e:
        print()
        print(lat)
        print(lon)
        print(e)
        return []

    result = json.loads(request.text)
    print(request.text + "\n\n\n")

    if result["status"] != "OK":
        print()
        print("STATUS SEARCH IS NOT OK")
        print(lat)
        print(lon)
        return []
    # html_attributions seems empty

    return [p["place_id"] for p in result["results"]]


def get_place(id):
    # TODO
    print()
    print(id)

    url = DETAIL % (KEY, id)
    try:
        request = requests.get(url)
    except Exception as e:
        print()
        print(id)
        print(e)
        return []

    result = json.loads(request.text)

    print("\n\nHERE\n\n" + request.text)

    if result["status"] != "OK":
        print()
        print("STATUS SEARCH IS NOT OK")
        print(id)
        return []
    # html_attributions seems empty

    print(result["result"].keys())
    for key in result["result"]:
        print("\n" + key)
        print(result["result"][key])


def main():
    ids = get_search_ids(LAT, LON, RAD)

    for id in ids:
        get_place(id)




if __name__ == "__main__":
    #  main()

    #  Starting at
