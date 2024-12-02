# Generated by Django 5.1.2 on 2024-12-02 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0004_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='price_range',
            field=models.CharField(choices=[('$', 'Low'), ('$$', 'Medium'), ('$$$', 'High'), ('$$$$', 'Luxury')], default='$$', help_text="Price range of the artist's services", max_length=4),
        ),
    ]
