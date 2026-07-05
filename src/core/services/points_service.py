from django.db.models import F
from core.domain.user import User


class PointsService:
    ACTION_POINTS = {
        'publish_advice': 5,
        'publish_experience': 5,
        'publish_notice': 3,
        'receive_like': 2,
        'comment_building': 1,
    }

    TITLE_THRESHOLDS = [
        (0, 'Cachorro'),
        (21, 'Sobreviviente'),
        (51, 'Veterano'),
        (101, 'Leyenda UNAL'),
        (201, 'Inmortal Académico'),
    ]

    def award_points(self, user_id: int, action_type: str):
        points = self.ACTION_POINTS.get(action_type)
        if not points:
            return

        User.objects.filter(id=user_id).update(
            reputation_points=F('reputation_points') + points
        )

        user = User.objects.get(id=user_id)
        new_title = self.calculate_title(user.reputation_points)
        if new_title != user.title:
            user.title = new_title
            user.save(update_fields=['title'])

    def calculate_title(self, points: int) -> str:
        if points >= 201:
            return 'Inmortal Académico'
        elif points >= 101:
            return 'Leyenda UNAL'
        elif points >= 51:
            return 'Veterano'
        elif points >= 21:
            return 'Sobreviviente'
        return 'Cachorro'

    def update_title(self, user_id: int):
        user = User.objects.get(id=user_id)
        new_title = self.calculate_title(user.reputation_points)
        if new_title != user.title:
            user.title = new_title
            user.save(update_fields=['title'])
