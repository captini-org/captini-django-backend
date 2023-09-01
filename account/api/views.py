from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.utils.encoding import force_str
from account.api.serializers import RegistrationSerializer, MyTokenObtainPairSerializer
from account import models
from account.api.serializers import UserSerializer, UserLeaderboardSerializer,DeactivateAccountSerializer,ActivateAccountSerializer,PasswordResetSerializer,PasswordResetConfirmSerializer,ConfirmAccountActivationSerializer, SessionSerializer, TopicUserStatsSerializer, LessonUserStatsSerializer, LessonTasksUserStatsSerializer
from captini.api.permissions import *
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from django_rest_passwordreset.views import ResetPasswordRequestToken
from .serializers import PasswordResetSerializer,PasswordResetConfirmSerializer
from account.models import User, UserSession
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Sum

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
def change_password(request):
    # get password from request data
    pwData = request.data['passwordForm']

    # get username from request data
    userData = request.data['profilForm']
    distinctUsername = userData['username']

    # get account by filtering query set for Users and finding the one with unique username from requestData
    account = models.User.objects.get_queryset().filter(username=distinctUsername).first()

    if request.method == 'POST':
        # if the hashed value of old password from request data matches hashed password stored in user account, replace
        if check_password(pwData['_oldPass'],account.password):
            try:
                account.set_password(pwData['_newPass'])
                account.save()    
                return Response({'message': 'Change password successful!'}, status=status.HTTP_200_OK)
            except Exception as e:
                print("Error {0}".format(e))
                return Response({'error': 'Request to change password failed'})
        else:
            return Response({'error': 'Old password does not match stored password'})
        
        
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
    
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class PasswordResetView(generics.CreateAPIView):
    serializer_class = PasswordResetSerializer
class PasswordResetConfirmView(generics.UpdateAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid = force_str(urlsafe_base64_decode(serializer.validated_data['uid']))
        user = User.objects.get(pk=uid)

        if not default_token_generator.check_token(user, serializer.validated_data['token']):
            return Response({'detail': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({'detail': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class SessionView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SessionSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_object(self):
        return self.request.user
    
class SessionUserDataView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SessionSerializer

    def get_object(self):
        user_id = self.kwargs['pk']
        sessions = UserSession.objects.filter(user_id=user_id)
        total_duration = sessions.aggregate(Sum('duration'))['duration__sum']
        return {'total_duration': total_duration}

    def get(self, request, *args, **kwargs):
        session_data = self.get_object()
        return Response(session_data)



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def deactivate_account(request):
    if request.method == "POST":
        serializer = DeactivateAccountSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                user_id = serializer.validated_data['id']
                user = User.objects.get(pk=user_id)
                user.is_active = False
                user.save()
                
                serializer.save()  # Send the deactivation email
                
                return Response({"message": "Account deactivated successfully."}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": "Failed to deactivate account."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ActivateAccountView(generics.CreateAPIView):
    serializer_class = ActivateAccountSerializer

class ConfirmAccountActivationView(generics.UpdateAPIView):
    serializer_class = ConfirmAccountActivationSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid = force_str(urlsafe_base64_decode(serializer.validated_data['uid']))
        user = User.objects.get(pk=uid)

        if not default_token_generator.check_token(user, serializer.validated_data['token']):
            return Response({'detail': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data['new_password'])
        user.is_active = True 
        user.save()

        return Response({'detail': 'Account has been activated successfully.'}, status=status.HTTP_200_OK)

class TopicUserStats(generics.RetrieveAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = models.User.objects.all()
    serializer_class = TopicUserStatsSerializer
        
class LessonUserStats(generics.RetrieveAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = models.User.objects.all()
    serializer_class = LessonUserStatsSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['topic_id'] = self.kwargs.get('pk2')  # Get the topic ID from the query parameters
        return context
        
class LessonTasksUserStats(generics.RetrieveAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = models.User.objects.all()
    serializer_class = LessonTasksUserStatsSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['lesson_id'] = self.kwargs.get('pk2')  # Get the topic ID from the query parameters
        return context


'''def deactivate_account(request):
    if request.method == "POST":
        try:
            userid = request.data.get("id")
            print(userid)
            user = User.objects.get(pk=userid)
            user.is_active = False
            user.save()
            return Response({"message": "Account deactivated successfully."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "Failed to deactivate account."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
'''
