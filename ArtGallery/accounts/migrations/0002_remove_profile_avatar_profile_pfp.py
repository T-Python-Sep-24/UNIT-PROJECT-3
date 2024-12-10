# Generated by Django 5.1.3 on 2024-11-28 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='avatar',
        ),
        migrations.AddField(
            model_name='profile',
            name='pfp',
            field=models.ImageField(default='images/usersPfps/defaultPfp.jpg', upload_to='images/usersPfp/'),
        ),
    ]
