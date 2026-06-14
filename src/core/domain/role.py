from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'role'
        managed = False

    def __str__(self):
        return self.name
