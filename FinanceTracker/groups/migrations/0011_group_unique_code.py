# Generated by Django 5.1.3 on 2024-12-03 07:22

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0010_rename_invited_at_groupinvitation_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='unique_code',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
