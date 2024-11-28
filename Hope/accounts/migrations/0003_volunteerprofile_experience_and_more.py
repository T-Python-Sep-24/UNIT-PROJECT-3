# Generated by Django 5.1.3 on 2024-11-28 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_user_organizationprofile_organization_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='volunteerprofile',
            name='experience',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='volunteerprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/'),
        ),
        migrations.AddField(
            model_name='volunteerprofile',
            name='skills',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
