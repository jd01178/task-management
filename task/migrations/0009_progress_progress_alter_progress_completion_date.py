# Generated by Django 4.2.3 on 2023-07-21 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0008_externalcalendarevent_calendar_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='progress',
            name='progress',
            field=models.IntegerField(choices=[(0, 'Not Started'), (1, 'In Progress'), (2, 'Completed')], default=0),
        ),
        migrations.AlterField(
            model_name='progress',
            name='completion_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]