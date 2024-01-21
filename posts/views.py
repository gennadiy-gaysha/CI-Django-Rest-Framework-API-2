from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer


class PostList(APIView):
    serializer_class=PostSerializer
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
        serializer = PostSerializer(data = request.data, context={'request': request})
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


