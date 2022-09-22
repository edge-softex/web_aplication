from django.db import models

from .pvstring import PVString

class PVData(models.Model):
    timestamp = models.DateTimeField(primary_key=True)
    irradiance = models.FloatField(default=0, null=True)
    temperature_pv = models.FloatField(default=0, null=True)
    temperature_amb = models.FloatField(default=0, null=True)
    power_avg = models.FloatField(default=0, null=True)
    strings = models.ManyToManyField(PVString)

    def __str__(self):
        return str(self.timestamp) + " " + str(self.irradiance) + " " + str(self.temperature_pv) + " " + str(self.temperature_amb) + " " + str(self.power_avg)