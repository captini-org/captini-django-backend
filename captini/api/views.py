from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from captini.api.permissions import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.parsers import FileUploadParser

from captini.models import (
    Topic,
    Lesson,
    Prompt,
    Task,
    UserTaskRecording,
    ExampleTaskRecording
)
from captini.api.serializers import (
    TopicSerializer,
    LessonSerializer,
    PromptSerializer,
    TaskSerializer,
    TaskRecordingSerializer,
    ExampleRecordingSerializer,
)


# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from rest_framework.viewsets import ModelViewSet
# from rest_framework.permissions import AllowAny
# from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

class TopicList(generics.ListCreateAPIView):
    serializer_class = TopicSerializer
    queryset = Topic.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    # throttle_classes = [ReviewListthrottle, AnonRateThrottle]
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ["review_user__username", "active"]

class TopicDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class LessonList(generics.ListCreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAdminOrReadOnly]
    # throttle_classes = [ReviewListthrottle, AnonRateThrottle]
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ["review_user__username", "active"]

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Lesson.objects.filter(topic=pk)


class LessonDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class PromptList(generics.ListCreateAPIView):
    serializer_class = PromptSerializer
    permission_classes = [IsAdminOrReadOnly]
    # throttle_classes = [ReviewListthrottle, AnonRateThrottle]
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ["review_user__username", "active"]

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Prompt.objects.filter(lesson=pk)


class PromptDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer


class TaskList(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAdminOrReadOnly]
    # throttle_classes = [ReviewListthrottle, AnonRateThrottle]
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ["review_user__username", "active"]

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Task.objects.filter(prompt=pk)


class TaskDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskRecordingUpload(generics.CreateAPIView):
    serializer_class = TaskRecordingSerializer
    #permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        pk = self.kwargs["pk"]
        return UserTaskRecording.objects.filter(user=user, pk=pk)
    
class ExampleRecordingUpload(generics.ListCreateAPIView):
    serializer_class = ExampleRecordingSerializer
    permission_classes = [IsAdminOrReadOnly]


    def get_queryset(self):
        pk = self.kwargs["pk"]
        return ExampleTaskRecording.objects.filter(pk=pk)

class TopicSearch(generics.ListCreateAPIView):
    serializer_class = TopicSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['topic_name']
    search_fields = ['topic_name']

    def get_queryset(self):
        search_pattern = self.request.query_params.get('search')
        if search_pattern:
            return Topic.objects.filter(topic_name__icontains=search_pattern)
        return Topic.objects.all()

class LessonSearch(generics.ListCreateAPIView):
    serializer_class = LessonSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['subject']
    search_fields = ['subject']

    def get_queryset(self):
        search_pattern = self.request.query_params.get('search')
        pk = self.kwargs["pk"]
        if search_pattern:
            return Lesson.objects.filter(subject__icontains=search_pattern,topic=pk)
        return Lesson.objects.filter(topic=pk)