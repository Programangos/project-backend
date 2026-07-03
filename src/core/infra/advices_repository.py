from django.db.models import Count, Q
from core.domain.advice import Advice, AdviceLike


class AdvicesRepository:
    def get_all(self, search=None):
        queryset = Advice.objects.annotate(like_count=Count('advicelike'))
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )
        return queryset.order_by('-like_count', '-created_at')

    def find_by_id(self, advice_id: int):
        return Advice.objects.filter(id=advice_id).first()

    def create(self, data: dict, user_id: int):
        return Advice.objects.create(**data, user_id=user_id)

    def like_exists(self, advice_id: int, user_id: int) -> bool:
        return AdviceLike.objects.filter(
            advice_id=advice_id, user_id=user_id
        ).exists()

    def create_like(self, advice_id: int, user_id: int):
        return AdviceLike.objects.create(
            advice_id=advice_id, user_id=user_id
        )

    def delete_like(self, advice_id: int, user_id: int):
        AdviceLike.objects.filter(advice_id=advice_id, user_id=user_id).delete()

    def delete(self, advice_id: int):
        Advice.objects.filter(id=advice_id).delete()
