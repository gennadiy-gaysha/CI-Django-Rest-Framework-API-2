from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view()
def endpoint_list(request):
    return Response([
        'http://127.0.0.1:8000/profiles',
        'http://127.0.0.1:8000/posts/',
        'http://127.0.0.1:8000/comments/',
        'http://127.0.0.1:8000/likes/',
        'http://127.0.0.1:8000/followers/',

    ]
    )