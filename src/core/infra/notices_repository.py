from core.domain.notice import Notice, NoticeLike
from core.domain.report import Report


class NoticesRepository:
    def create(self, data: dict, user_id: int):
        return Notice.objects.create(**data, user_id=user_id)

    def like_exists(self, notice_id: int, user_id: int) -> bool:
        return NoticeLike.objects.filter(
            notice_id=notice_id, user_id=user_id
        ).exists()

    def create_like(self, notice_id: int, user_id: int):
        return NoticeLike.objects.create(notice_id=notice_id, user_id=user_id)

    def create_report(self, data: dict):
        return Report.objects.create(**data)
