from django.db.models import Count
from rest_framework import permissions, generics, filters
from drf_api.permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer
from .models import Post
from django_filters.rest_framework import DjangoFilterBackend

# comments_count
# likes_count
class PostList(generics.ListCreateAPIView):
    # queryset = Post.objects.all()
    queryset = Post.objects.annotate(
        comments_count=Count('comment', distinct=True),
        likes_count=Count('likes', distinct=True)
    ).order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend,]
    ordering_fields = ['likes_count', 'comments_count', 'likes__created_at',]
    search_fields=['owner__username', 'title']
    # 1) showing posts that are owned by users that a particular user is following
    # i.e., getting the user post feed by their profile id
    # 2) liked by a  particular user - returns all the posts a user with a given id liked
    # 3) owned by a particular user
    filterset_fields=[
        'owner__followed__owner__profile',
        # 1) 'likes': This is the related_name for the ForeignKey relationship from the Like
        # model to the Post model. It represents the connection from a post to all the
        # like objects associated with it
        # 2) '__': In Django's query language, double underscores are used to access related
        # fields or to apply filters on fields of related models.
        # 3) 'owner': This is a field in the Like model, which is a ForeignKey to the User
        # model. It indicates the user who created the like.
        # 'likes__owner__profile', - CI suggestion
        'likes__owner',
        'owner__profile',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    # queryset = Post.objects.all()
    queryset = Post.objects.annotate(
        comments_count=Count('comment', distinct=True),
        likes_count=Count('likes', distinct=True)
    ).order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]


# 1) showing posts that are owned by users that a particular user is following,
# 2) liked by a  particular user
# 3) owned by a particular user

