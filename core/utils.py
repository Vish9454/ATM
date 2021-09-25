from rest_framework.authtoken.models import Token
from atm.models import User


def get_or_create_user_token(instance):
    """
        method used to create the user toke
    :param instance:
    :return: token key
    """
    obj = User.objects.filter(email=instance).first()
    token, created = Token.objects.get_or_create(user=obj)
    return token.key
