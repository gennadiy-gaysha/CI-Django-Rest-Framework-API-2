from django.http import Http404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_api.permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostSerializer


class PostList(APIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        posts = Post.objects.all()
        # The posts queryset is passed to the serializer with many=True,
        # indicating that multiple objects are being serialized.
        # The context parameter is used to pass additional data to the
        # serializer – in this case, the current HTTP request (request).
        # This can be useful for operations that require request data,
        # such as generating hyperlinks.
        serializer = PostSerializer(
            posts, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def post(self, request):
        # The data sent with the POST request (typically in JSON format) is available
        # in request.data
        # initializes a PostSerializer instance for deserialization.
        serializer = PostSerializer(data=request.data, context={'request': request})
        # validates the data against the serializer's fields and constraints.
        if serializer.is_valid():
            # saves the new Post instance to the database.
            # The owner of the post is set to the current user (request.user),
            # assuming the Post model has an owner field linked to the user.
            serializer.save(owner=request.user)
            # sends a response with the serialized data of the new post and an
            # HTTP status code of 201, indicating successful creation.
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Handling Invalid Data:
        # If the data is not valid, return Response(serializer.errors,
        # status=status.HTTP_400_BAD_REQUEST) sends a response with the
        # serialization errors and an HTTP status code of 400.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    # get_object is a helper method to retrieve a Post instance
    # based on its primary key (pk). This pk (primary key) is passed
    # to the method when it's called. It represents the ID of the Post
    # that you're trying to retrieve.
    # This pk typically comes from the URL. For instance, if your URL
    # pattern is something like
    # path('posts/<int:pk>/', views.PostDetail.as_view()),
    # then when a user accesses a URL like http://127.0.0.1:8000/posts/5/,
    # the number 5 is captured and passed as the pk to the get_object method.
    def get_object(self, pk):
        try:
            # pk in the Query (Post.objects.get(pk=pk)):
            # The pk used in Post.objects.get(pk=pk) is a field lookup
            # in Django's query syntax. Here, pk on the left side of pk=pk is
            # referring to the primary key field of the Post model in the database.
            # The pk on the right side of pk=pk is the value passed to the get_object
            # method (from the URL, as mentioned above).
            post = Post.objects.get(pk=pk)
            # self.check_object_permissions(request, obj) Method:
            # checks whether the user making the request (self.request) has the required
            # permissions to perform the action on this particular post object (post).
            # Your view (PostDetail) has a permission_classes attribute set to
            # [IsOwnerOrReadOnly]. This means that the IsOwnerOrReadOnly permission
            # class will be used to determine if the request is permitted on the obj.

            # When you call self.check_object_permissions(self.request, post), DRF
            # internally calls the has_object_permission method of each permission
            # class listed in permission_classes.
            # It passes self.request, the current view instance (self), and the post
            # object to this method.
            # If any of the permission checks fail, DRF raises an appropriate
            # exception (like PermissionDenied), which translates into an HTTP
            # 403 Forbidden response (unless it's an anonymous user, which results
            # in a 401 Unauthorized response).
            self.check_object_permissions(self.request, post)
            return post
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_object(pk)
        # Deserialize and Validate Data:
        # serializer = PostSerializer(post, data=request.data, context={'request': request})
        # initializes the serializer with the post instance and the new data from the request.
        serializer = PostSerializer(post, data=request.data, context={'request': request})
        # validates the data:
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
