from django.db import models

class YieldMinute(models.Model):
    timestamp = models.DateTimeField(primary_key=True)
    yield_minute = models.FloatField(default=0, null=True) 
    yield_day_forecast = models.FloatField(default=0, null=True)

    def __str__(self):
        return str(self.timestamp) + " " + str(self.yield_minute) + " " + str(self.yield_day_forecast)