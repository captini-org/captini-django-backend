from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from captini.api import views
# from rest_framework_simplejwt import views as jwt_views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.


urlpatterns = [
    path("topics/", views.TopicList.as_view(), name="topic-list"),
    path("topics/<int:pk>/", views.TopicDetails.as_view(), name="topic-details"),
    path("lessons/<int:pk>/", views.LessonDetails().as_view(), name="lesson-details"),
    path("topics/<int:pk>/lessons/", views.LessonList().as_view(), name="lesson-list"),
#    path("users/<int:pk>/progress", views.userProgress.as_view(), name="user-progress"),
    #path("topics/create/", views.TopicCreate.as_view(), name="topic-create"),
    # path("users/", views.UserList.as_view({'get': 'list'})),
    # path("users/<int:pk>/", views.UserDetails.as_view(), name="user-detail"),
#    path("users/signup/", views.UserCreate.as_view(), name="user-create"),
#    path("users/login/", views.UserLogin.as_view(), name="user-login"),
    # path("api/auth/logout/", views.user_logout, name="user-logout"),
    # path('api/change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    # path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    # path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]

urpatterns = format_suffix_patterns(urlpatterns)