from rest_framework.exceptions import ValidationError
from core.services.base_service import BaseService
from core.services.points_service import PointsService


class AdvicesService(BaseService):
    def __init__(self, repository=None):
        if repository is None:
            from core.infra.advices_repository import AdvicesRepository
            repository = AdvicesRepository()
        self.repository = repository
        self.points_service = PointsService()

    def get_all_advices(self, search=None):
        return self.repository.get_all(search=search)

    def create_advice(self, data: dict, user_id: int):
        title = data.get('title', '').strip()
        if not title:
            raise ValidationError("El título es obligatorio.")

        content = data.get('content', '').strip()
        if not content:
            raise ValidationError("El contenido es obligatorio.")

        category = data.get('category', '').strip()
        if not category:
            raise ValidationError("La categoría es obligatoria.")

        advice = self.repository.create(data, user_id)
        self.points_service.award_points(user_id, 'publish_advice')
        return advice

    def like_advice(self, advice_id: int, user_id: int):
        if self.repository.like_exists(advice_id, user_id):
            self.repository.delete_like(advice_id, user_id)
            return None
        like = self.repository.create_like(advice_id, user_id)
        advice = self.repository.find_by_id(advice_id)
        if advice and advice.user_id != user_id:
            self.points_service.award_points(advice.user_id, 'receive_like')
        return like

    def delete_advice(self, advice_id: int, requester_id: int):
        from core.domain.user import User
        advice = self.repository.find_by_id(advice_id)
        if not advice:
            raise ValueError('Consejo no encontrado.')
        requester = User.objects.filter(id=requester_id).first()
        if not requester:
            raise ValueError('Usuario no encontrado.')
        is_admin = requester.role and requester.role.name == 'Administrador'
        is_author = advice.user_id == requester_id
        if not (is_admin or is_author):
            raise PermissionError('No tienes permiso para eliminar este consejo.')
        self.repository.delete(advice_id)
