# Generated by Django 5.0.6 on 2024-06-20 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stackusers', '0002_profile_bio_profile_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]