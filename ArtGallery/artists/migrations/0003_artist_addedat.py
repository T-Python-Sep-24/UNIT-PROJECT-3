# Generated by Django 5.1.3 on 2024-12-01 08:59

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artists', '0002_alter_artist_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='addedAt',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
