from django.db import models


class Notice(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=255)
    is_official = models.BooleanField(default=False)
    expiration_date = models.DateField(null=True)
    user = models.ForeignKey(
        'core.User',
        on_delete=models.DO_NOTHING,
        db_column='user_id'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notice'
        managed = False


class NoticeLike(models.Model):
    user = models.ForeignKey(
        'core.User',
        on_delete=models.DO_NOTHING,
        db_column='user_id'
    )
    notice = models.ForeignKey(
        'core.Notice',
        on_delete=models.DO_NOTHING,
        db_column='notice_id'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notice_like'
        managed = False
        unique_together = ('user', 'notice')

