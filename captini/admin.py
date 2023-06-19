from django.contrib import admin
from .models import Topic, Lesson, Prompt, Task, UserPromptScore, UserTaskRecording, ExampleTaskRecording


class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic_name', 'topic_description', 'number')
    ordering = ['id', 'number']

class LessonsAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic', 'subject', 'description', 'number')
    ordering = ['id', 'number']

class TaskInline(admin.StackedInline):
    model = Task
    list_display = ['id', 'prompt', 'task_text', 'audio_url', 'number']
    ordering = ['id', 'prompt', 'number']
    extra = 0
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'prompt':
            kwargs['queryset'] = Prompt.objects.order_by('prompt_number')
        return super(TaskInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
    

class PromptAdmin(admin.ModelAdmin):
    list_display = ('id', 'lesson', 'prompt_number', 'number')
    ordering = ['id', 'number']
    inlines = [TaskInline]


class UserTaskRecordingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'task', 'recording', 'time_created')
    ordering = ['user', 'task', 'time_created']
    
class ExampleTaskRecordingAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'recording', 'time_created')
    ordering = ['task', 'time_created']


class UserPromptScoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'lesson_topic', 'prompt_number', 'score')
    ordering = ['user', 'prompt_number', 'score']


admin.site.register(Topic, TopicAdmin)
admin.site.register(Lesson, LessonsAdmin)
admin.site.register(Prompt, PromptAdmin)
admin.site.register(UserTaskRecording, UserTaskRecordingAdmin)
admin.site.register(ExampleTaskRecording, ExampleTaskRecordingAdmin)
admin.site.register(UserPromptScore, UserPromptScoreAdmin)
