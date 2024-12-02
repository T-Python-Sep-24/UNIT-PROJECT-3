# Generated by Django 5.1.3 on 2024-12-02 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_skill_profile_skills'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='skills',
        ),
        migrations.DeleteModel(
            name='Skill',
        ),
        migrations.AddField(
            model_name='profile',
            name='skills',
            field=models.TextField(blank=True),
        ),
    ]
