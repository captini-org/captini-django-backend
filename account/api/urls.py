from django.urls import include, path
from . import views

# from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from account.api.views import  UserDetails, UserUpdateProfileView, registration_view, UserList, MyTokenObtainPairView,PasswordResetView,PasswordResetConfirmView

urlpatterns = [
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetails.as_view(), name='user-details'),
    path('users/<int:pk>/update/', UserUpdateProfileView.as_view(), name='user-update-profile'),
    path('register/', registration_view, name='register'),
    path('api/password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('api/password-confirm/', PasswordResetConfirmView.as_view(), name='password-confirm'),
]