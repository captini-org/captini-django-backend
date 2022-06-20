from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from captini import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.


urlpatterns = [
    path("topics/", views.TopicList.as_view(), name="topic-list"),
    path("topics/<int:pk>/", views.TopicDetails.as_view(), name="topic-details"),
    path("lessons/<int:pk>/", views.LessonDetails().as_view(), name="lesson-details"),
#    path("users/<int:pk>/progress", views.userProgress.as_view(), name="user-progress"),
    #path("topics/create/", views.TopicCreate.as_view(), name="topic-create"),
    path("users/", views.UserList.as_view({'get': 'list'})),
    path("users/<int:pk>/", views.UserDetails.as_view(), name="user-detail"),
#    path("users/signup/", views.UserCreate.as_view(), name="user-create"),
#    path("users/login/", views.UserLogin.as_view(), name="user-login"),
    path("users/logout/", views.user_logout, name="user-logout"),
    path('api/change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]

urpatterns = format_suffix_patterns(urlpatterns)