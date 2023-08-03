from account.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone
from django_rest_passwordreset.serializers import PasswordResetTokenSerializer

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
    
class CustomPasswordResetSerializer(PasswordResetTokenSerializer):
    def get_email_context(self):
        context = super().get_email_context()
        # temporary url
        context["reset_url"] = "http://localhost:4200/api/password_reset/confirm/"
        return context