# Generated by Django 4.1.6 on 2023-03-12 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message',
            field=models.BinaryField(),
        ),
    ]