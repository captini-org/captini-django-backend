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
from django.db.models import Max
from django.db import transaction
import random
import logging
factory = APIRequestFactory()
request = factory.get('/')

class UserPromptScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserPromptScore
        fields = '__all__'

class TaskRecordingSerializer(serializers.ModelSerializer):
    recording = serializers.FileField()

    class Meta:
        model = UserTaskRecording
        fields = ['recording', 'user', 'task', 'lesson']

    #Opening connection
    def openConnection(self):
        self.response_event = threading.Event()
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='connector_rabbitmq_1'))
        self.channel = self.connection.channel()
        self.session_id= str(uuid.uuid4())

    def format_exercise_text(self,exercise_text):
        # Remove '.', ';', ',', and '-' characters and convert to lowercase
        formatted_text = exercise_text.replace('.', '').replace(';', '').replace(',', '').replace('-', '').replace('–', '').replace('?', '').replace('!', '').lower()
        # Remove extra spaces
        formatted_text = ' '.join(formatted_text.split())
        return formatted_text

    def takeScoreRecording(self,validated_data, filename, recording_id):
        self.openConnection()
        formatted_text = self.format_exercise_text(validated_data['task'].task_text)
        message_data = {
            "audio_path": filename,
            "session_id": self.session_id,
            "text_id": validated_data['task'].id,
            "text" : formatted_text,
            "speaker_id": validated_data['user'].id,
            "recording_id": recording_id
        }
        logging.info(f"printing {json.dumps(message_data)}")

        #Send Message
        routing_key = 'SYNC_SPEECH_INPUT'
        self.channel.basic_publish(
            exchange="captini",
            routing_key=routing_key,
            body=json.dumps(message_data)
        )
        return 1, []
        
    def callback(self, ch, method, properties, body):
        if properties.correlation_id == self.session_id:
            response_data = json.loads(body)
            print(response_data)
            self.response_event.set()
        ch.close()

    def close_connection(self):
        self.connection.close()

    def saveRecordingLocally(self,validated_data):
        name=f"{validated_data['user'].gender}{validated_data['task'].id}{validated_data['recording'].name}"
        filename = default_storage.get_available_name(name)
        default_storage.save(filename, validated_data['recording'])
        return filename

    def create(self, validated_data):
        '''
        filename=self.saveRecordingLocally(validated_data)
        score, errors = self.takeScoreRecording(validated_data,filename)
        '''
        old_score = 0
        task_recording = UserTaskRecording.objects.filter(user=validated_data['user'], task=validated_data['task']).aggregate(Max('score'))
        if task_recording['score__max'] is not None:
            old_score = task_recording['score__max']
        filename = self.saveRecordingLocally(validated_data)
        # TODO: save the userTaskrecording
        # Create UserTaskRecording object
        with transaction.atomic():  
            new_task_recording = UserTaskRecording.objects.create(
                score=0,
                **validated_data
            )

        # Get the recording ID
        recording_id = new_task_recording.id
        score, errors = self.takeScoreRecording(validated_data, filename, recording_id)
        new_task_recording.errors = errors
        return new_task_recording

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
