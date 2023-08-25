import subprocess
from captini.models import  Topic, Lesson, Prompt, Task, UserPromptScore, UserTaskRecording, ExampleTaskRecording , UserTaskScoreStats
from account.models import User
from rest_framework import serializers
from rest_framework.test import APIRequestFactory
import random
import os
from django.core.files.storage import default_storage
import pika
import json 
import uuid
import threading

factory = APIRequestFactory()
request = factory.get('/')

class UserPromptScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserPromptScore
        fields = '__all__'

class TaskRecordingSerializer(serializers.ModelSerializer):
    recording = serializers.FileField()  # Assuming 'recording' is a CharField in your request

    class Meta:
        model = UserTaskRecording
        fields = ['recording', 'user', 'task', 'lesson']

    #Opening connection
    def openConnection(self):
        self.response_event = threading.Event()
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='connector-rabbitmq-1'))
        self.channel = self.connection.channel()
        self.session_id= str(uuid.uuid4())

    ### N.B. it will be fixed because actually it is running only in localhost when we will run the caitlin script in a real server it will work better
    def calculateScore(self,output):
        tot = 0
        errors=[]
        for line in output.splitlines()[1:]: # skip first line
            if(line[0]!= '\t'):
                words = line.split("\t")
                tot=tot+1
                if(float(words[1]) <-0.2):
                    errors.append(words[0])

        return 100*int((tot-len(errors))/tot),errors

    def takeScoreRecording(self,validated_data, filename):
        print("Open connection")
        self.openConnection()
        print(validated_data['task'].task_text)
        message_data = {
            "audio_path": "recordings/"+filename,
            "session_id": self.session_id,
            "text_id": validated_data['task'].task_text,
            "speaker_id": validated_data['user'].id,
        }
        print(message_data)
        #Send Message
        routing_key = 'SYNC_SPEECH_INPUT'

        self.channel.basic_publish(
            exchange="",
            routing_key=routing_key,
            body=json.dumps(message_data)
        )
        print(f'[x]{message_data} sent to {routing_key}')
        # Wait until you don t get reply
        return 0,""
        
    def callback(self, ch, method, properties, body):
        if properties.correlation_id == self.session_id:
            response_data = json.loads(body)
            print(response_data)
            self.response_event.set()

        ch.close()

    def close_connection(self):
        self.connection.close()

    ### TODO async function with RabbitMQ to save the file with a queue
    def saveRecordingLocally(self,validated_data):
        ###PATH /pronunciation-score-icelandic/recordings/M4demo_j7bpKCm.wav
        name=f"{validated_data['user'].gender}{validated_data['task'].id}{validated_data['recording'].name}"
        filename = default_storage.get_available_name(name)
        default_storage.save(filename, validated_data['recording'])
        return filename

    #Override of the creation to save the score inside the DB and modify the user total score 
    def create(self, validated_data):
        filename=self.saveRecordingLocally(validated_data)
        score, errors = self.takeScoreRecording(validated_data,filename)
        old_score = 0
        scoring = {
            'score_mean': score,
            'task_id': validated_data['task'].id,
            'user_id': validated_data['user'].id,
            'number_tries': "1"
        }

        task_recording = UserTaskRecording.objects.filter(user=validated_data['user'], task=validated_data['task']).first()
        if task_recording:
            old_score = task_recording.score
            task_recording.score = score

            stats = UserTaskScoreStats.objects.filter(user=validated_data['user'], task=validated_data['task']).first()

            if stats:
                stats.score_mean = ((stats.score_mean * stats.number_tries) + score) / (stats.number_tries + 1)
                stats.number_tries += 1
                stats.save()
            else:
                # If the UserTaskScoreStats record doesn't exist, create a new one.
                stats = UserTaskScoreStats.objects.create(
                    user=validated_data['user'],
                    task=validated_data['task'],
                    score_mean=score,
                    number_tries=1
                )
            task_recording.save()

        else:
            if 'recording' in validated_data:
                del validated_data['recording']
            task_recording = UserTaskRecording.objects.create(score=score, **validated_data)
            stats = UserTaskScoreStats.objects.create(**scoring)

        validated_data['user'].score = validated_data['user'].score + score - old_score
        validated_data['user'].save()
        task_recording.errors = errors

        return task_recording

    #Overwrite output
    def to_representation(self, instance):
        return {'task':instance.task.id,'score': instance.score, 'errors': instance.errors}
    
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
