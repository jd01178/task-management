# Generated by Django 4.2.3 on 2023-07-21 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0013_remove_task_is_personal_task_task_task_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='progress',
            name='progress',
            field=models.IntegerField(choices=[(0, 'Not Started'), (1, 'In Progress'), (2, 'Review'), (3, 'Completed')], default=0),
        ),
    ]
