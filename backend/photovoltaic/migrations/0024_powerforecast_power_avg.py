# Generated by Django 4.2.1 on 2023-08-01 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("photovoltaic", "0023_ambienttemperatureforecast_irradianceforecast_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="powerforecast",
            name="power_avg",
            field=models.FloatField(default=0, null=True),
        ),
    ]
