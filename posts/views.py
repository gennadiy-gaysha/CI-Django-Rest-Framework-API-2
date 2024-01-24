from django.db.models import Count
from rest_framework import permissions, generics, filters
from drf_api.permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer
from .models import Post

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
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['likes_count', 'comments_count', 'likes__created_at',]

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

