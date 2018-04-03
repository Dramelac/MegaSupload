import json
from json import JSONDecodeError

from django.http import JsonResponse


def json_parser(func):
    def wrapper(request, *args, **kwargs):
        try:
            request.json = json.loads(request.body.decode("utf-8"))
        except JSONDecodeError:
            return JsonResponse({"message": "Bad JSON."}, status=400)
        return func(request, *args, **kwargs)
    return wrapper
