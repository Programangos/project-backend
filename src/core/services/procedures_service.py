from rest_framework.exceptions import ValidationError
from core.services.base_service import BaseService


class ProceduresService(BaseService):
    def __init__(self, repository=None):
        if repository is None:
            from core.infra.procedures_repository import ProceduresRepository
            repository = ProceduresRepository()
        self.repository = repository

    def create_experience(self, data: dict, user_id: int, procedure_id: int = None):
        if data.get('actual_time_days', 0) <= 0:
            raise ValidationError("El tiempo debe ser mayor a cero.")
        comment = data.get('comment', '').strip()
        if not comment:
            raise ValidationError("El comentario es obligatorio.")
        cleaned = {**data, 'comment': comment}
        return self.repository.create_experience(cleaned, user_id, procedure_id)

    def get_avg_time(self, procedure_id: int):
        return self.repository.get_avg_time(procedure_id)

    def get_experiences_with_likes(self, procedure_id: int, user_id=None):
        return self.repository.get_experiences_with_likes(procedure_id, user_id)

    def delete_experience(self, experience_id: int, requester_id: int):
        from core.domain.user import User
        from core.domain.procedure import ProcedureExperience

        requester = User.objects.filter(id=requester_id).first()
        if not requester:
            raise ValueError('Usuario no encontrado.')
        experience = ProcedureExperience.objects.filter(id=experience_id).first()
        if not experience:
            raise ValueError('Experiencia no encontrada.')
        is_admin = requester.role and requester.role.name == 'Administrador'
        is_author = experience.user_id == requester_id
        if not (is_admin or is_author):
            raise PermissionError('No tienes permiso para eliminar esta experiencia.')
        experience.delete()

    def delete_procedure(self, procedure_id: int, requester_id: int):
        from core.domain.user import User
        from core.domain.procedure import Procedure, ProcedureExperience, ProcedureExperienceVote

        requester = User.objects.filter(id=requester_id).first()
        if not requester:
            raise ValueError('Usuario no encontrado.')
        is_admin = requester.role and requester.role.name == 'Administrador'
        if not is_admin:
            raise PermissionError('No tienes permiso para eliminar este trámite.')
        procedure = Procedure.objects.filter(id=procedure_id).first()
        if not procedure:
            raise ValueError('Trámite no encontrado.')
        experience_ids = ProcedureExperience.objects.filter(
            procedure_id=procedure_id
        ).values_list('id', flat=True)
        ProcedureExperienceVote.objects.filter(
            experience_id__in=list(experience_ids)
        ).delete()
        ProcedureExperience.objects.filter(procedure_id=procedure_id).delete()
        procedure.delete()

    def delete_experience(self, experience_id: int, requester_id: int):
        from core.domain.user import User
        from core.domain.procedure import ProcedureExperience, ProcedureExperienceVote

        experience = ProcedureExperience.objects.filter(id=experience_id).first()
        if not experience:
            raise ValueError('Experiencia no encontrada.')
        requester = User.objects.filter(id=requester_id).first()
        if not requester:
            raise ValueError('Usuario no encontrado.')
        is_admin = requester.role and requester.role.name == 'Administrador'
        is_author = experience.user_id == requester_id
        if not (is_admin or is_author):
            raise PermissionError('No tienes permiso para eliminar esta experiencia.')
        ProcedureExperienceVote.objects.filter(experience_id=experience_id).delete()
        experience.delete()

    def like_experience(self, experience_id: int, user_id: int):
        if self.repository.vote_exists(experience_id, user_id):
            self.repository.delete_vote(experience_id, user_id)
            return None
        return self.repository.create_vote(experience_id, user_id)
