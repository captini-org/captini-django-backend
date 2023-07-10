from captini.models import  Topic, Lesson, Prompt, Task, UserPromptScore, UserTaskRecording, ExampleTaskRecording , UserTaskScoreStats
from account.models import User
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
        return 0#random.randrange(0, 100, 5) 

    #Override of the creation to save the score inside the DB and modify the user total score 
    def create(self,validated_data):
        score=random.randrange(0, 100, 5)
        old_score=0
        scoring= {
            'score_mean': score,
            'task_id': validated_data['task'].id,
            'user_id':validated_data['user'].id,
            'number_tentative' : "1"
        }
        task_recording=UserTaskRecording.objects.get_queryset().filter( user=validated_data['user'],task=validated_data['task']).first()
        if(task_recording):
            task_recording.recording=validated_data['recording']
            old_score= task_recording.score
            task_recording.score=score
            stats=UserTaskScoreStats.objects.get_queryset().filter( user=validated_data['user'],task=validated_data['task']).first()
            stats.score_mean=((stats.score_mean*stats.number_tentative)+score)/(stats.number_tentative+1)
            stats.number_tentative=stats.number_tentative+1
            task_recording.score=score
        else:
            task_recording=  UserTaskRecording.objects.create(score=score,**validated_data)
            stats= UserTaskScoreStats.objects.create(**scoring)

        print(validated_data['user'].score+score-old_score)
        validated_data['user'].score=validated_data['user'].score+score-old_score
        validated_data['user'].save()
        stats.save()
        task_recording.save()
        return score

    
class UserTaskScoreStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTaskScoreStats
        fields = '__all__'

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
