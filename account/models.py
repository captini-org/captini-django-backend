from datetime import date
from django.db import models
# from django.conf import settings
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractUser


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
    
    def __str__(self):
        return str(self.id, self.username)


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)