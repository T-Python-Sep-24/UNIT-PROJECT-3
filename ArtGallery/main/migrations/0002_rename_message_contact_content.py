# Generated by Django 5.1.3 on 2024-12-01 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='message',
            new_name='content',
        ),
    ]
