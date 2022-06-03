from django import forms
from django.contrib import admin
from .models import User, Topic, Lesson, Prompt, Task, UserPromptScore
from django.contrib.auth.forms import ReadOnlyPasswordHashField
import nested_admin


from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin


# Register your models here.

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 
            'password', 
            'password2', 
            'email', 
            'first_name', 
            'last_name', 
            'nationality',
            #"spoken_languages",
            'birthday'
            ]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 
            'first_name', 
            'last_name', 
            'nationality',
            #"spoken_languages",
            'birthday',
            'is_active', 'is_superuser')

    def clean_password(self):
        return self.initial["password"]

class UserAdmin(admin.ModelAdmin, DynamicArrayMixin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'birthday', 'is_superuser')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'birthday', 'nationality')}),
        ('Permissions', {'fields': ('is_superuser',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'birthday', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()  # type: Set[str]

        if not is_superuser:
            disabled_fields |= {
                'username',
                'is_superuser',
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form

#class PromptInline(admin.TabularInline):
#    model = Prompt

#class LessonInline(admin.TabularInline):
#    model = Lesson
#
#    inlines = [PromptInline]

class TaskInline(nested_admin.NestedTabularInline):
    model = Task
    extra = 0

class PromptInline(nested_admin.NestedTabularInline):
    model = Prompt
    inlines = [TaskInline]
    extra = 0

class LessonInline(nested_admin.NestedTabularInline):
    model = Lesson
    inlines = [PromptInline]

class TopicAdmin(nested_admin.NestedModelAdmin):

    inlines = [LessonInline]

class UserPromptScoreAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(UserPromptScore, UserPromptScoreAdmin)
