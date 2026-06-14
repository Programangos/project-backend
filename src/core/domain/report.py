from django.db import models


class Report(models.Model):
    content_type = models.CharField(max_length=50)
    reference_id = models.IntegerField()

    reporter = models.ForeignKey(
        'core.User',
        on_delete=models.DO_NOTHING,
        db_column='reporter_id'
    )
    reason = models.TextField()
    status = models.CharField(max_length=50, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'report'
        managed = False
