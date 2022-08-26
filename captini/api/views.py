from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status

from captini.models import (
    User,
    Topic,
    Lesson,
    Prompt,
    Task,
    UserTaskRecording,
)
from captini.api.serializers import (
    TopicSerializer,
    LessonSerializer,
    PromptSerializer,
    TaskSerializer,
    TaskRecordingSerializer
)


# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from rest_framework.viewsets import ModelViewSet
# from rest_framework.permissions import AllowAny
# from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.exceptions import TokenError, InvalidToken


class TopicList(APIView):
    def get(self, request):
        topics = Topic.objects.all()
        serializer = TopicSerializer(topics, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = TopicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class TopicDetails(APIView):
    def get(self, request, pk):
        try:
            topic = Topic.objects.get(pk=pk)
            print(topic)
        except Topic.DoesNotExist:
            return Response(
                {"Error": "Topic not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = TopicSerializer(topic)
        return Response(serializer.data)

    def put(self, request, pk):
        topic = Topic.objects.get(pk=pk)
        serializer = TopicSerializer(topic, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        topic = Topic.objects.get(pk=pk)
        topic.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LessonList(generics.ListCreateAPIView):
    serializer_class = LessonSerializer
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListthrottle, AnonRateThrottle]
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ["review_user__username", "active"]

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Lesson.objects.filter(topic=pk)


class LessonDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class PromptList(generics.ListCreateAPIView):
    serializer_class = PromptSerializer
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListthrottle, AnonRateThrottle]
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ["review_user__username", "active"]

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Prompt.objects.filter(lesson=pk)


class PromptDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer


class TaskList(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListthrottle, AnonRateThrottle]
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ["review_user__username", "active"]

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Task.objects.filter(prompt=pk)


class TaskDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskRecordingUpload(generics.CreateAPIView):
    serializer_class = TaskRecordingSerializer

    def get_queryset(self):
        user = self.request.user
        pk = self.kwargs["pk"]
        return UserTaskRecording.objects.filter(user=user, pk=pk)


# class UserList(viewsets.ModelViewSet):
#     """
#     List all users
#     """

#     queryset = User.objects.all().order_by("id")
#     serializer_class = UserListSerializer

#     def get(self, request, *args, **kwargs):
#         user = self.get_object()
#         return Response(user)


# class UserDetails(generics.RetrieveAPIView):

#     queryset = User.objects.all()
#     serializer_class = UserDetailsSerializer
#     permission_classes = (IsAuthenticated,)


# class LoginViewSet(ModelViewSet, TokenObtainPairView):
#     serializer_class = serializers.LoginSerializer
#     permission_classes = (AllowAny,)
#     http_method_names = ['post']

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)

#         try:
#             serializer.is_valid(raise_exception=True)
#         except TokenError as e:
#             raise InvalidToken(e.args[0])

#         return Response(serializer.validated_data, status=status.HTTP_200_OK)


# class RegistrationViewSet(ModelViewSet, TokenObtainPairView):
#     serializer_class = serializers.RegisterSerializer
#     permission_classes = (AllowAny,)
#     http_method_names = ['post']

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)

#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         refresh = RefreshToken.for_user(user)
#         res = {
#             "refresh": str(refresh),
#             "access": str(refresh.access_token),
#         }

#         return Response({
#             "user": serializer.data,
#             "refresh": res["refresh"],
#             "token": res["access"]
#         }, status=status.HTTP_201_CREATED)

# class RefreshViewSet(viewsets.ViewSet, TokenRefreshView):
#     permission_classes = (AllowAny,)
#     http_method_names = ['post']

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)

#         try:
#             serializer.is_valid(raise_exception=True)
#         except TokenError as e:
#             raise InvalidToken(e.args[0])

#         return Response(serializer.validated_data, status=status.HTTP_200_OK)

# def user_logout(request):
#     logout(request)
#     return redirect('/api/auth/login/')
