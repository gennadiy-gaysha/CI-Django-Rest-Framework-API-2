from django.contrib.auth.models import User
from rest_framework import serializers

from followers.models import Follower
from .models import Profile


# if I want to make owner an object (User instance)
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'first_name', 'last_name']  # or any fields you want from the User model


class ProfileSerializer(serializers.ModelSerializer):
    # The ReadOnlyField is used here, which means this field is read-only and
    # will not be used for updating or creating a new Profile instance. It's
    # used only for serialization.
    # source Argument: The source argument is set to 'owner.username'. This tells
    # the serializer to use the username attribute of the owner (User instance)
    # associated with the Profile. In other words, when a Profile instance is
    # serialized, the owner field in the resulting JSON will contain the username
    # of the related User.
    # we rewrite the owner here, that initially was an object (instance of user class)
    # to make it a string 'username' in our response
    # The source argument tells DRF where to get the data for this field from
    # owner refers to the associated User object of the Profile
    # BUT!!! By default, when DRF encounters a foreign key relationship (like your
    # owner field in the Profile model, which is a OneToOneField to the User model),
    # it represents this relationship using the primary key of the related object (id).

    # if I want to make owner an object (User instance)
    # owner = UserSerializer()
    owner = serializers.ReadOnlyField(source='owner.username')
    # This is an example of using a SerializerMethodField. This is a type of field
    # that is used in DRF serializers to add custom fields to your serialized data,
    # where the value of the field is computed by a method on the serializer class
    # SerializerMethodField: This is a read-only field. It is used in a serializer
    # to include some custom or computed data in the serialization output.
    # Dynamic Content: The content of this field is not directly taken from the model
    # instance. Instead, it's determined by a method you define on the serializer.
    is_owner = serializers.SerializerMethodField()
    # The id_following_me field is a custom field that is not directly tied to a model
    # field. Instead, it is calculated at runtime using a method on the serializer class.

    # When an instance of ProfileSerializer is used to serialize a Profile object, the
    # id_following_me field initializes as a SerializerMethodField. This field type tells
    # DRF to call a specific method on the serializer to get the value of the field.
    id_following_me = serializers.SerializerMethodField()

    # Defining the Method: To provide a value for a SerializerMethodField, you define
    # a method on the serializer class with a specific naming pattern: get_<field_name>.
    # For your field is_owner, the method should be named get_is_owner.
    # Method Implementation: This method takes an instance of the model being serialized
    # (in your case, an instance of Profile) and returns the value that should be
    # assigned to the is_owner field in the serialized representation.
    # The value for is_owner is determined by the get_is_owner method. This method
    # takes the profile object (obj) as its argument.
    def get_is_owner(self, obj):
        # The method first retrieves the current HTTP request from the serializer context
        request = self.context['request']
        # The method then compares the user making the request (request.user)
        # with the owner of the profile (obj.owner). If they are the same, it
        # means the current user is the owner of the profile.
        # return request.user == obj.owner
        return request.user == obj.owner

    # The method named get_id_following_me is defined to provide the value for this field
    def get_id_following_me(self, obj):
        # Inside get_id_following_me, the method accesses the current request object from
        # the serializer context. This is necessary to determine the current user making
        # the request
        user = self.context['request'].user
        # The method checks if the current user is authenticated. If not, the method
        # returns None because an unauthenticated user cannot be following anyone.
        if user.is_authenticated:
            # If the user is authenticated, the method queries the Follower model for
            # a relationship where the current user (owner) is following the profile's
            # owner (followed). It uses the .filter() method to search for this and then
            # calls .first() to get the first instance that matches the criteria, if any.
            following = Follower.objects.filter(
                # owner=user: This is a filter condition. owner is a field in the Follower
                # model that refers to the user who is following someone. In this context,
                # user is a variable that typically represents the current authenticated user
                # making the request. So, owner=user means "find (work only with) Follower
                # instances where the owner is the current user.
                # owner=user is essentially looking for Follower instances where the
                # follower (the one who follows someone else) is the current user.

                # followed=obj.owner: This is another filter condition. followed is
                # a field in the Follower model that refers to the user who is being
                # followed. obj is the current instance of the object being serialized
                # by ProfileSerializer. obj.owner refers to the owner of that profile.
                # So, followed=obj.owner means "find Follower instances where the
                # followed user is the owner of the profile being serialized".

                # When you use Follower.objects.filter(owner=user, followed=obj.owner),
                # you're asking, "Show me if the current user is following the owner of
                # this profile instance."

                # followed=obj.owner means "find all the relationships where the owner
                # of this profile is the one being followed".

                # obj is the parameter passed to the method get_id_following_me. It
                # represents the instance of the Profile model that is currently being
                # serialized.

                owner=user, followed=obj.owner
            ).first()
            #     def __str__(self):
            #         return f"{self.owner} {self.followed}"
            print(following) # WE SEE THE RESULT BECAUSE OF THESE TWO LINES ABOVE
            return {'following_id': following.id, 'following_username': following.owner.username} if following else None
        return None

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'content', 'image', 'is_owner', 'id_following_me'
        ]

# user.following.all() fetches all instances of Follower where the specified user
# is the owner (i.e., the one who initiated the following relationship).
# It's a way to get all the users that a specific user is following.

# user.followed.all() fetches all instances of Follower where the specified user is
# the followed (i.e., the one being followed).
# It's a way to get all the users who are following a specific user.
