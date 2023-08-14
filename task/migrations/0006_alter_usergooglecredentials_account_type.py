# Generated by Django 4.2.3 on 2023-07-19 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0005_alter_usergooglecredentials_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usergooglecredentials',
            name='account_type',
            field=models.CharField(choices=[('google_calendar', 'Google Calendar'), ('microsoft_calendar', 'Microsoft Calendar')], default='google_calendar', max_length=100),
        ),
    ]
