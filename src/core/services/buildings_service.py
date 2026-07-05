from core.domain.building import BuildingComment
from core.services.base_service import BaseService


class BuildingsService(BaseService):
    def get_comments(self, building_id: int):
        return BuildingComment.objects.filter(building_id=building_id).select_related('user').order_by('-created_at')

    def create_comment(self, building_id: int, user_id: int, content: str):
        return BuildingComment.objects.create(
            building_id=building_id,
            user_id=user_id,
            content=content
        )

    def delete_comment(self, comment_id: int, requester_id: int):
        from core.domain.user import User

        comment = BuildingComment.objects.filter(id=comment_id).first()
        if not comment:
            raise ValueError('Comentario no encontrado.')
        requester = User.objects.filter(id=requester_id).first()
        if not requester:
            raise ValueError('Usuario no encontrado.')
        is_admin = requester.role and requester.role.name == 'Administrador'
        is_author = comment.user_id == requester_id
        if not (is_admin or is_author):
            raise PermissionError('No tienes permiso para eliminar este comentario.')
        comment.delete()
