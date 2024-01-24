from rest_framework import serializers
from .models import Post
from likes.models import Like


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    is_owner = serializers.SerializerMethodField()
    like_id = serializers.SerializerMethodField()
    comments_count=serializers.ReadOnlyField()
    likes_count=serializers.ReadOnlyField()

    def validate_image(self, value):
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                'Image size larger than 2MB!'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width larger than 4096px'
            )
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height larger than 4096px'
            )
        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    # Method checks if the current authenticated user has liked the post
    # represented by obj, and if so, it will return the ID of the Like instance
    def get_like_id(self, obj):
        # Retrieves the current user from the request context.
        # If the request is not authenticated, request.user would be an instance of
        # django.contrib.auth.models.AnonymousUser
        user = self.context['request'].user
        if user.is_authenticated:
            # (my text) we filter only those Post instances on .../posts/, where
            # logged-in user (user) is the owner (field in Like model) of the like
            # and post object of Like instance (post) is the same as obj - serialized
            # instance of Post model
            # (Chat GPT) Filters the Like model for an instance where the owner is
            # the current user and the post is the post instance being serialized (obj)
            like = Like.objects.filter(owner=user, post=obj).first()
            return like.id if like else None
        return None
    class Meta:
       model = Post
       fields = [
            'id', 'owner', 'is_owner', 'profile_id',
            'profile_image', 'created_at', 'updated_at',
            'title', 'content', 'image', 'image_filter', 'like_id', 'comments_count', 'likes_count'
       ]