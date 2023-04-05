from django.db import models
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  
import os

from account.models import User

class TopicNameField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(TopicNameField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower()

class Topic(models.Model):
    topic_name = TopicNameField(max_length=100)
    topic_description = models.TextField(max_length=254)
    number = models.IntegerField(default=0)
    
    def __str__(self):
        return self.topic_name
    

class Lesson(models.Model):
    topic = models.ForeignKey(Topic, related_name='lessons', on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    description = models.TextField(max_length=254)
    number = models.IntegerField(default=0)

    def __str__(self):
        return self.subject

class Prompt(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='prompts', on_delete=models.CASCADE)
    prompt_number = models.CharField(max_length=25, blank=False, unique=True)
    flashcard_text = models.TextField(max_length=500, default="", blank=True)
    number = models.IntegerField(default=0)

    def __str__(self):
        return self.prompt_number

class Task(models.Model):
    prompt = models.ForeignKey(Prompt, related_name='tasks', on_delete=models.CASCADE)
    task_text = models.CharField(max_length=255)
    audio_url = models.CharField(blank=True, max_length=500)
    number = models.IntegerField(default=0)

    def __str__(self):
        return self.task_text

class UserPromptScore(models.Model):
    user = models.ForeignKey(User, related_name='user_prompt_score', on_delete=models.CASCADE)
    lesson_topic = models.CharField(max_length = 255, blank=False)
    prompt_number = models.CharField(max_length=25, blank=False, unique=True)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.prompt_number

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class UserTaskRecording(models.Model):
    user = models.ForeignKey(User, related_name='task_recording', on_delete=models.CASCADE)
    task = models.ForeignKey(Task, related_name='task_recording', on_delete=models.CASCADE)
    recording = models.FileField(upload_to=user_directory_path)
    time_created = models.DateTimeField(auto_now_add=True)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    if 'ON_HEROKU' in os.environ:
        email_plaintext_message = "{}?token={}".format('https://captini.tullius.dev/api/password_reset/confirm' , reset_password_token.key)
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
