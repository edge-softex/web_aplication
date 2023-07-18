# Generated by Django 4.2.1 on 2023-07-03 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photovoltaic', '0022_alter_pvdata_wind_direction'),
    ]

    operations = [
        migrations.CreateModel(
            name='AmbientTemperatureForecast',
            fields=[
                ('timestamp', models.DateTimeField(primary_key=True, serialize=False)),
                ('t1', models.FloatField(default=0, null=True)),
                ('t2', models.FloatField(default=0, null=True)),
                ('t3', models.FloatField(default=0, null=True)),
                ('t4', models.FloatField(default=0, null=True)),
                ('t5', models.FloatField(default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='IrradianceForecast',
            fields=[
                ('timestamp', models.DateTimeField(primary_key=True, serialize=False)),
                ('t1', models.FloatField(default=0, null=True)),
                ('t2', models.FloatField(default=0, null=True)),
                ('t3', models.FloatField(default=0, null=True)),
                ('t4', models.FloatField(default=0, null=True)),
                ('t5', models.FloatField(default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PVModuleTemperatureForecast',
            fields=[
                ('timestamp', models.DateTimeField(primary_key=True, serialize=False)),
                ('t1', models.FloatField(default=0, null=True)),
                ('t2', models.FloatField(default=0, null=True)),
                ('t3', models.FloatField(default=0, null=True)),
                ('t4', models.FloatField(default=0, null=True)),
                ('t5', models.FloatField(default=0, null=True)),
            ],
        ),
    ]