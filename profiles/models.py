from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    # The upload_to='images/' argument specifies that uploaded images for this
    # field should be stored in the images/ directory in Cloudinary. This path
    # is appended to the base Cloudinary storage location.
    image = models.ImageField(
        upload_to='images/', default='../gennadiy_gaysha_dc8uyh'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s profile"

# Signal Receiver Function (create_profile): This is a function defined to act
# as a receiver for the post_save signal. It has the following parameters:
# sender: The model class that sent the signal (in this case, User).
# instance: The actual instance of the sender that was saved.
# created: A boolean that is True if a new record was created, and False if an
# existing record was updated.
# create_profile function checks if the created argument is True, indicating that
# a new User instance has been created.
# **kwargs: A dictionary that captures any additional keyword arguments.
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance)
# The post_save.connect function is used to connect the create_profile function
# to the post_save signal for the User model.
post_save.connect(create_profile, sender=User)
