# Generated by Django 4.0.5 on 2022-06-18 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0003_door_infomation_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='door_infomation',
            name='img',
            field=models.ImageField(null=True, upload_to='documents'),
        ),
    ]
