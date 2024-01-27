from rest_framework.decorators import api_view
from rest_framework.response import Response
from .settings import (
    JWT_AUTH_COOKIE,
    JWT_AUTH_REFRESH_COOKIE,
    JWT_AUTH_SAMESITE,
    JWT_AUTH_SECURE
)


@api_view()
def endpoint_list(request):
    return Response([
        'http://127.0.0.1:8000/profiles/',
        'http://127.0.0.1:8000/posts/',
        'http://127.0.0.1:8000/comments/',
        'http://127.0.0.1:8000/likes/',
        'http://127.0.0.1:8000/followers/',
        'https://drf-api-app-gaysha-repeat-150999686cdd.herokuapp.com/profiles/',
        'https://drf-api-app-gaysha-repeat-150999686cdd.herokuapp.com/posts/',
        'https://drf-api-app-gaysha-repeat-150999686cdd.herokuapp.com/comments/',
        'https://drf-api-app-gaysha-repeat-150999686cdd.herokuapp.com/likes/',
        'https://drf-api-app-gaysha-repeat-150999686cdd.herokuapp.com/followers/',
    ]
    )


# dj-rest-auth logout view fix
@api_view(['POST'])
def logout_route(request):
    response = Response()
    response.set_cookie(
        key=JWT_AUTH_COOKIE,
        value='',
        httponly=True,
        expires='Thu, 01 Jan 1970 00:00:00 GMT',
        max_age=0,
        samesite=JWT_AUTH_SAMESITE,
        secure=JWT_AUTH_SECURE,
    )
    response.set_cookie(
        key=JWT_AUTH_REFRESH_COOKIE,
        value='',
        httponly=True,
        expires='Thu, 01 Jan 1970 00:00:00 GMT',
        max_age=0,
        samesite=JWT_AUTH_SAMESITE,
        secure=JWT_AUTH_SECURE,
    )
    return response
