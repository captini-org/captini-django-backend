from account.models import User
from captini.models import UserTaskScoreStats, Task, Prompt, Lesson, Topic
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django_rest_passwordreset.serializers import ResetTokenSerializer
from django.contrib.auth.tokens import default_token_generator
from sendgrid.helpers.mail import Mail, HtmlContent
from sendgrid import SendGridAPIClient
import os
from CaptiniAPI.settings import SENDGRID_API_KEY,EMAIL_HOST_USER, RESET_PASSWORD_LINK, TEMPLATE_ID
from django.db.models import Count, Avg, Sum
from dotenv import load_dotenv, find_dotenv
from rest_framework.exceptions import AuthenticationFailed
load_dotenv(find_dotenv())
ACTIVATE_ACCOUNT_LINK = os.environ['ACTIVATE_ACCOUNT_LINK']
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
    completed_tasks = serializers.SerializerMethodField()
    completed_lessons = serializers.SerializerMethodField()
    completed_topics = serializers.SerializerMethodField()
    average_score = serializers.SerializerMethodField()
    total_tasks = serializers.SerializerMethodField()
    total_prompts = serializers.SerializerMethodField()
    total_lessons = serializers.SerializerMethodField()
    total_topics = serializers.SerializerMethodField()
    total_tries = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'birthyear', 'nationality','score', 
                  'global_rank', 'country_rank','native_language', 'display_language', 'gender', 
                  'language_level', 'notification_setting_in_app', 'notification_setting_email', 
                  'profile_photo', 'completed_tasks', 'completed_lessons', 'completed_topics', 'average_score',
                  'total_tasks', 'total_prompts', 'total_lessons', 'total_topics', 'total_tries']
        read_only_fields = ['score', 'global_rank', 'country_rank', 'completed_tasks', 
                            'completed_lessons', 'completed_topics', 'average_score',
                            'total_tests', 'total_prompts', 'total_lessons', 'total_tasks', 'total_topics', 'total_tries']

    def get_completed_tasks(self, obj):
        return UserTaskScoreStats.objects.filter(user_id=obj.id).count()
        #return 1000

    def get_completed_lessons(self, obj):
        # Get all the lessons which have associated prompts
        lessons = Lesson.objects.annotate(prompt_count=Count('prompts'))
        
        completed_lessons = 0
        for lesson in lessons:
            prompts = lesson.prompts.all()
            prompts = prompts.annotate(task_count=Count('tasks'))
            #prompts = lesson.prompts.all().annotate(task_count=Count('tasks'))
            print(f"All prompts for lesson {lesson.id}: {[p.id for p in prompts]}")
            
            all_prompts_completed = True
            print(lesson)
            for prompt in prompts:
                print(f"Checking prompt {prompt.id}")
                completed_tasks_count = UserTaskScoreStats.objects.filter(
                    user_id=obj.id,
                    task__prompt=prompt
                ).count()

                print(f"Completed tasks for prompt {prompt.id}: {completed_tasks_count}/{prompt.task_count}")
                    
                if completed_tasks_count != prompt.task_count:
                    print(completed_tasks_count)
                    all_prompts_completed = False
                    break

            if all_prompts_completed:
                completed_lessons += 1

        for lesson in Lesson.objects.all():
            prompts = lesson.prompts.all()
            print(f"Lesson: {lesson.id}, Prompts: {[p.id for p in prompts]}")

        return completed_lessons

    def get_completed_topics(self, obj):

        topics = Topic.objects.annotate(lesson_count=Count('lessons'))

        completed_topics = 0
        for topic in topics:
            # Get all the lessons which have associated prompts
            lessons = topic.lessons.all()

            completed_lessons = 0
            for lesson in lessons:
                prompts = lesson.prompts.all().annotate(task_count=Count('tasks'))
                print(f"All prompts for lesson {lesson.id}: {[p.id for p in prompts]}")
                
                all_prompts_completed = True
                for prompt in prompts:
                    completed_tasks_count = UserTaskScoreStats.objects.filter(
                        user_id=obj.id,
                        task__prompt=prompt
                    ).count()

                    print(f"Completed tasks for prompt {prompt.id}: {completed_tasks_count}/{prompt.task_count}")
                        
                    if completed_tasks_count != prompt.task_count:
                        all_prompts_completed = False
                        break

                if all_prompts_completed:
                    completed_lessons += 1

            # Check if all lessons for a topic have been completed
            if completed_lessons == lessons.count():
                completed_topics += 1

        return completed_topics


    def get_average_score(self, obj):
        avg_score = UserTaskScoreStats.objects.filter(user_id=obj.id)\
            .aggregate(Avg('score_mean'))['score_mean__avg']

        return avg_score if avg_score is not None else 0  # Or any other default value you want
    
    def get_total_tries(self, obj):
        total_tries = UserTaskScoreStats.objects.filter(user_id=obj.id)\
            .aggregate(Sum('number_tries'))['number_tries__sum']

        return total_tries if total_tries is not None else 0
    
    def get_total_tasks(self, obj):
        total_tasks = Task.objects.count()

        return total_tasks
    
    def get_total_prompts(self, obj):
        total_prompts = Prompt.objects.count()

        return total_prompts
    
    def get_total_lessons(self, obj):
        total_lessons = Lesson.objects.count()

        return total_lessons
    
    def get_total_topics(self, obj):
        total_topics = Topic.objects.count()

        return total_topics

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
        if not self.user.is_active:
            return AuthenticationFailed('Account is not activated', code='account_not_activated')
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

        message = Mail(
            from_email= EMAIL_HOST_USER,  # Sender's email
            to_emails=self.validated_data['email'],  # Recipient's email
            subject='Password reset link for CAPTinI',
        )
        
        message.template_id = TEMPLATE_ID
        message.dynamic_template_data = {
            "reset_link": reset_link
        }
        try:
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            response = sg.send(message)
        except Exception as e:
            print(str(e))

class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField()

class DeactivateAccountSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def validate_uid(self, value):
        try:
            user = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("No user found with this id.")
        return value

    def save(self):
        user = User.objects.get(id=self.validated_data['id'])
        email_content = HtmlContent(f"""
            <p>Hello {user.username},</p>
            <p>This email confirms that your CAPTinI account has been temporarily deactivated.</p>
            <p>We are really sorry to see you go, but thanks for giving us a try.</p>
            <h2>Make a mistake? Having second thoughts?</h2>
            <p>If you believe that this cancellation is an error, or you have any other questions, please contact support. You can also try to login with your last used credentials and follow the required steps to reactivate your account.</p>
            <p>Thank you again for being a customer.</p>
            <p>The crew team from CAPTinI.</p>
        """)
        message = Mail(
            from_email=EMAIL_HOST_USER,  # Sender's email
            to_emails=user.email,  # Recipient's email
            subject='CAPTinI: Your account has been temporarily deactivated. We´re really sorry to see you go',
            html_content= email_content
            
        )

       
        try:
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            response = sg.send(message)
        except Exception as e:
            print(str(e))

class ActivateAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
  
    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("No user found with this email.")
        return value

    def save(self):
        print(ACTIVATE_ACCOUNT_LINK)
        user = User.objects.get(email=self.validated_data['email'])
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_link = ACTIVATE_ACCOUNT_LINK +f"{uid}/{token}/"

        email_content = HtmlContent(f"""
            <p>Hi {user.username},</p>
            <p>Welcome back</p>
            <p> click  <a href="{activation_link}">here</a> to activate your account  </p>
            <p>Thank you again for being a customer.</p>
            <p>The crew team from CAPTinI.</p>
        """)
        message = Mail(
            from_email=EMAIL_HOST_USER,  # Sender's email
            to_emails=user.email,  # Recipient's email
            subject='CAPTinI: Activate your account',
            html_content= email_content
            
        )
        try:
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            response = sg.send(message)
        except Exception as e:
            print(str(e))

class ConfirmAccountActivationSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField()