# Generated by Django 5.1.3 on 2024-11-26 19:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_leave', '0003_alter_leaverequest_employee'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='leaverequest',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='manager_leave_requests', to=settings.AUTH_USER_MODEL),
        ),
    ]
