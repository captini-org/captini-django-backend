from captini.models import  Topic, Lesson, Prompt, Task, UserPromptScore, UserTaskRecording
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

factory = APIRequestFactory()
request = factory.get('/')

class UserPromptScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserPromptScore
        fields = '__all__'

class TaskRecordingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserTaskRecording
        fields = '__all__'

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
