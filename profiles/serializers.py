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


    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'content', 'image', 'is_owner',
        ]

