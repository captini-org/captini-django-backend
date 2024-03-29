from django.urls import include, path

# from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from account.api.views import  UserDetails, UserUpdateProfileView, registration_view, UserList, MyTokenObtainPairView,PasswordResetView,PasswordResetConfirmView, change_password, deactivate_account, ActivateAccountView,ConfirmAccountActivationView, SessionView, SessionUserDataView, TopicUserStats, LessonUserStats, LessonTasksUserStats

urlpatterns = [
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetails.as_view(), name='user-details'),
    path('users/<int:pk>/update/', UserUpdateProfileView.as_view(), name='user-update-profile'),
    path('register/', registration_view, name='register'),
    path('api/password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('api/password-confirm/', PasswordResetConfirmView.as_view(), name='password-confirm'),
    path('api/change_password/',change_password, name='change_password'),
    path('users/session/', SessionView.as_view(), name='session'),
    path('users/session/<int:pk>/', SessionUserDataView.as_view(), name='session'),
    path('api/deactivate_account/',deactivate_account, name='deactivate_account'),
    path('api/activate_account/',ActivateAccountView.as_view(), name='activate_account'),
    path('api/reactivate_account/',ConfirmAccountActivationView.as_view(), name='reactivate_account'),
    path("users/<int:pk>/topics/statistics/", TopicUserStats().as_view(), name="topic-user-stats"),
    path("users/<int:pk>/topics/<int:pk2>/statistics/", LessonUserStats().as_view(), name="lesson-user-stats"),
    path("users/<int:pk>/lesson/<int:pk2>/statistics/", LessonTasksUserStats().as_view(), name="lesson-tasks-user-stats"),
]