from django.db.models import Count
from rest_framework import generics, filters
from drf_api.permissions import IsOwnerOrReadOnly
from .serializers import ProfileSerializer
from .models import Profile
from django_filters.rest_framework import DjangoFilterBackend


# posts_count
# followers_count
# following_count
class ProfileList(generics.ListAPIView):
    # queryset = Profile.objects.all()
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = [
        'posts_count',
        'followers_count',
        'following_count'
        'owner__following__created_at',
        'owner__followed__created_at',

    ]

    filterset_fields = [
        # filter user profiles that  follow a user with a given profile_id.
        'owner__following__followed__profile',
        # get all profiles that are followed by a profile, given its id
        'owner__followed__owner__profile'
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProfileDetail(generics.RetrieveUpdateAPIView):
    # queryset = Profile.objects.all()
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]
