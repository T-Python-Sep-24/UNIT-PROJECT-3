# Generated by Django 5.1.3 on 2024-11-30 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='images/avatar.webp', upload_to='images/'),
        ),
    ]
