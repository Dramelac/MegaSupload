from django.core.exceptions import ObjectDoesNotExist

from MegaSuploadAPI.models import User


def getUserFromId(userId):
    user = User.objects.get(id=userId)
    if user is not None:
        return user
    else:
        raise ObjectDoesNotExist
