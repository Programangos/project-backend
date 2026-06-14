from rest_framework.exceptions import ValidationError


class AdvicesService:
    def __init__(self, repository=None):
        if repository is None:
            from core.infra.advices_repository import AdvicesRepository
            repository = AdvicesRepository()
        self.repository = repository

    def create_advice(self, data: dict, user_id: int):
        if not data.get('title', '').strip():
            raise ValidationError("El título es obligatorio.")

        if not data.get('content', '').strip():
            raise ValidationError("El contenido es obligatorio.")

        if not data.get('category', '').strip():
            raise ValidationError("La categoría es obligatoria.")

        return self.repository.create(data, user_id)

    def like_advice(self, advice_id: int, user_id: int):
        if self.repository.like_exists(advice_id, user_id):
            raise ValidationError("El usuario ya votó este consejo.")

        return self.repository.create_like(advice_id, user_id)
