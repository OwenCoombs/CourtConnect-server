# Generated by Django 5.0.6 on 2024-06-18 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_image_upload', '0010_image_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='desc',
            field=models.TextField(default=''),
        ),
    ]
