from math import pi, sin, cos, atan2, sqrt


def getDistance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Return distance between to point in lat/lon
    source - https://qna.habr.com/answer?answer_id=1077472#answers_list_answer

    :param lat1: latitude of first point
    :param lon1: longitude of first point
    :param lat2: latitude of second point
    :param lon2: longitude of second point
    :return:
    """

    def deg2rad(deg):
        return deg * (pi / 180)

    d_lat = deg2rad(lat2 - lat1)
    d_lon = deg2rad(lon2 - lon1)
    a = sin(d_lat / 2) * sin(d_lat / 2) + cos(deg2rad(lat1)) * cos(deg2rad(lat2)) * sin(d_lon / 2) * sin(d_lon / 2)
    return 6371 * 2 * atan2(sqrt(a), sqrt(1 - a))
