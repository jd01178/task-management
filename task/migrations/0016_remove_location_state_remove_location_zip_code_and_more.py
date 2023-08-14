# Generated by Django 4.2.3 on 2023-07-23 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0015_reminder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='state',
        ),
        migrations.RemoveField(
            model_name='location',
            name='zip_code',
        ),
        migrations.AddField(
            model_name='location',
            name='county',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='postcode',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]