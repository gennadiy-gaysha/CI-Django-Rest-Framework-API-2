from django.db import models
from django.contrib.auth.models import User


class Follower(models.Model):
    # owner: This represents the user who is initiating the follow action.
    # In the context of a social network, the owner is the "follower". This
    # is the person who wants to follow someone else's updates.

    # The related_name='following' implies that if you have a User instance
    # and you access user.following, you will get a list of Follower instances
    # where this user is the owner.

    # The user.following would not directly give you a list of users that the
    # owner (follower) is following. Instead, it would give you a list of
    # Follower instances where the owner is the current user.
    # Each Follower instance contains a reference to the followed, which is the
    # user that is being followed. So, to get a list of users that the owner is
    # following, you would need to iterate over the user.following queryset and
    # access the followed attribute for each instance.
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    # followed: This represents the user that is being followed. In other words,
    # this is the account whose updates will be shown to the owner.

    # The related_name='followed' implies that if you have a User instance and
    # you access user.followed, you will get a list of Follower instances where
    # this user is the followed.

    # if some_user has followers, you would access them like this:
    # followers = some_user.followed.all()

    # Here, some_user.followed.all() retrieves all the Follower instances where
    # some_user is the one being followed (followed). However, each item in
    # followers is still a Follower instance, not a User instance.

    # !!!
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed')
    created_at = models.DateTimeField(auto_now_add=True)
    # To put it into a real-world context, if user A (the owner) follows user B
    # (the followed), user A is the follower, and user B is the one being followed.
    class Meta:
        ordering = ['-created_at']
        # The unique_together constraint ensures that a User can only follow another
        # User once (i.e., a user cannot follow the same user multiple times).
        unique_together=[['owner', 'followed']]

    def __str__(self):
        return f"{self.owner} {self.followed}"

    # In other words, when followed comes first, it's a name of the field,
    # otherwise it is a related name.
    # In Django ORM (Object-Relational Mapping):
    # Field Name: When you use followed first (as in follower_instance.followed),
    # you're referring to the field name on the Follower model. This is the actual
    # column in the Follower table that stores the reference to the User instance
    # being followed.
    # Related Name: When you access the User model and use .followed (as in
    # user_instance.followed.all()), you're using the related_name of the ForeignKey
    # relationship. This related_name allows you to access the reverse relationship
    # from the User model to the Follower model to retrieve all Follower instances
    # where the User instance is the one being followed.
    # So in summary, followed is the name of the field when you are accessing it
    # directly from an instance of the Follower model. When you are accessing the
    # reverse relationship from an instance of the User model, you use the
    # related_name (followed in this case, as defined in your model).

