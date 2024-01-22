from django.db import IntegrityError
from rest_framework import serializers
from .models import Like

class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    post_info = serializers.SerializerMethodField()

    def get_post_info(self, obj):
        return {
            'username': obj.post.owner.username,
            'title': obj.post.title
        }

    class Meta:
        model = Like
        fields = ['id', 'created_at', 'owner', 'post', 'post_info' ]

    # The create function in your LikeSerializer class is an overridden method
    # from Django's ModelSerializer class, which is used to handle the creation
    # of new instances of the Like model based on the validated data received
    # from an API request.
    def create(self, validated_data):
        try:
            # super().create(validated_data) calls the create method of the
            # superclass (ModelSerializer in this case). This method takes the
            # validated_data - which is a dictionary containing deserialized
            # input data - and creates a new instance of the Like model. The
            # validated_data would typically include the fields necessary to
            # create a Like instance, such as the user (owner) and the post
            # being liked (post).
            return super().create(validated_data)
        # Handling IntegrityError: The try...except block is used to catch any
        # IntegrityError that might be raised during the creation of a new Like
        # instance. An IntegrityError would occur if the creation violates any
        # database constraints. In your case, the most likely cause of an
        # IntegrityError is the violation of the unique_together constraint in
        # the Like model, which ensures that a user cannot like the same post
        # more than once.
        except IntegrityError:
            # If an IntegrityError is caught, the function raises a
            # serializers.ValidationError. This is a custom error handling to
            # provide a more specific and user-friendly error message. In your
            # code, it specifies the error with the message
            # {'detail': 'possible duplicate'}, indicating that the like action
            # might be a duplicate (i.e., the user has already liked the post).
            raise serializers.ValidationError({
                'detail': 'possible duplicate',
            })