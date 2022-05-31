from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import redirect


# Create your views here.
from captini.models import User, Topic
from rest_framework import status
from django.http import Http404, request
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from rest_framework import generics

from rest_framework import status
from captini.serializers import *
import jwt

from django.conf import settings


class TopicList(generics.ListAPIView):
    serializer_class = TopicSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned topic to a given user,
        by filtering against a `topic` query parameter in the URL.
        """
        queryset = Topic.objects.all()
        topic = self.request.query_params.get('topic_name')
        print(topic)
        if topic is not None:
            queryset = queryset.filter(topic_name__iexact=topic)
        return queryset

class TopicDetails(generics.RetrieveAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

   
#class TopicCreate(generics.CreateAPIView):
#    queryset = Topic.objects.all()
#    serializer_class = TopicSerializer

class LessonDetails(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class UserList(viewsets.ModelViewSet):
    """
    List all users
    """
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        return Response(user)

class UserDetails(generics.RetrieveAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserCreate(generics.CreateAPIView):
    
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

#class UserProgress(generics.ListAPIView):
#    lesson_id_list = self.request.user.lesson_id_list
#    print(lesson_id_list)
#    queryset = Lesson.objects.filter(pk__in=lesson_id_list)
#    serializer_class = LessonSerializer

class UserLogin(generics.GenericAPIView):

    serializer_class = LoginSerializer

    def post(self,request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            serializer = self.serializer_class(user)
            print(serializer.data)
            login(request, user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


def user_logout(request):
    logout(request)
    return redirect('/users/login')


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

