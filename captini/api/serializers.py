from captini.models import  Topic, Lesson, Prompt, Task, UserPromptScore, UserTaskRecording, ExampleTaskRecording , UserTaskScore
from rest_framework import serializers
from rest_framework.test import APIRequestFactory
import random

factory = APIRequestFactory()
request = factory.get('/')

class UserPromptScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserPromptScore
        fields = '__all__'

class TaskRecordingSerializer(serializers.ModelSerializer):
    random_score = serializers.SerializerMethodField()

    class Meta:
        model = UserTaskRecording
        fields = '__all__'
        
    def get_random_score(self, obj):
        return random.randrange(0, 100, 5)

    #Override of the cration to save the score inside the DB and modify the user total score 
    def create(self,validated_data):
        print(self)
        print(validated_data)
        score=self.get_random_score(self)
        scoring= {
            'score': score,
            'task_id': validated_data['task'].id,
            'user_id':validated_data['user'].id
        }
        print(scoring)
        print(*validated_data)
        #print(validated_data)
        task_recording=UserTaskRecording.objects.get_queryset().filter( user=validated_data['user'],task=validated_data['task']).first()
        if(task_recording):
            print("Esiste")
            task_recording.recording=validated_data['recording']
        else:
            task_recording=  UserTaskRecording.objects.create(**validated_data)
        score= UserTaskScore.objects.create(**scoring)
        return task_recording

    
class ExampleRecordingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ExampleTaskRecording
        fields = '__all__'
        
class TaskSerializer(serializers.ModelSerializer):
    examples = ExampleRecordingSerializer(many=True, read_only=True, source='task_example')
    
    class Meta:
        model = Task
        fields = '__all__'
        

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
