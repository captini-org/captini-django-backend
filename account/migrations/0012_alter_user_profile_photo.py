# Generated by Django 4.0.3 on 2023-08-03 13:20
# Generated by Django 4.0.3 on 2023-08-08 10:51

import account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_alter_user_gender_alter_user_native_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_photo',
            field=models.ImageField(blank=True, default='../recordings/user/profile_photos/puffin.jpg', upload_to=account.models.user_directoryphotos),
        ),
    ]
