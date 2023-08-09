import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from account.api.serializers import RegistrationSerializer, MyTokenObtainPairSerializer
from account import models
from account.api.serializers import UserSerializer, UserLeaderboardSerializer
from captini.api.permissions import *
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from django.shortcuts import get_object_or_404
from django_rest_passwordreset.views import ResetPasswordRequestToken
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


@api_view(
    [
        "POST",
    ]
)
def logout_view(request):

    if request.method == "POST":
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(
    [
        "POST",
    ]
)
def registration_view(request):

    if request.method == "POST":
        serializer = RegistrationSerializer(data=request.data)

        data = {}

        if serializer.is_valid():
            account = serializer.save()

            data["response"] = "Registration successful!"
            data["username"] = account.username
            data["email"] = account.email

            # token = Token.objects.get(user=account).key
            # data['token'] = token

            refresh = RefreshToken.for_user(account)
            data["token"] = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }

        else:
            data = serializer.errors

        return Response(data, status=status.HTTP_201_CREATED)

@api_view(["POST"])
def send_mail(request,*args):
    if request.method == 'POST':
        FROM_EMAIL = ['tme1@hi.is']
        print(args)
        TO_EMAIL = 'tme1@hi.is'
        TEMPLATE_ID = 'd-6a4459d36f194d1e862acafb8ae1d4e3'

        message = Mail(
        from_email=FROM_EMAIL,
        to_emails=TO_EMAIL
        )
        
        message.template_id = TEMPLATE_ID
        
        try:
            sg = SendGridAPIClient(os.environ['SENDGRID_API_KEY'])
            response = sg.send(message)
            code, body, headers = response.status_code, response.body, response.headers
            print(f"Response code: {code}")
            print(f"Response headers: {headers}")
            print(f"Response body: {body}")
            print("Dynamic Messages Sent!")
            return Response({'message': 'Sendgrid mail sent successfully!'}, status=status.HTTP_200_OK)
        except Exception as e:
            print("Error {0}".format(e))
            return Response({'error': 'Sendgrid mail failed to send'})
        
@api_view(["POST"])
def change_password(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
        try:    
            print(request.data)
            return Response({'message': 'Request to change password received!'}, status=status.HTTP_200_OK)
        except Exception as e:
            print("Error {0}".format(e))
            return Response({'error': 'Request to change password failed'})

class UserList(generics.ListAPIView):
    permission_classes = [IsAuthenticated] #This was formerly IsAdminUser

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return UserSerializer
        else:
            return UserLeaderboardSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return models.User.objects.all()
        else:
            return models.User.objects.filter(is_superuser=False).order_by('global_rank','date_joined')


class UserDetails(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.User.objects.all()
    serializer_class = UserSerializer
    
class UserUpdateProfileView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = models.User.objects.all()
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
