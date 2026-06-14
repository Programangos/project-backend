from django.db import models

class Advice(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default='active')
    user = models.ForeignKey(
        'core.User',
        on_delete=models.DO_NOTHING,
        db_column='user_id'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'advice'
        managed = False
