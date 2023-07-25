from datetime import date
import os
from CaptiniAPI import settings
from django.db import models
# from django.conf import settings
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractUser

GENDER = [
    ("M", "Male"),
    ("F", "Female"),
    ("N", "NotIdentified"),
]
LANGUAGE_LEVEL = [
    ("L", "Low"),
    ("M", "Medium"),
    ("H", "High"),
]


def user_directoryphotos(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/profilephoto<ext>
    uniform_name = 'profilephoto'+os.path.splitext(filename)[1]
    return 'user/profile_photos/user_{0}/{1}'.format(instance.id, uniform_name) 


class User(AbstractUser):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """

    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=550)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    birthyear = models.IntegerField(default=0)
    nationality = models.CharField(max_length=254)
    date_joined = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)
    global_rank = models.IntegerField(default=0)
    country_rank = models.IntegerField(default=0)
    native_language = models.CharField(default="English",max_length=50)
    display_language = models.CharField(default="en",max_length=3)
    gender = models.CharField(max_length=6, choices=GENDER, default="N")
    language_level = models.CharField(max_length=6, choices=LANGUAGE_LEVEL, default="L")
    notification_setting_in_app= models.BooleanField(default=False)
    notification_setting_email= models.BooleanField(default=False)
    profile_photo = models.ImageField(upload_to=user_directoryphotos, default="../recordings/user/profile_photos/puffin.jpg", blank=True)

    def save(self, *args, **kwargs):
        '''overrides tendency in django to add hexadecimal in file name to prevent overwriting of file with same name'''
        try:
            this = User.objects.get(id=self.id)
            if this.profile_photo != self.profile_photo:
                this.profile_photo.delete()
        except: pass
        super(User, self).save(*args, **kwargs)


    def initialize_ranks(self):
        # Get the highest global rank from existing users or default to 0 if no users exist
        lowest_global_rank = User.objects.aggregate(models.Max('global_rank'))['global_rank__max'] or 0

        # Get the highest country rank from existing users or default to 0 if no users exist
        lowest_country_rank = User.objects.aggregate(models.Max('country_rank'))['country_rank__max'] or 0

        # Set the new user's global_rank and country_rank to one more than the lowest ranks
        self.global_rank = lowest_global_rank + 1
        self.country_rank = lowest_country_rank + 1

    def __str__(self):
        return '{} {}'.format(self.id, self.username)



# native language - gender - language level - notification setting - uploading profile photo
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)