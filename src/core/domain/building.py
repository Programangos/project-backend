from django.db import models


class Building(models.Model):
    name = models.CharField(max_length=255)
    building_number = models.IntegerField(unique=True)
    description = models.TextField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)

    class Meta:
        db_table = 'building'
        managed = False


class BuildingComment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(
        'core.User',
        on_delete=models.DO_NOTHING,
        db_column='user_id'
    )
    building = models.ForeignKey(
        'core.Building',
        on_delete=models.DO_NOTHING,
        db_column='building_id'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'building_comment'
        managed = False
