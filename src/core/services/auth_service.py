import hashlib
from rest_framework.exceptions import ValidationError


class AuthService:
    def __init__(self, repository=None):
        if repository is None:
            from core.infra.user_repository import UserRepository
            repository = UserRepository()
        self.repository = repository

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, data: dict):
        email = data.get('email', '')
        if not email.endswith('@unal.edu.co'):
            raise ValidationError("El correo debe ser institucional (@unal.edu.co).")
        if self.repository.find_by_email(email):
            raise ValidationError("El correo ya está registrado.")
        data['password_hash'] = self._hash_password(data.pop('password'))
        return self.repository.create(data)

    def login(self, email: str, password: str):
        user = self.repository.find_by_email(email)
        if not user:
            raise ValidationError("Credenciales inválidas.")
        if user.password_hash != self._hash_password(password):
            raise ValidationError("Credenciales inválidas.")
        return user

    def update_profile(self, user_id: int, data: dict):
        allowed = {'major', 'current_semester'}
        filtered = {k: v for k, v in data.items() if k in allowed}
        if not filtered:
            raise ValidationError("No hay campos válidos para actualizar.")
        return self.repository.update(user_id, filtered)
