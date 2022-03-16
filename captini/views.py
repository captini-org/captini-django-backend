from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
from captini.models import User
from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from rest_framework import generics

from rest_framework import status
from captini.serializers import UserSerializer, LoginSerializer, LogoutSerializer, RegisterSerializer




class UserList(viewsets.ModelViewSet):
    """
    List all users, or create a new user.
    """
    queryset = User.objects.all()
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

class UserLogin(generics.UpdateAPIView):

    queryset = User.objects.all()
    serializer_class = LoginSerializer

    error_messages = {
        'invalid': "Invalid username or password",
        'disabled': "Sorry, this account is suspended",
    }

    def post(self,request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)

        return Response(status=status.HTTP_200_OK)

class UserLogout(generics.UpdateAPIView):

    queryset = User.objects.all()
    serializer_class = LogoutSerializer


    def post(self,request):
        email = request.POST.get('email')
        user = authenticate(email = email)
        if user is not None:
            if user.is_active:
                logout(request, user)

        return Response(status = status.HTTP_200_OK)
