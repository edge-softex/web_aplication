from django.db import models

class IrradianceForecast(models.Model):
    timestamp = models.DateTimeField(primary_key=True)
    t1 = models.FloatField(default=0, null=True)
    t2 = models.FloatField(default=0, null=True)
    t3 = models.FloatField(default=0, null=True)
    t4 = models.FloatField(default=0, null=True)
    t5 = models.FloatField(default=0, null=True)

    def __str__(self):
        return str(self.timestamp) + " " + str(self.t1) + " " + str(self.t2) + " " + str(self.t3) + " " + str(self.t4) + " " + str(self.t5)