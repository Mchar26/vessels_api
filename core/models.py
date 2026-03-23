from django.db import models


class Vessel(models.Model):
    mmsi = models.CharField(max_length=10, primary_key=True)
    date_entry = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.mmsi} - {self.date_entry}'



class VesselInfo(models.Model):
    mmsi = models.OneToOneField(Vessel, on_delete=models.CASCADE)
    imo = models.CharField(max_length=10, null=True, blank=True)
    vessel_name = models.CharField(max_length=50, null=True, blank=True)
    year_of_build = models.IntegerField(null=True, blank=True)
    flag = models.CharField(max_length=50, null=True, blank=True)
    dwt = models.FloatField(null=True, blank=True)
    teu_capacity = models.FloatField(null=True, blank=True)
    draft = models.FloatField(null=True, blank=True)
    loa = models.FloatField(null=True, blank=True)
    lbp = models.FloatField(null=True, blank=True)
    breadth_extreme = models.FloatField(null=True, blank=True)
    breadth_moulded = models.FloatField(null=True, blank=True)
    vessel_type = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.mmsi} - {self.imo} - {self.vessel_name}'