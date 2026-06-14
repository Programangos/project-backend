from django.db import models


class AdviceLike(models.Model):
    user = models.ForeignKey(
        'core.User',
        on_delete=models.DO_NOTHING,
        db_column='user_id'
    )
    advice = models.ForeignKey(
        'core.Advice',
        on_delete=models.DO_NOTHING,
        db_column='advice_id'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'advice_like'
        managed = False
