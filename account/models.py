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
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    path=settings.PHOTOS_URL+'/user/profile_photos/user_{0}/{1}'.format(instance.id, filename)
    if os.path.isfile(path):
        os.remove(path)
        print("Removed Element")
    return 'user/profile_photos/user_{0}/{1}'.format(instance.id, filename) 

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
    birthday = models.DateField(auto_now=False, default=date.today)
    nationality = models.CharField(max_length=254)
    date_joined = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)
    global_rank = models.IntegerField(default=0)
    country_rank = models.IntegerField(default=0)
    native_language = models.CharField(default="english",max_length=50)
    display_language = models.CharField(default="en",max_length=3)
    gender = models.CharField(max_length=6, choices=GENDER, default="M")
    language_level = models.CharField(max_length=6, choices=LANGUAGE_LEVEL, default="L")
    notification_setting_in_app= models.BooleanField(default=False)
    notification_setting_email= models.BooleanField(default=False)
    profile_photo = models.ImageField(upload_to=user_directoryphotos, default="../recordings/puffin.jpg", blank=True)

    def __str__(self):
        return '{} {}'.format(self.id, self.username)



# native language - gender - language level - notification setting - uploading profile photo
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)