# - receive Request instances in your view
# - handle parsing errors
# - add  context to Response objects
# - extends Django's basic view functionality to provide a set of HTTP method handlers
# such as get(), post(), put(), delete(), etc., that you can override to define the
# behavior of your API.
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer

from drf_api.permissions import IsOwnerOrReadOnly


class ProfileList(APIView):
    # In DRF, when a request comes in, it's wrapped in a Request instance - request
    def get(self, request):
        # profile queryset is not used it in the response.
        # It should be serialized into a format that can be converted to
        # JSON (or another format) and passed to the Response object
        profiles = Profile.objects.all()
        # By passing the request object in the context, you make it available
        # to the serializer. This is crucial because get_is_owner needs the
        # request object to access the current user and compare it with the
        # profile owner.
        serializer = ProfileSerializer(profiles, many=True, context={'request': request})
        # The serializer.data (which is a Python dictionary) is passed to the
        # Response object. The Response class then automatically renders this
        # data into the appropriate content type (e.g., JSON) based on the
        # client's request
        return Response(serializer.data)
        # This example shows how you can retrieve data from the database,
        # serialize it, and return it in a response, adhering to RESTful
        # principles and leveraging the capabilities of Django REST Framework.


class ProfileDetail(APIView):
    serializer_class = ProfileSerializer
    # If permission_classes is set to [IsOwnerOrReadOnly] it means the
    # IsOwnerOrReadOnly permission check will be applied to all requests handled by
    # this view.
    permission_classes = [IsOwnerOrReadOnly]

    # try-except Block: The get_object method uses a try-except block to handle
    # the possibility of the Profile instance not existing:
    # Try: It tries to retrieve the Profile instance with Profile.objects.get(pk=pk).
    # Exception Handling: If no Profile instance is found (i.e., Profile.DoesNotExist
    # is raised), the method raises an Http404 exception. This results in Django
    # returning a 404 Not Found response to the client.
    def get_object(self, pk):
        try:
            profile = Profile.objects.get(pk=pk)
            # This method checks the permissions specified in permission_classes
            # against the retrieved Profile instance

            # This is where IsOwnerOrReadOnly comes into play. It ensures that the
            # user making the request is either the owner of the profile (for non-safe
            # methods) or allows access to anyone (for safe methods).
            self.check_object_permissions(self.request, profile)
            return profile
        except Profile.DoesNotExist:
            raise Http404

    # 1) The get method of the ProfileDetail class is the entry point for
    # handling the GET request. It's responsible for processing the request,
    # fetching the relevant Profile instance, serializing it, and returning
    # the response.
    # Fetching the Profile: profile = self.get_object(pk)
    # This line calls the get_object method, passing the pk obtained from the URL.
    # The get_object method attempts to retrieve a Profile instance with the given
    # pk from the database.
    def get(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        # The first step in the put method is to retrieve the Profile instance that
        # needs to be updated:
        # The put method retrieves the existing data from the database (the data that
        # is about to be updated), but this happens behind the scenes. This retrieval
        # is done to ensure that the correct instance (in your case, the correct Profile
        # instance) is being updated.
        # This is achieved with the line profile = self.get_object(pk), which fetches
        # the Profile instance that corresponds to the provided primary key (pk).
        profile = self.get_object(pk)
        # The serializer (ProfileSerializer(profile, data=request.data)) takes this
        # new data, validates it, and if valid, updates the Profile instance in the
        # database with this new data.

        # A ProfileSerializer is instantiated with two arguments: the Profile instance
        # to be updated and the data from the request (request.data). This step
        # deserializes the request data and initializes the serializer with the current
        # instance and the new data.
        serializer = ProfileSerializer(profile, data=request.data, context={'request': request})
        # so these two lines above interact on a server side in python format!
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
