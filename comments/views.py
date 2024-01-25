from rest_framework import generics, permissions
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Comment
from .serializers import CommentSerializer, CommentDetailSerializer
from django_filters.rest_framework import DjangoFilterBackend


# CommentList is a class that inherits from generics.ListCreateAPIView.
# This is a generic view provided by Django REST Framework (DRF) which
# is used for read-write endpoints to represent a collection of model
# instances. It provides functionality to list a queryset or create a
# new model instance.
class CommentList(generics.ListCreateAPIView):
    # queryset: This attribute defines the set of Comment model instances that
    # this view will operate on. Comment.objects.all() indicates that the view
    # will handle all instances of the Comment model.
    queryset = Comment.objects.all()
    # serializer_class: This attribute tells DRF which serializer to use when
    # processing the input (for creating new Comment instances) and output (when
    # listing existing comments). The CommentSerializer is responsible for
    # converting the Comment model instances to JSON format for API responses
    # and vice-versa for API requests.
    serializer_class = CommentSerializer
    # permission_classes: This list of permission classes is used to control
    # access to this view. permissions.IsAuthenticatedOrReadOnly ensures that
    # only authenticated users can create new comments (POST request), but any
    # user (authenticated or not) can read the list of comments (GET request).
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        # retrieve all the comments associated with a given post.
        'post',
    ]

    # This method is overridden from the parent class. It's called when a new
    # Comment instance is being created (i.e., when a POST request is made to
    # the API endpoint corresponding to this view).
    def perform_create(self, serializer):
        # serializer.save(owner=self.request.user) is called. This line is crucial
        # as it sets the owner of the new Comment instance to the current user
        # making the request (self.request.user). The serializer.save() function
        # is responsible for saving the new instance to the database after adding
        # the owner field to the validated data from the request.

        # When you call serializer.save(), as in the perform_create method, the
        # serializer already has the context with the request, which can be used
        # inside the serializer, for instance, in the create or update methods,
        # or to access request data in SerializerMethodField calculations.

        # When you instantiate a serializer within this view (which happens
        # automatically when the view processes a request), the request is included
        # in the context. Thus, in your serializer, you can access the request using
        # self.context['request'].
        # This is particularly useful in your CommentSerializer where you might need
        # access to the request, for example, in the get_is_owner method to compare
        # request.user with the owner of the comment.
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CommentDetailSerializer

# By having two serializers:
# CommentSerializer can be used for creating comments where the post field is writable.
# CommentDetailSerializer can be used for editing comments where the post field is read-only.
