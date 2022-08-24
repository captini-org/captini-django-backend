from captini.models import User, Topic, Lesson, Prompt, Task, UserPromptScore
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from django.contrib.auth.models import update_last_login
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password



factory = APIRequestFactory()
request = factory.get('/')

class UserPromptScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserPromptScore
        fields = ['id', 'lesson_topic', 'prompt_identifier', 'score']
        ordering = ['-id']

class UserDetailsSerializer(serializers.ModelSerializer):
    user_prompt_score = UserPromptScoreSerializer(many=True)

    class Meta:
        model = User
        fields = [
            "id",
            "url",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
            "nationality",
            "birthday",
            "score",
            "global_rank",
            "country_rank",
            "user_prompt_score",
        ]
        ordering = ['-id']


# class UserListSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = [
#             "id",
#             "url",
#             "username",
#             "email",
#             "first_name",
#             "last_name",
#         ]
#         ordering = ['-id']


# class ChangePasswordSerializer(serializers.Serializer):
#     model = User

#     """
#     Serializer for password change endpoint.
#     """
#     old_password = serializers.CharField(required=True)
#     new_password = serializers.CharField(required=True)


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = "__all__"

class PromptSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Prompt
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    prompts = PromptSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = "__all__"


class TopicSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = "__all__"


    #def create(self, validated_data):
    #    topic_data = validated_data.pop('lessons')
    #    topic = Topic.objects.create(**validated_data)
    #    for lesson_data in topic_data:
    #        Lesson.objects.create(topic=topic, **lesson_data)
    #    return topic

#class LessonsCompletedSerializer(serializers.ModelSerializer):
#    user = request.user
#    lesson_id_list = user.get('progress')
#    print(lesson_id_list)
#    prompts = PromptSerializer(many=True)

#    class Meta:
#        model = Lesson
#        fields = ['id', 'subject', 'description', 'prompts']
#
