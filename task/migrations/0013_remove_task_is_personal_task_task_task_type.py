# Generated by Django 4.2.3 on 2023-07-21 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0012_task_start_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='is_personal_task',
        ),
        migrations.AddField(
            model_name='task',
            name='task_type',
            field=models.CharField(choices=[('personal', 'Personal'), ('work', 'Work')], default='work', max_length=100),
        ),
    ]