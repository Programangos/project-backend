from datetime import date
from rest_framework.exceptions import ValidationError


class NoticesService:
    def __init__(self, repository=None):
        if repository is None:
            from core.infra.notices_repository import NoticesRepository
            repository = NoticesRepository()
        self.repository = repository

    def create_notice(self, data: dict, user_id: int):
        if not data.get('title', '').strip():
            raise ValidationError('El titulo es obligatorio.')
        expiration = data.get('expiration_date')
        if expiration and expiration < date.today():
            raise ValidationError('La fecha de vigencia no puede ser en el pasado.')
        return self.repository.create(data, user_id)

    def like_notice(self, notice_id: int, user_id: int):
        if self.repository.like_exists(notice_id, user_id):
            raise ValidationError('El usuario ya voto este aviso.')
        return self.repository.create_like(notice_id, user_id)

    def report_notice(self, notice_id: int, reporter_id: int, reason: str):
        if not reason.strip():
            raise ValidationError('La razon del reporte es obligatoria.')
        data = {
            'content_type': 'notice',
            'reference_id': notice_id,
            'reporter_id': reporter_id,
            'reason': reason,
            'status': 'pending'
        }
        return self.repository.create_report(data)
