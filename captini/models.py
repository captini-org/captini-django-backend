from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.


class User(AbstractUser):
    age = models.IntegerField(default=0)
    nationality = models.CharField(max_length=254)
    location = models.CharField(max_length=254)

    def __str__(self):
        return self.username
