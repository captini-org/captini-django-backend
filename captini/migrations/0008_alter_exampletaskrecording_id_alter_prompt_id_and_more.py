# Generated by Django 4.0.3 on 2024-03-15 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('captini', '0007_alter_lesson_id_alter_topic_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exampletaskrecording',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='prompt',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='task',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='userpromptscore',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='usertaskrecording',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='usertaskscorestats',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
