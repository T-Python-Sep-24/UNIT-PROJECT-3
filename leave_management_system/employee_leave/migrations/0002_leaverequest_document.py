# Generated by Django 5.1.3 on 2024-11-26 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_leave', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaverequest',
            name='document',
            field=models.FileField(blank=True, null=True, upload_to='leave_documents/'),
        ),
    ]