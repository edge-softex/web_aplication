# Generated by Django 4.1 on 2022-08-15 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("photovoltaic", "0004_pvstring_remove_pvdata_current_s1_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="PowerForecast",
            fields=[
                ("timestamp", models.DateTimeField(primary_key=True, serialize=False)),
                ("t1", models.FloatField(default=0, null=True)),
                ("t2", models.FloatField(default=0, null=True)),
                ("t3", models.FloatField(default=0, null=True)),
                ("t4", models.FloatField(default=0, null=True)),
                ("t5", models.FloatField(default=0, null=True)),
            ],
        ),
    ]
