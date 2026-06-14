import hashlib
from rest_framework.exceptions import ValidationError


class AuthService:
    def __init__(self, repository=None):
        if repository is None:
            from core.infra.user_repository import UserRepository
            repository = UserRepository()
        self.repository = repository

    def register(self, data: dict):
        email = data.get('email', '')
        if not email.endswith('@unal.edu.co'):
            raise ValidationError("El correo debe ser institucional (@unal.edu.co).")
        if self.repository.find_by_email(email):
            raise ValidationError("El correo ya está registrado.")
        data['password_hash'] = hashlib.sha256(
            data.pop('password').encode()
        ).hexdigest()
        return self.repository.create(data)

    def login(self, email: str, password: str):
        user = self.repository.find_by_email(email)
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if not user or user.password_hash != password_hash:
            raise ValidationError("Credenciales inválidas.")
        return user

    def update_profile(self, user_id: int, data: dict):
        allowed = {'major', 'current_semester'}
        filtered = {k: v for k, v in data.items() if k in allowed}
        if not filtered:
            raise ValidationError("No hay campos válidos para actualizar.")
        return self.repository.update(user_id, filtered)
