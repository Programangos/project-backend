from rest_framework.exceptions import ValidationError


class ProceduresService:
    def __init__(self, repository=None):
        if repository is None:
            from core.infra.procedures_repository import ProceduresRepository
            repository = ProceduresRepository()
        self.repository = repository

    def create_experience(self, data: dict, user_id: int):
        if data.get('actual_time_days', 0) <= 0:
            raise ValidationError("El tiempo debe ser mayor a cero.")
        comment = data.get('comment', '').strip()
        if not comment:
            raise ValidationError("El comentario es obligatorio.")
        return self.repository.create_experience(data, user_id)

    def get_avg_time(self, procedure_id: int):
        if procedure_id <= 0:
            raise ValidationError("ID de trámite inválido.")
        return self.repository.get_avg_time(procedure_id)

    def like_experience(self, experience_id: int, user_id: int):
        if self.repository.vote_exists(experience_id, user_id):
            raise ValidationError("El usuario ya votó esta experiencia.")
        return self.repository.create_vote(experience_id, user_id)
