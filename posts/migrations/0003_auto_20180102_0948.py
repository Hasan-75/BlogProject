# Generated by Django 2.0 on 2018-01-02 03:48

from django.db import migrations, models
import posts.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, default=None, height_field='height_field', null=True, upload_to=posts.models.uploadLocation, width_field='width_field'),
        ),
    ]