from django.db import models


class Cycle(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    date = models.DateField(auto_now_add=True)
    genetics = models.CharField(max_length=200, blank=True, null=True)
    seedbank = models.CharField(max_length=80, blank=True, null=True)
    fixture = models.CharField(max_length=200, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    day_logs = models.ManyToManyField('DayLog', blank=True, related_name='cycles')

    def __str__(self):
        return self.name


class DayLog(models.Model):
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE, related_name='dayLogs')
    temperature_day = models.FloatField(blank=True, null=True)
    temperature_night = models.FloatField(blank=True, null=True)
    humidity_day = models.FloatField(blank=True, null=True)
    humidity_night = models.FloatField(blank=True, null=True)
    pH = models.FloatField(blank=True, null=True)
    ec = models.FloatField(blank=True, null=True)
    nutrients = models.ManyToManyField('Nutrient', blank=True)
    irrigation = models.FloatField(blank=True, null=True)
    light_height = models.FloatField(blank=True, null=True)
    light_power = models.FloatField(blank=True, null=True)
    calibration = models.BooleanField(default=False, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)


class Nutrient(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name
