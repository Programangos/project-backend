from datetime import date
from rest_framework.exceptions import ValidationError
from core.services.base_service import BaseService
from core.services.points_service import PointsService


class NoticesService(BaseService):
    def __init__(self, repository=None):
        if repository is None:
            from core.infra.notices_repository import NoticesRepository
            repository = NoticesRepository()
        self.repository = repository
        self.points_service = PointsService()

    def get_all_notices(self, search=None):
        return self.repository.get_all(search=search)

    def create_notice(self, data: dict, user_id: int):
        title = data.get('title', '').strip()
        if not title:
            raise ValidationError('El titulo es obligatorio.')
        expiration = data.get('expiration_date')
        if expiration and expiration < date.today():
            raise ValidationError('La fecha de vigencia no puede ser en el pasado.')
        notice = self.repository.create(data, user_id)
        self.points_service.award_points(user_id, 'publish_notice')
        return notice

    def like_notice(self, notice_id: int, user_id: int):
        if self.repository.like_exists(notice_id, user_id):
            self.repository.delete_like(notice_id, user_id)
            return None
        like = self.repository.create_like(notice_id, user_id)
        notice = self.repository.find_by_id(notice_id)
        if notice and notice.user_id != user_id:
            self.points_service.award_points(notice.user_id, 'receive_like')
        return like

    def unlike_notice(self, notice_id: int, user_id: int):
        self.repository.delete_like(notice_id, user_id)

    def delete_notice(self, notice_id: int, requester_id: int):
        from core.domain.user import User
        notice = self.repository.find_by_id(notice_id)
        if not notice:
            raise ValueError('Aviso no encontrado.')
        requester = User.objects.filter(id=requester_id).first()
        if not requester:
            raise ValueError('Usuario no encontrado.')
        is_admin = requester.role and requester.role.name == 'Administrador'
        is_author = notice.user_id == requester_id
        if not (is_admin or is_author):
            raise PermissionError('No tienes permiso para eliminar este aviso.')
        self.repository.delete(notice_id)

    def report_notice(self, notice_id: int, reporter_id: int, reason: str):
        reason_stripped = reason.strip()
        if not reason_stripped:
            raise ValidationError('La razon del reporte es obligatoria.')
        data = {
            'content_type': 'notice',
            'reference_id': notice_id,
            'reporter_id': reporter_id,
            'reason': reason,
            'status': 'pending'
        }
        return self.repository.create_report(data)
