from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status

from captini.models import User, Topic, Lesson, Prompt, Task, UserPromptScore
from captini.api.serializers import TopicSerializer, LessonSerializer, PromptSerializer, TaskSerializer


# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from rest_framework.viewsets import ModelViewSet
# from rest_framework.permissions import AllowAny
# from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.exceptions import TokenError, InvalidToken






class TopicList(APIView):
    
    def get(self, request):
        topics = Topic.objects.all()
        serializer = TopicSerializer(
            topics, many=True, context={"request": request}
        )
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


# class ChangePasswordView(generics.UpdateAPIView):
#     """
#     An endpoint for changing password.
#     """

#     serializer_class = ChangePasswordSerializer
#     model = User
#     permission_classes = (IsAuthenticated,)

#     def get_object(self, queryset=None):
#         return self.request.user

#     def update(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         serializer = self.get_serializer(data=request.data)

#         if serializer.is_valid():
#             # Check old password
#             if not self.object.check_password(serializer.data.get("old_password")):
#                 return Response(
#                     {"old_password": ["Wrong password."]},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#             # set_password also hashes the password that the user will get
#             self.object.set_password(serializer.data.get("new_password"))
#             self.object.save()
#             response = {
#                 "status": "success",
#                 "code": status.HTTP_200_OK,
#                 "message": "Password updated successfully",
#                 "data": [],
#             }

#             return Response(response)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
