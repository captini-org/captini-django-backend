from django.urls import path
# from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from account.api.views import UserDetails, registration_view, logout_view, UserList

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:pk>', UserDetails.as_view(), name='user-details'),
    # path('logout/', logout_view, name='logout'),
    path('register/', registration_view, name='register'),
]