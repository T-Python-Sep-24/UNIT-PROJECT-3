# Generated by Django 5.1.2 on 2024-11-27 16:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='language',
            name='level',
        ),
    ]
