# Generated by Django 4.0.3 on 2023-08-11 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_alter_user_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='native_language',
            field=models.CharField(default='en', max_length=50),
        ),
    ]