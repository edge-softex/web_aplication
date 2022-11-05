from django.db import models

class AlertTreshold(models.Model):
    ALERT_TYPES = [
        ('VT', 'Voltage'),
        ('CR', 'Current')
    ]

    id = models.AutoField(primary_key=True)
    alert_type = models.CharField(max_length=2, choices=ALERT_TYPES, default='VT')
    string_number = models.IntegerField(default=0)
    meteorological_value = models.FloatField(default=0)
    treshold_wa_max = models.FloatField(default=0)
    treshold_wa_min = models.FloatField(default=0)
    treshold_ft_max = models.FloatField(default=0)
    treshold_ft_min = models.FloatField(default=0)

    def __str__(self):
        return str(self.id) + " " + self.alert_type + " " + str(self.meteorological_value) + " " + str(self.treshold_wa_max) + " " + str(self.treshold_wa_min) + " " + str(self.treshold_ft_max) + " " + str(self.treshold_ft_min)