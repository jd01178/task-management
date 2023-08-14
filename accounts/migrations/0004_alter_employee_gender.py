# Generated by Django 4.2.3 on 2023-07-20 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_employee_bio_employee_dob_employee_website'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], default='F', max_length=2, null=True),
        ),
    ]