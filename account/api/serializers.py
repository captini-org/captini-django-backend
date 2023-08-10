from account.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django_rest_passwordreset.serializers import ResetTokenSerializer
from django.contrib.auth.tokens import default_token_generator
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient
import os
from CaptiniAPI.settings import SENDGRID_API_KEY,EMAIL_HOST_USER, RESET_PASSWORD_LINK
class RegistrationSerializer(serializers.ModelSerializer):
    
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2','first_name','last_name','birthyear','nationality']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def save(self):
        
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'error': 'Passwords do not match!'})
        
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'That email already in use!'})
        
        account = User(email=self.validated_data['email'], username=self.validated_data['username'],
        first_name=self.validated_data['first_name'],
        last_name=self.validated_data['last_name'],
        birthyear=self.validated_data['birthyear'],
        nationality=self.validated_data['nationality'])
        account.initialize_ranks()
        account.set_password(password)
        account.save()
        return account
    
class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
    
class UserSerializer(DynamicFieldsModelSerializer):
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'birthyear', 'nationality','score', 'global_rank', 'country_rank','native_language', 'display_language', 'gender', 'language_level', 'notification_setting_in_app', 'notification_setting_email', 'profile_photo']
        read_only_fields = ['score', 'global_rank', 'country_rank']

class UserLeaderboardSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
                'id',
                'is_active',
                'date_joined',
                'country_rank',
                'global_rank',
                'score',
                'last_login',
                'gender',
                'language_level',
                'username',
                'native_language',
                'nationality',
                'profile_photo'
            ]
        read_only_fields = fields
        
        
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        data = super().validate(attrs)

        # Updating the `last_login` field.
        self.user.last_login = timezone.now()
        self.user.save(update_fields=['last_login'])

        # Your custom data
        data.update({
            'user': self.user.username,
            'id': self.user.id,
        })

        return data
    
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("No user found with this email.")
        return value

    def save(self):
        user = User.objects.get(email=self.validated_data['email'])
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = RESET_PASSWORD_LINK +f"{uid}/{token}/"
        TEMPLATE_ID = 'd-492b6c9a72a9447f827f8cfe04b8f4a4'
        
        print(reset_link)
        print(uid)
        print(token)
        message = Mail(
            from_email= EMAIL_HOST_USER,  # Sender's email
            to_emails=self.validated_data['email'],  # Recipient's email
            subject='Password Reset',
        )
        
        message.template_id = TEMPLATE_ID
        message.dynamic_template_data = {
            "reset_link": reset_link
        }
        try:
            print(SENDGRID_API_KEY)
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(str(e))

class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField()