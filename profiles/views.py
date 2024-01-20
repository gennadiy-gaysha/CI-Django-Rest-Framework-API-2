# - receive Request instances in your view
# - handle parsing errors
# - add  context to Response objects
# -extends Django's basic view functionality to provide a set of HTTP method handlers
# such as get(), post(), put(), delete(), etc., that you can override to define the
# behavior of your API.
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer
class ProfileList(APIView):
    # In DRF, when a request comes in, it's wrapped in a Request instance - request
    def get(self, request):
        # profile queryset is not used it in the response.
        # It should be serialized into a format that can be converted to
        # JSON (or another format) and passed to the Response object
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        # The serializer.data (which is a Python dictionary) is passed to the
        # Response object. The Response class then automatically renders this
        # data into the appropriate content type (e.g., JSON) based on the
        # client's request
        return Response(serializer.data)
        # This example shows how you can retrieve data from the database,
        # serialize it, and return it in a response, adhering to RESTful
        # principles and leveraging the capabilities of Django REST Framework.


