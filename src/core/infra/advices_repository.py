from core.domain.advice import Advice, AdviceLike


class AdvicesRepository:
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
