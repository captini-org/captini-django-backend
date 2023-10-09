from CaptiniAPI import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  
import os
#from compositefk.fields import CompositeForeignKey


from account.models import User

class Topic(models.Model):
    topic_name = models.CharField(max_length=100)
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

#Audit table that will be used to the statistics for the user
class UserTaskScoreStats(models.Model):
    user = models.ForeignKey(User, related_name='user_task_score', on_delete=models.CASCADE)
    task =models.ForeignKey(Task, related_name='task_id_score', on_delete=models.CASCADE)
    score_mean = models.IntegerField(default=0)
    number_tries = models.IntegerField(default=1)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'task'],
                name='unique_user_task'
            )
        ]

### Function that is used to save all the recording keeping track only for the task id and gender
def directory_path(instance, filename):
    path=settings.MEDIA_ROOT+'/{0}/{1}'.format(instance.task.id,filename)
    print(path)
    return path

def example_recording_directory_path(instance, filename):
    return 'examples/task_{0}_{1}'.format(instance.task, instance.gender)


class UserTaskRecording(models.Model):
    user = models.ForeignKey(User, related_name='task_recording', on_delete=models.CASCADE)
    task = models.ForeignKey(Task, related_name='task_recording', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, related_name='task_recording', on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
    score =  models.IntegerField(default=0)
    recording = models.FileField(upload_to = directory_path,default='file_example')
    
    #def save(self, *args, **kwargs):
    # Save the model instance without the 'recording' field
    #    print(*args)
    #    super().save(*args, **kwargs)
        # Save the 'recording' file locally if it's a new instance or the file has changed
        

    
GENDER = [
    ("M", "Male"),
    ("F", "Female")
]
    
class ExampleTaskRecording(models.Model):
    task = models.ForeignKey(Task, related_name='task_example', on_delete=models.CASCADE)
    gender = models.CharField(max_length=6, choices=GENDER, default="M")
    recording = models.FileField(max_length=150, upload_to=example_recording_directory_path)
    time_created = models.DateTimeField(auto_now_add=True)
    


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    if 'ON_HEROKU' in os.environ:
        email_plaintext_message = "{}?token={}".format('https://captini.tullius.dev/api/password_reset/confirm' , reset_password_token.key)
    else:
        email_plaintext_message = "{}?token={}".format('http://127.0.0.1:8000/api/password_reset/confirm' , reset_password_token.key)

    send_mail(
        # title:
        "Password reset for captini",
        # message:
        email_plaintext_message,
        # from:
        "no-reply@tiro.is",
        # to:
        #[reset_password_token.user.email]
        
        # temporary test
        ['tme1@hi.is'],
        fail_silently=False
    )

