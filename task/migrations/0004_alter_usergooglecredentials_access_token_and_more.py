# Generated by Django 4.2.3 on 2023-07-18 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_usergooglecredentials_expiry_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usergooglecredentials',
            name='access_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='usergooglecredentials',
            name='client_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='usergooglecredentials',
            name='client_secret',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='usergooglecredentials',
            name='refresh_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='usergooglecredentials',
            name='token_uri',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]