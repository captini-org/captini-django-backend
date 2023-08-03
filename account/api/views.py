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
from django_rest_passwordreset.views import PasswordResetView
from .serializers import CustomPasswordResetSerializer

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

class CustomPasswordResetView(PasswordResetView):
    serializer_class = CustomPasswordResetSerializer

    def send_email(self, request, **kwargs):
        # Here, we override the send_email method to use our custom serializer
        # for generating the email content, including the reset URL.

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # You can customize the response as needed.
        return Response({"message": "Password reset email has been sent successfully."}, status=status.HTTP_200_OK)