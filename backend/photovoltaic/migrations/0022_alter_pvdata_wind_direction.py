# Generated by Django 4.2.1 on 2023-06-13 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("photovoltaic", "0021_remove_pvdata_strings"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pvdata",
            name="wind_direction",
            field=models.TextField(default="NONE", null=True),
        ),
    ]
