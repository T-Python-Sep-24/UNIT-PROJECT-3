# Generated by Django 5.1.2 on 2024-12-01 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='about',
            new_name='about_user',
        ),
    ]
