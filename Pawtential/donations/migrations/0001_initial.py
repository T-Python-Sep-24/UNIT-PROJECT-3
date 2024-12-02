# Generated by Django 5.1.3 on 2024-12-01 09:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DonationRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('donation_type', models.CharField(choices=[('food', 'Food'), ('supplies', 'Supplies'), ('medical', 'Medical'), ('other', 'Other')], max_length=20)),
                ('amount_requested', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('date_requested', models.DateTimeField(auto_now_add=True)),
                ('fulfilled', models.BooleanField(default=False)),
                ('shelter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donation_requests', to='accounts.shelter')),
            ],
        ),
    ]
