from django.db import models

class PVString(models.Model):
    ALERT_CHOICES = [
        ('NM', 'Normal'),
        ('WA', 'Warning'),
        ('FT', 'Fault'),
        ('NR', 'Not Rated')
    ]

    name = models.CharField(max_length=1024, primary_key=True)
    timestamp = models.DateTimeField()
    voltage = models.FloatField(default=0, null=True)
    current = models.FloatField(default=0, null=True)
    power = models.FloatField(default=0, null=True)
    voltage_alert = models.CharField(max_length=2, choices=ALERT_CHOICES, default='NM')
    current_alert = models.CharField(max_length=2, choices=ALERT_CHOICES, default='NM')
    string_number = models.IntegerField(default=0)

    def __str__(self):
        return self.name + " " + str(self.voltage) + " " + str(self.current) + " " + str(self.power)