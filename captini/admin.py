from django.contrib import admin
from .models import Topic, Lesson, Prompt, Task, UserPromptScore, UserTaskRecording



class TopicAdmin(admin.ModelAdmin):
    list_display = ('topic_name', 'topic_description', 'level')

class LessonsAdmin(admin.ModelAdmin):
    list_display = ('topic', 'subject', 'description')


class PromptAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'prompt_number')


class TaskAdmin(admin.ModelAdmin):
    list_display = ('prompt', 'prompt_number', 'task_text', 'audio_url')


class UserTaskRecordingAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'recording', 'time_created')


class UserPromptScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson_topic', 'prompt_number', 'score')


admin.site.register(Topic, TopicAdmin)
admin.site.register(Lesson, LessonsAdmin)
admin.site.register(Prompt, PromptAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(UserTaskRecording, UserTaskRecordingAdmin)
admin.site.register(UserPromptScore, UserPromptScoreAdmin)
