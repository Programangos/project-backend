from core.domain.user import User


class UserRepository:
    def find_by_email(self, email: str):
        return User.objects.filter(email=email).first()

    def find_by_id(self, user_id: int):
        return User.objects.filter(id=user_id).first()

    def create(self, data: dict):
        return User.objects.create(**data)

    def update(self, user_id: int, data: dict):
        User.objects.filter(id=user_id).update(**data)
        return User.objects.get(id=user_id)

    def get_all(self):
        return User.objects.all().order_by('-created_at')

    def delete(self, user_id: int):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM advice_like WHERE user_id = %s', [user_id])
            cursor.execute('DELETE FROM notice_like WHERE user_id = %s', [user_id])
            cursor.execute('DELETE FROM procedure_experience_vote WHERE user_id = %s', [user_id])
            cursor.execute('DELETE FROM building_comment WHERE user_id = %s', [user_id])
            cursor.execute('DELETE FROM report WHERE reporter_id = %s', [user_id])
            cursor.execute('DELETE FROM user_achievement WHERE user_id = %s', [user_id])
            cursor.execute('DELETE FROM password_reset_token WHERE user_id = %s', [user_id])
            cursor.execute('DELETE FROM advice WHERE user_id = %s', [user_id])
            cursor.execute('DELETE FROM notice WHERE user_id = %s', [user_id])
            cursor.execute('DELETE FROM procedure_experience WHERE user_id = %s', [user_id])
        User.objects.filter(id=user_id).delete()
