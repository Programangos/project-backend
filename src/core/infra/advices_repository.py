from django.db.models import Count, Q 
from core.domain.advice import Advice, AdviceLike

class AdvicesRepository:
    def get_all(self, search=None):
        queryset = Advice.objects.filter(status='active').annotate(
            like_count=Count('advicelike')
        )
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search) |
                Q(category__icontains=search)
            )
        return queryset.order_by('-like_count', '-created_at')

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
    