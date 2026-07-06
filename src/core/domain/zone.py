from django.db import models


class Zone(models.Model):
    zone_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    route = models.CharField(max_length=100, default='/notices')
    bounds_south = models.FloatField()
    bounds_west = models.FloatField()
    bounds_north = models.FloatField()
    bounds_east = models.FloatField()

    class Meta:
        db_table = 'zone'
