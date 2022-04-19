from captini.models import User, Topic, Lesson, Flashcard, Prompt
from rest_framework import serializers

from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):

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
            #"spoken_languages",
            "location",
            "birthday",
            "progress",
        ]

class RegisterSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 
            'password', 
            'password2', 
            'email', 
            'first_name', 
            'last_name', 
            "nationality",
            #"spoken_languages",
            "location",
            "birthday"
            ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            age=validated_data['birthday'],
            #spoken_languages=validated_data['spoken_languages'],
            nationality=validated_data['nationality'],
            location=validated_data['location']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

class LoginSerializer(serializers.ModelSerializer):

     class Meta:
         model = User
         fields = ('username', 'password', 'token')

         read_only_fields=['token']

class FlashcardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flashcard
        fields = ['id', 'display_id', 'text']
         

class PromptSerializer(serializers.ModelSerializer):
    flashcards = FlashcardSerializer()

    class Meta:
        model = Prompt
        fields = ['id', 'display_id', 'text', 'audio_url', 'flashcards']
         

class LessonSerializer(serializers.ModelSerializer):
    prompts = PromptSerializer(many=True)

    class Meta:
        model = Lesson
        fields = ['id', 'description', 'subject', 'prompts']
         

class TopicSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True)

    class Meta:
        model = Topic
        fields = ['id', 'topic_name', 'lessons']


    def create(self, validated_data):
        topic_data = validated_data.pop('lessons')
        topic = Topic.objects.create(**validated_data)
        for lesson_data in topic_data:
            Lesson.objects.create(topic=topic, **lesson_data)
        return topic


