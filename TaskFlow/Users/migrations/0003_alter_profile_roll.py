# Generated by Django 5.1.3 on 2024-11-30 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Users", "0002_delete_role_alter_profile_roll"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile", name="roll", field=models.CharField(max_length=50),
        ),
    ]
