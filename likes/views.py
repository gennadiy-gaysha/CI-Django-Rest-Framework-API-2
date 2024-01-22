from rest_framework import permissions, generics
from drf_api.permissions import IsOwnerOrReadOnly
from .serializers import LikeSerializer
from .models import Like

class LikeList(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # The primary purpose of overriding perform_create is to add custom behavior
    # during the save operation of a model instance. In your case, when a new Like
    # instance is created, you need to assign the owner of the Like to the current
    # authenticated user making the request. This cannot be done automatically by
    # the serializer since the owner field is a ReadOnlyField in your LikeSerializer.

    # perform_create is a powerful way to include additional logic when creating new
    # instances of a model via a DRF view. In your case, it's essential for correctly
    # associating each new Like with the authenticated user who created it
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class LikeDetail(generics.RetrieveDestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsOwnerOrReadOnly]
