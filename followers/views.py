from .serializers import FollowerSerializer
from .models import Follower
from drf_api.permissions import IsOwnerOrReadOnly
from rest_framework import permissions, generics


# See full description in comments/views.py
class FollowerList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = FollowerSerializer
    queryset = Follower.objects.all()


    # See full description in comments/views.py, likes/views.py
    # When a new Follower instance is created, you need to assign the owner
    # of the Follower to the current authenticated user making the request.
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class FollowerDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = FollowerSerializer
    queryset = Follower.objects.all()


# When an authenticated user decides to follow another user and initiates a POST
# request the following sequence of events occurs based on the provided code snippets:

# 1. Request Initiation:
# The user interacts with the client interface (e.g., by clicking a "Follow" button),
# which sends a POST request to the server to create a new `Follower` instance. The
# request includes the ID of the user to be followed.

# 2. View Processing:
# Django Rest Framework routes the request to the `FollowerList` view since it matches
# the URL pattern defined for follower creation.

# 3. Permissions Check:
# Before proceeding, the `FollowerList` view checks that the user is authenticated
# due to the `permissions.IsAuthenticatedOrReadOnly` permission class. If the user
# is not authenticated, the request will be rejected.

# 4. Serializer Initialization:
# The `FollowerList` view initializes the `FollowerSerializer` with the data from
# the request.

# 5. Data Validation:
# The `FollowerSerializer` validates the incoming data against the `Follower` model
# constraints. It checks that the `followed` field is present and that the data types
# are correct.

# 6. Perform Create:
# If the data is valid, the `FollowerList` view calls the `perform_create` method,
# passing the `FollowerSerializer` instance. Within `perform_create`, the
# `serializer.save` method is called with `owner=self.request.user` to set the `owner`
# field to the authenticated user making the request.

# 7. Serializer Save:
# The `FollowerSerializer`'s overridden `create` method attempts to save the new
# `Follower` instance using `super().create(validated_data)`. This calls the default
# create method of the base `ModelSerializer` class.

# 8. Integrity Check:
# During the save operation, the database checks for integrity constraints. If the
# `unique_together` constraint on the `['owner', 'followed']` fields in the `Follower`
# model is violated (meaning this user already follows the target user), an
# IntegrityError` is raised.

# 9. Exception Handling:
# If an `IntegrityError` occurs, the `except` block in the `create` method catches the
# exception and raises a `serializers.ValidationError` with the message 'possible
# duplicate'. This prevents the creation of a duplicate `Follower` instance.
#
# 10. Response:
# Finally, a response is sent back to the client. If the creation was successful, it
# will typically be a 201 Created response with the serialized `Follower` instance data.
# If there was an error, such as a 'possible duplicate' error, the response will contain
# the error message and a corresponding error status code.
#
# Remember that the PUT method is idempotent and typically used for updating resources.
# For creating new instances, a POST request is more appropriate, and the client should
# use POST to follow the RESTful API conventions.
