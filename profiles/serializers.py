from django.contrib.auth.models import User
from rest_framework import serializers
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
    # it represents this relationship using the primary key of the related object.

    # if I want to make owner an object (User instance)
    # owner = UserSerializer()
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'content', 'image'
        ]

