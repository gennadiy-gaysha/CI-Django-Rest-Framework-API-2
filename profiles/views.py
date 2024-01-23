from rest_framework import generics
from drf_api.permissions import IsOwnerOrReadOnly
from .serializers import ProfileSerializer
from .models import Profile

class ProfileList(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ProfileDetail(generics.RetrieveDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]

