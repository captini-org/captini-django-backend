from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.postgres.fields import ArrayField
from .forms import ChoiceArrayField
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import date
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  
import uuid
import os

import jwt

from django.conf import settings

# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None, **kwargs):
        """Create and return a `User` with an email, phone number, username and password."""
        if username is None:
            raise TypeError('Users must have a username.')
        if email is None:
            raise TypeError('Users must have an email.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')
        if email is None:
            raise TypeError('Superusers must have an email.')
        if username is None:
            raise TypeError('Superusers must have an username.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user



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
    birthday = models.DateField(_("Date"), auto_now=False, default=date.today)
    nationality = models.CharField(max_length=254)
    #spoken_languages = ArrayField(
    #    models.CharField(
    #        max_length=50, blank=True
    #    )
    #)
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
    score = models.IntegerField(_("score"), default=0)
    global_rank = models.IntegerField(_("global rank"), default=0)
    country_rank = models.IntegerField(_("country rank"), default=0)

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
    topic_description = models.TextField(max_length=254, default="")
    level = models.IntegerField(default=0)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.topic_name
    

class Lesson(models.Model):
    topic = models.ForeignKey(Topic, related_name='lessons', on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    description = models.TextField(max_length=254)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.subject

class Prompt(models.Model):
    Lesson = models.ForeignKey(Lesson, related_name='prompts', on_delete=models.CASCADE)
    prompt_number = models.CharField(max_length=25, blank=False, unique=True)
    flashcard_text = models.TextField(_("flashcard text"),max_length=500, default="", blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.prompt_number

class Task(models.Model):
    prompt = models.ForeignKey(Prompt, related_name='tasks', on_delete=models.CASCADE)
    prompt_number = models.CharField(max_length=25, blank=False)
    task_text = models.CharField(_("task text"), max_length=255)
    audio_url = models.CharField(_("audio url"), blank=True, max_length=500)

class UserPromptScore(models.Model):
    user = models.ForeignKey(User, related_name='user_prompt_score', on_delete=models.CASCADE)
    lesson_topic = models.CharField(max_length = 255, blank=False)
    prompt_number = models.CharField(max_length=25, blank=False, unique=True)
    score = models.IntegerField(default=0)

    class Meta:
        ordering = ['prompt_number']

    def __str__(self):
        return self.prompt_number


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):


    
    if 'ON_HEROKU' in os.environ:
        email_plaintext_message = "{}?token={}".format('https://hidden-hamlet-75709.herokuapp.com/api/password_reset/confirm' , reset_password_token.key)
    else:
        email_plaintext_message = "{}?token={}".format('http://127.0.0.1:8000/api/password_reset/confirm' , reset_password_token.key)


    send_mail(
        # title:
        "Password Reset for captini",
        # message:
        email_plaintext_message,
        # from:
        "no-reply@tiro.is",
        # to:
        [reset_password_token.user.email]
    )