from django.db import models


class User(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password_hash = models.CharField(max_length=255)
    major = models.CharField(max_length=255)
    current_semester = models.IntegerField()
    avatar_url = models.TextField(blank=True, null=True)
    reputation_points = models.IntegerField(default=0)
    title = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    role = models.ForeignKey(
        'core.Role',
        on_delete=models.DO_NOTHING,
        db_column='role_id',
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user'
        managed = False
