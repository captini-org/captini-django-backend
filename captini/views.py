from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import redirect

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
from captini.serializers import UserSerializer, LoginSerializer, RegisterSerializer
import jwt

from django.conf import settings


class UserList(viewsets.ModelViewSet):
    """
    List all users, or create a new user.
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

class UserLogin(generics.GenericAPIView):

    serializer_class = LoginSerializer

    def post(self,request):
        data = request.data
        print(data)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            serializer = self.serializer_class(user)
            login(request, user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


def user_logout(request):
    logout(request)
    return redirect('/users/login')
