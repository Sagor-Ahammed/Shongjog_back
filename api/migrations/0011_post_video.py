# Generated by Django 4.1.6 on 2023-03-05 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='post_videos/'),
        ),
    ]
