# Generated by Django 4.0.3 on 2023-07-20 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_alter_user_profile_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='birthday',
        ),
        migrations.AddField(
            model_name='user',
            name='birthyear',
            field=models.IntegerField(default=0),
        ),
    ]