# Generated by Django 5.1.2 on 2024-12-02 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='equipment_category',
            field=models.CharField(choices=[('none', 'No Machine'), ('machine', 'Machine')], max_length=30),
        ),
    ]
