from django.contrib import admin
from .models import User, Topic, Lesson, Prompt, Task, UserPromptScore, UserTaskRecording
import nested_admin



class TopicAdmin(admin.ModelAdmin):
    pass

class LesosnAdmin(admin.ModelAdmin):
    pass

class PromptAdmin(admin.ModelAdmin):
    pass

class TaskAdmin(admin.ModelAdmin):
    pass

class UserTaskRecordingAdmin(admin.ModelAdmin):
    pass

class UserPromptScoreAdmin(admin.ModelAdmin):
    pass


admin.site.register(Topic, TopicAdmin)
admin.site.register(Lesson, LesosnAdmin)
admin.site.register(Prompt, PromptAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(UserTaskRecording, UserTaskRecordingAdmin)
admin.site.register(UserPromptScore, UserPromptScoreAdmin)
