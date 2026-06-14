from core.domain.user import User


class UserRepository:
    def find_by_email(self, email: str):
        return User.objects.filter(email=email).first()

    def create(self, data: dict):
        return User.objects.create(**data)

    def update(self, user_id: int, data: dict):
        User.objects.filter(id=user_id).update(**data)
        return User.objects.get(id=user_id)
