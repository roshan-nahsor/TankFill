# Generated by Django 4.2.11 on 2024-05-02 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tank', '0002_remove_tank_fill_type_remove_tank_subscribe_topic_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensordata',
            name='tank_status',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
