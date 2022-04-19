# Generated by Django 4.0.3 on 2022-04-19 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('captini', '0005_remove_user_spoken_languages_alter_lesson_topic_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flashcard',
            name='Prompt',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='flashcards', to='captini.prompt'),
        ),
        migrations.AlterField(
            model_name='prompt',
            name='Lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prompts', to='captini.lesson'),
        ),
    ]
