from math import radians, sin, cos, asin, sqrt, degrees


START_POINT = [54.24, 35.13]
EARTH_RADIUS = 6371 * 100


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    :param lon1: first point longitude
    :param lat1: first point latitude
    :param lon2: second point longitude
    :param lat2: second point latitude
    :return: distance between two points in meters
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    dec_m = EARTH_RADIUS * c
    return dec_m


def translate_geo_to_decart(data):
    """
    converts lonlat into meters
    :param data: dict of data in format [[lon, lat], ...]
    :return: converted data in format [[x, y], ...]
    """
    buf = []
    for point in data:
        x = haversine(float(START_POINT[1]), float(START_POINT[0]),
                      float(START_POINT[1]), float(point[0]))
        y = haversine(float(START_POINT[1]), float(START_POINT[0]),
                      float(point[1]), float(START_POINT[0]))
        buf.append([x, y])
    return buf


def reverse_transofm_coordinates(data):
    """
    reverse translate coords into [lat, lon] from distances
    :param data: dict of data in format [[x, y], ...]
    :return: point in format [lat lon]
    """
    buf = []
    for point in data:
        distance = sqrt(float(point[0])**2 + float(point[1])**2)
        dlat = distance / EARTH_RADIUS
        dlon = asin(sin(dlat) / cos(radians(START_POINT[1])))
        buf.append([START_POINT[0] + degrees(dlon), START_POINT[1] + degrees(dlat)])
    return buf