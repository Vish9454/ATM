from rest_framework.authtoken.models import Token
from atm.models import User
from django.contrib.gis.geos import Point


def get_or_create_user_token(instance):
    """
        method used to create the user toke
    :param instance:
    :return: token key
    """
    obj = User.objects.filter(email=instance).first()
    token, created = Token.objects.get_or_create(user=obj)
    return token.key


def save_user_coordinate(instance, latitude, longitude) -> object:
    """
        method used to save the user coordinates
    :param instance:
    :param latitude:
    :param longitude:
    :return:
    """
    point = Point(x=longitude, y=latitude, srid=4326)
    instance.coordinate = point
    return instance


def get_latitude_from_obj(instance):
    """
        method used to get the latitude of the address
    :param instance:
    :return:
    """
    try:
        latitude = instance.geolocation.y
    except Exception:
        latitude = 0
    return latitude


def get_longitude_from_obj(instance):
    """
        method used to get the longitude of the address
    :param instance:
    :return:
    """
    try:
        longitude = instance.geolocation.x
    except Exception:
        longitude = 0
    return longitude

