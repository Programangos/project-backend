from unittest.mock import MagicMock
import pytest
from rest_framework.exceptions import ValidationError
from core.services.auth_service import AuthService


class TestAuthService:

    def setup_method(self):
        self.mock_repo = MagicMock()
        self.service = AuthService(repository=self.mock_repo)

    def test_registro_email_valido(self):
        self.mock_repo.find_by_email.return_value = None
        self.mock_repo.create.return_value = {"id": 1, "email": "test@unal.edu.co"}
        data = {
            "full_name": "Juan",
            "email": "test@unal.edu.co",
            "password": "segura123",
            "major": "Sistemas",
            "current_semester": 4
        }
        resultado = self.service.register(data)
        assert resultado["email"] == "test@unal.edu.co"

    def test_registro_email_no_institucional(self):
        data = {
            "full_name": "Juan",
            "email": "test@gmail.com",
            "password": "segura123",
            "major": "Sistemas",
            "current_semester": 4
        }
        with pytest.raises(ValidationError, match="institucional"):
            self.service.register(data)

    def test_registro_email_duplicado(self):
        self.mock_repo.find_by_email.return_value = {"id": 1, "email": "test@unal.edu.co"}
        data = {
            "full_name": "Juan",
            "email": "test@unal.edu.co",
            "password": "segura123",
            "major": "Sistemas",
            "current_semester": 4
        }
        with pytest.raises(ValidationError, match="registrado"):
            self.service.register(data)

    def test_login_contrasena_incorrecta(self):
        mock_user = MagicMock()
        mock_user.password_hash = "hash_incorrecto"
        self.mock_repo.find_by_email.return_value = mock_user
        with pytest.raises(ValidationError, match="Credenciales"):
            self.service.login("test@unal.edu.co", "wrongpassword")

    def test_login_usuario_no_existe(self):
        self.mock_repo.find_by_email.return_value = None
        with pytest.raises(ValidationError, match="Credenciales"):
            self.service.login("noexiste@unal.edu.co", "password123")

    def test_actualizar_perfil_campos_validos(self):
        self.mock_repo.update.return_value = {"id": 1, "major": "Sistemas", "current_semester": 5}
        resultado = self.service.update_profile(1, {"major": "Sistemas", "current_semester": 5})
        assert resultado["major"] == "Sistemas"
