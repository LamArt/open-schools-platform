# Generated by Django 3.2.12 on 2023-03-17 16:58

from django.db import migrations, models
import open_schools_platform.common.services


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0001_initial_squashed_0004_refactoring_history'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to=open_schools_platform.common.services.file_generate_upload_path),
        ),
    ]
