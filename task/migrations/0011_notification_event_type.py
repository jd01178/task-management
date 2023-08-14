# Generated by Django 4.2.3 on 2023-07-21 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0010_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='event_type',
            field=models.CharField(blank=True, choices=[('task_event', 'Task Event'), ('google_calendar_event', 'Google Calendar Event'), ('microsoft_calendar_event', 'Microsoft Calendar Event')], default='task_event', max_length=100, null=True),
        ),
    ]
