from unittest.mock import MagicMock
import pytest
from rest_framework.exceptions import ValidationError
from core.services.advices_service import AdvicesService


class TestAdvicesService:

    def setup_method(self):
        self.mock_repo = MagicMock()
        self.service = AdvicesService(repository=self.mock_repo)

    def test_crear_consejo_valido(self):
        data = {"title": "Tip útil", "content": "Contenido válido", "category": "académico"}
        self.mock_repo.create.return_value = {"id": 1, **data}
        resultado = self.service.create_advice(data, user_id=1)
        assert resultado["id"] == 1
        self.mock_repo.create.assert_called_once_with(data, 1)

    def test_rechazar_consejo_sin_titulo(self):
        data = {"title": "", "content": "Contenido", "category": "académico"}
        with pytest.raises(ValidationError, match="título"):
            self.service.create_advice(data, user_id=1)

    def test_rechazar_consejo_sin_contenido(self):
        data = {"title": "Tip útil", "content": "", "category": "académico"}
        with pytest.raises(ValidationError, match="contenido"):
            self.service.create_advice(data, user_id=1)

    def test_rechazar_consejo_sin_categoria(self):
        data = {"title": "Tip útil", "content": "Contenido válido", "category": ""}
        with pytest.raises(ValidationError, match="categoría"):
            self.service.create_advice(data, user_id=1)

    def test_rechazar_like_duplicado(self):
        self.mock_repo.like_exists.return_value = True
        with pytest.raises(ValidationError, match="ya votó"):
            self.service.like_advice(advice_id=1, user_id=1)

    def test_crear_like_valido(self):
        self.mock_repo.like_exists.return_value = False
        self.mock_repo.create_like.return_value = {"id": 1, "advice_id": 1, "user_id": 1}
        resultado = self.service.like_advice(advice_id=1, user_id=1)
        assert resultado["id"] == 1
        self.mock_repo.create_like.assert_called_once_with(1, 1)
