from django.db import models

class Settings(models.Model):
    id = models.AutoField(primary_key=True)

    fault_vt_percentile = models.IntegerField(default=98)
    warning_vt_percentile = models.IntegerField(default=88)
    delt_vt = models.FloatField(default=0.6)

    fault_cr_percentile = models.IntegerField(default=98)
    warning_cr_percentile = models.IntegerField(default=88)
    delt_cr = models.FloatField(default=5)

    fault_user_active = models.BooleanField(default=True)
    warning_user_active = models.BooleanField(default=True)
    alert_days_active = models.BooleanField(default=False)
    days_left = models.IntegerField(default=7)

    retraining_interval = models.IntegerField(default=3)

    def __str__(self):
        return (str(self.id) + " " + str(self.fault_vt_percentile) + " " + str(self.warning_vt_percentile) + " " + str(self.delt_vt)
            + " " + str(self.fault_cr_percentile) + " " + str(self.warning_cr_percentile) + " " + str(self.delt_cr)
            + " " + str(self.fault_user_active) + " " + str(self.warning_user_active) + + " " + str(self.alert_days_active)
            + " " + str(self.retraining_interval))