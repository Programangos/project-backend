from core.infra.role_repository import RoleRepository

class RoleService:
    def __init__(self):
        self.repository = RoleRepository()

    def get_all_roles(self):
        return self.repository.get_all()
