# Generated by Django 5.0.6 on 2024-06-10 14:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_image_upload', '0003_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='profile',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='images', to='app_image_upload.profile'),
        ),
    ]