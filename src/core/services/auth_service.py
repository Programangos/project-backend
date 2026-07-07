import hashlib
import secrets
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
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
        if 'role_id' not in data:
            try:
                from core.domain.role import Role
                regular = Role.objects.filter(name='regular').first()
                if regular:
                    data['role_id'] = regular.id
            except RuntimeError:
                pass
        return self.repository.create(data)

    def login(self, email: str, password: str):
        user = self.repository.find_by_email(email)
        if not user:
            raise ValidationError("Credenciales inválidas.")
        if user.password_hash != self._hash_password(password):
            raise ValidationError("Credenciales inválidas.")
        return user

    def update_profile(self, user_id: int, data: dict):
        allowed = {'full_name', 'major', 'current_semester', 'avatar_url', 'reputation_points'}
        filtered = {k: v for k, v in data.items() if k in allowed}
        if not filtered:
            raise ValidationError("No hay campos válidos para actualizar.")
        user = self.repository.update(user_id, filtered)
        from core.services.points_service import PointsService
        PointsService().update_title(user_id)
        return user

    def forgot_password(self, email: str):
        from core.infra.user_repository import UserRepository
        from core.infra.email_service import EmailService

        repo = UserRepository()
        user = repo.find_by_email(email)
        if not user:
            return

        token = secrets.token_urlsafe(32)
        expires_at = timezone.now() + timedelta(hours=1)

        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute(
                'DELETE FROM password_reset_token WHERE user_id = %s',
                [user.id]
            )
            cursor.execute(
                'INSERT INTO password_reset_token (user_id, token, expires_at) VALUES (%s, %s, %s)',
                [user.id, token, expires_at]
            )

        service = EmailService()
        service.send_password_reset(email, token)

    def get_user(self, user_id: int):
        return self.repository.find_by_id(user_id)

    def get_all_users(self):
        return self.repository.get_all()

    def delete_user(self, user_id: int):
        self.repository.delete(user_id)

    def update_user_role(self, user_id: int, role_id: int):
        return self.repository.update(user_id, {'role_id': role_id})

    def reset_password(self, token: str, new_password: str):
        from django.db import connection

        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT user_id, expires_at FROM password_reset_token WHERE token = %s',
                [token]
            )
            row = cursor.fetchone()

        if not row:
            raise ValidationError("El enlace de recuperación es inválido.")

        user_id, expires_at = row
        if timezone.now() > expires_at:
            with connection.cursor() as c:
                c.execute('DELETE FROM password_reset_token WHERE token = %s', [token])
            raise ValidationError("El enlace de recuperación ha expirado.")

        password_hash = self._hash_password(new_password)
        self.repository.update(user_id, {'password_hash': password_hash})

        with connection.cursor() as c:
            c.execute('DELETE FROM password_reset_token WHERE token = %s', [token])
