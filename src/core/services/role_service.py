from core.infra.role_repository import RoleRepository


class RoleService:
    def __init__(self, repository=None):
        if repository is None:
            repository = RoleRepository()
        self.repository = repository

    def get_all_roles(self):
        return self.repository.get_all()
