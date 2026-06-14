from core.domain.role import Role


class RoleRepository:
    def get_all(self):
        return Role.objects.all()
