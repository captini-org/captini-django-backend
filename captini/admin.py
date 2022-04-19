from django.contrib import admin
from .models import User, Topic, Lesson, Prompt, Flashcard
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin


# Register your models here.

class UserAdmin(admin.ModelAdmin, DynamicArrayMixin):
    pass

#class PromptInline(admin.TabularInline):
#    model = Prompt

#class LessonInline(admin.TabularInline):
#    model = Lesson
#
#    inlines = [PromptInline]

class TopicAdmin(admin.ModelAdmin):
    pass

class PromptAdmin(admin.ModelAdmin):
    pass

class LessonAdmin(admin.ModelAdmin):
    pass

class FlashcardAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Prompt, PromptAdmin)
admin.site.register(Flashcard, FlashcardAdmin)
