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
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
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
    serializer_class = UserListSerializer

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        return Response(user)

class UserDetails(generics.RetrieveUpdateAPIView):

    queryset = User.objects.all()
    serializer_class = UserDetailsSerializer

class UploadAudio(generics.CreateAPIView):

    serializer_class = AudioRecordingsSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.serializer(data=request.data)
        print(request.data)
        if serializer.is_valid:
            recording = serializer.save(user=request.user, task=self.kwargs['pk'])

        try:
            serializer.is_valid(raise_exception=True)
        except AuthenticationError as e:
            raise NotAuthenticatedException(e.args[0])
        
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class LoginViewSet(ModelViewSet, TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RegistrationViewSet(ModelViewSet, TokenObtainPairView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, validated_data):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        res = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        return Response({
            "user": serializer.data,
            "refresh": res["refresh"],
            "token": res["access"]
        }, status=status.HTTP_201_CREATED)

class RefreshViewSet(viewsets.ViewSet, TokenRefreshView):
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

def user_logout(request):
    logout(request)
    return redirect('/api/auth/login/')


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

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

