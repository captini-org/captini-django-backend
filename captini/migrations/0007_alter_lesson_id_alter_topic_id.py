# Generated by Django 4.0.3 on 2024-03-15 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('captini', '0006_alter_topic_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='topic',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
