# Generated by Django 4.2.1 on 2023-10-03 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photovoltaic', '0024_powerforecast_power_avg'),
    ]

    operations = [
        migrations.AddField(
            model_name='aialgorithm',
            name='path',
            field=models.CharField(default='lstm/model.h5', max_length=1000),
        ),
    ]