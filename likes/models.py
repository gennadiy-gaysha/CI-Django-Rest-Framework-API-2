from django.db import models
from django.contrib.auth.models import User
from posts.models import Post

class Like(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # related_name: This is an attribute you use in models with ForeignKey
    # relationships (or OneToOneField or ManyToManyField relationships). It
    # specifies the name of the reverse relation from the Post model back to
    # the Like model.
    # post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    # means that each Post instance will have access to a list of related Like
    # instances. Specifically, if you have a Post object called post, you can access
    # all related Like objects with post.likes.all().
    # Without specifying a related_name, Django automatically creates one using the
    # name of the related model followed by _set (e.g., like_set), but setting a
    # related_name provides a clearer and more convenient way to access the related
    # objects.
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        # unique_together: This is a model option that's used inside the Meta class
        # of a Django model. It's a list or tuple of lists/tuples that specifies the
        # combination of fields that must be unique when considered together.
        # In your Like model, unique_together = [['owner', 'post']] ensures that a
        # User can only "like" a specific Post once. It prevents duplicate Like
        # instances for the same User and Post combination. In database terms, it
        # creates a unique constraint on the owner and post fields together.
        # This means that if a user tries to create a new Like for a post they've
        # already liked, the database will reject it because it would violate the
        # unique constraint.
        unique_together = [['owner', 'post']]

    def __str__(self):
        return f"{self.owner} {self.post}"

