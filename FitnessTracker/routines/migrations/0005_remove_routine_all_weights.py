# Generated by Django 5.1.2 on 2024-12-04 18:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('routines', '0004_routine_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='routine',
            name='all_weights',
        ),
    ]
