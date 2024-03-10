from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    is_owner = serializers.SerializerMethodField()
    post_info = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_post_info(self,obj):
        return {
            'username': obj.post.owner.username,
            'title': obj.post.title
        }

    # self refers to the instance of the CommentSerializer class itself.
    # In the context of a serializer method, self is used to access the
    # properties and methods of the serializer instance.
    # In your method get_is_owner, self is used to access the serializer's
    # context with self.context. The context is a dictionary that can hold
    # extra information useful for serialization. In this case, it's used
    # to pass the current HTTP request object (request) to the serializer.

    # obj refers to the instance of the object being serialized. For
    # CommentSerializer, obj is an instance of the model class that the
    # serializer is meant to serialize (presumably a Comment model in this case).
    # In get_is_owner, obj is used to access the owner of the comment. The
    # method is checking whether the user making the request (request.user)
    # is the same as the owner of the comment (obj.owner).
    def get_is_owner(self, obj):
        # Context Access:
        # The method starts by extracting the request from the serializer's
        # context: request = self.context['request']. This request object
        # includes information about the current user making the request.
        # Ownership Comparison:
        # It then compares the owner of the Comment instance (obj.owner) to
        # the user who made the request (request.user). If they are the same,
        # it means the user making the request owns the comment being serialized.
        request = self.context['request']
        return request.user == obj.owner

    def get_created_at(self, obj):
        return naturaltime(obj.created_at)

    def get_updated_at(self, obj):
        return naturaltime(obj.updated_at)

    class Meta:
        model = Comment
        fields = ['id', 'owner', 'is_owner', 'profile_id', 'profile_image',
                  'post', 'post_info', 'created_at', 'updated_at', 'content']

# Inherits from CommentSerializer, meaning it starts with all the functionality
# of CommentSerializer and then adds or overrides specific features.
# I.e., it automatically includes all the fields and methods defined in
# CommentSerializer. This means it will have fields like id, owner, is_owner,
# profile_id, profile_image, created_at, updated_at, and content.
class CommentDetailSerializer(CommentSerializer):
    post = serializers.ReadOnlyField(source='painting.id')

# By having two serializers:
# CommentSerializer can be used for creating comments where the post field is writable.
# CommentDetailSerializer can be used for editing comments where the post field is read-only.

