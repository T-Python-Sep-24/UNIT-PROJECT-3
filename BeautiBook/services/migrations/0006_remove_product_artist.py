# Generated by Django 5.1.2 on 2024-12-02 22:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_alter_product_artist_alter_product_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='artist',
        ),
    ]
