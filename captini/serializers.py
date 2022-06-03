from captini.models import User, Topic, Lesson, Prompt, Task, UserPromptScore
from rest_framework import serializers

from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password



class UserPromptScoreSerializer(serializers.Serializer):

    class Meta:
        model = UserPromptScore
        fields = ['id', 'lesson_topic', 'prompt_identifier', 'score']
        ordering = ['-id']

class UserSerializer(serializers.ModelSerializer):
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
            #"spoken_languages",
            "birthday",
            "score",
            "global_rank",
            "country_rank",
            "progress",
            "user_prompt_score",
        ]
        ordering = ['-id']

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
            'nationality',
            #"spoken_languages",
            'birthday'
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
            birthday=validated_data['birthday']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

class LoginSerializer(serializers.ModelSerializer):

     class Meta:
         model = User
         fields = ('id', 'username', 'password', 'token')

         read_only_fields=['id', 'token']

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)         


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['id', 'prompt_identifier', 'task_text', 'audio_url']
        ordering = ['-id']

class PromptSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True)

    class Meta:
        model = Prompt
        fields = ['id', 'prompt_identifier', 'prompt_description', 'tasks']
        ordering = ['-id']
         

class LessonSerializer(serializers.ModelSerializer):
    prompts = PromptSerializer(many=True)

    class Meta:
        model = Lesson
        fields = ['id', 'description', 'subject', 'prompts']
        ordering = ['-id']
         

class TopicSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True)

    class Meta:
        model = Topic
        fields = ['id', 'topic_name', 'level', 'lessons']
        ordering = ['-id']


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
