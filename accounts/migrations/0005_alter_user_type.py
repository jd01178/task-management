# Generated by Django 4.2.3 on 2023-07-27 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_employee_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('EMP', 'Main User'), ('STF', 'Staff')], default='STF', max_length=5),
        ),
    ]
