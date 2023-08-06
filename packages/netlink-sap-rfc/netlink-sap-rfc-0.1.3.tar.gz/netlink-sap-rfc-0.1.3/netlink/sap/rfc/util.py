import datetime


def dats_to_date(dats: str):
    try:
        return datetime.datetime.strptime(dats, '%Y%m%d').date()
    except ValueError:
        return None


def tims_to_time(tims: str):
    try:
        return datetime.datetime.strptime(tims, '%H%M%S').time()
    except ValueError:
        return None


def datstims_to_datetime(dats: str, tims: str):
    try:
        return datetime.datetime.strptime(f'{dats}{tims}', '%Y&m&d%H%M%S')
    except ValueError:
        return None
