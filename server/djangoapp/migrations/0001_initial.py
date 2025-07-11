# Generated by Django 5.2.3 on 2025-06-18 23:28

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarMake',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=30)),
                ('description', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=30)),
                ('dealer_id', models.IntegerField(default=1)),
                ('car_type', models.CharField(choices=[('sedan', 'Sedan'), ('suv', 'SUV'), ('wagon', 'Wagon'), ('pickup', 'Pickup'), ('coupe', 'Coupe'), ('convertible', 'Convertible'), ('hatchback', 'Hatchback'), ('minivan', 'Minivan'), ('sports', 'Sports'), ('luxury', 'Luxury'), ('hybrid', 'Hybrid'), ('electric', 'Electric')], default='sedan', max_length=20)),
                ('year', models.IntegerField(default=2023, validators=[django.core.validators.MaxValueValidator(2023), django.core.validators.MinValueValidator(2015)])),
                ('car_make', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoapp.carmake')),
            ],
        ),
    ]
