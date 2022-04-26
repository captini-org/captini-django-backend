from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, UserManager, PermissionsMixin)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.postgres.fields import ArrayField
from .forms import ChoiceArrayField
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import datetime
import uuid

import jwt

from django.conf import settings

# Create your models here.

class UserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")

        if not email:
            raise ValueError("The given email must be set")

        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")



class User(AbstractBaseUser, PermissionsMixin):

    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer."
        ),
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    birthday = models.DateField(auto_now=False, default=datetime.now)
    nationality = models.CharField(max_length=254)
    #spoken_languages = ArrayField(
    #    models.CharField(
    #        max_length=50, blank=True
    #    )
    #)
    progress = ArrayField(
        models.IntegerField
        (
            blank=True
        ), blank=True
    )
    location = models.CharField(max_length=254)
    email = models.EmailField(_("email address"), blank=False, unique=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    @property
    def token(self):
            token = jwt.encode(
                {'username': self.usernames, 'email': self.email,
                    'exp':datetime.utcnow() + timedelta(hours=24)},
                settings.SECRET_KEY, algorithm='HS256')
            
            return token

class TopicNameField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(TopicNameField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower()

class Topic(models.Model):
    topic_name = TopicNameField(max_length=100, default="")
    level = models.IntegerField(default=0)

    class Meta:
        ordering = ['id']
    

class Lesson(models.Model):
    topic = models.ForeignKey(Topic, related_name='lessons', on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    description = models.CharField(max_length=254)

    class Meta:
        ordering = ['id']

class Prompt(models.Model):
    Lesson = models.ForeignKey(Lesson, related_name='prompts', on_delete=models.CASCADE)
    display_id = models.CharField(max_length=25, blank=False, unique=True)
    text = models.CharField(_("prompt text"), max_length=500)
    audio_url = models.CharField(_("audio url"), blank=True, max_length=100)

    class Meta:
        ordering = ['id']

class Flashcard(models.Model):
    Prompt = models.OneToOneField(Prompt, related_name="flashcards", on_delete=models.CASCADE)
    display_id = models.CharField(max_length=25, blank=False, unique=True)
    text = models.CharField(_("flashcard text"),max_length=500, default="", blank=True)

    class Meta:
        ordering = ['id']
