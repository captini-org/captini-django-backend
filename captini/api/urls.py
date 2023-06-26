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
    path("lessons/<int:pk>/prompts/", views.PromptList().as_view(), name="prompt-list"),
    path("prompts/<int:pk>/", views.PromptDetails().as_view(), name="prompt-details"),
    path("prompts/<int:pk>/tasks/", views.TaskList().as_view(), name="task-list"),
    path("tasks/<int:pk>/", views.TaskDetails().as_view(), name="task-details"),
    path("tasks/<int:pk>/upload/", views.TaskRecordingUpload().as_view(), name="recording-upload"),
    path("tasks/<int:pk>/upload-example/", views.ExampleRecordingUpload().as_view(), name="example-upload"),
    path('account/users/', views.UserListLeaderboard.as_view(), name='user-list'),
]

urpatterns = format_suffix_patterns(urlpatterns)