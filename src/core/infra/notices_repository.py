from datetime import date
from django.db.models import Count, Q, Case, When, Value, IntegerField
from core.domain.notice import Notice, NoticeLike
from core.domain.report import Report


class NoticesRepository:
    def get_all(self, search=None):
        today = date.today()
        queryset = Notice.objects.annotate(like_count=Count('noticelike'))
        queryset = queryset.filter(
            Q(expiration_date__isnull=True) | Q(expiration_date__gte=today)
        )
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        return queryset.annotate(
            official_priority=Case(
                When(
                    Q(is_official=True) | Q(user__role__name__in=['special', 'Administrador']),
                    then=Value(0)
                ),
                default=Value(1),
                output_field=IntegerField(),
            )
        ).order_by('official_priority', '-like_count', '-created_at')

    def find_by_id(self, notice_id: int):
        return Notice.objects.filter(id=notice_id).first()

    def create(self, data: dict, user_id: int):
        return Notice.objects.create(**data, user_id=user_id)

    def like_exists(self, notice_id: int, user_id: int) -> bool:
        return NoticeLike.objects.filter(
            notice_id=notice_id, user_id=user_id
        ).exists()

    def create_like(self, notice_id: int, user_id: int):
        return NoticeLike.objects.create(notice_id=notice_id, user_id=user_id)

    def delete_like(self, notice_id: int, user_id: int):
        NoticeLike.objects.filter(notice_id=notice_id, user_id=user_id).delete()

    def delete(self, notice_id: int):
        Notice.objects.filter(id=notice_id).delete()

    def create_report(self, data: dict):
        return Report.objects.create(**data)
