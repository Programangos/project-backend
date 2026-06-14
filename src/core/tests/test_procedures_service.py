from unittest.mock import MagicMock
import pytest
from rest_framework.exceptions import ValidationError
from core.services.procedures_service import ProceduresService


class TestProceduresService:

    def setup_method(self):
        self.mock_repo = MagicMock()
        self.service = ProceduresService(repository=self.mock_repo)

    def test_crear_experiencia_valida(self):
        data = {"comment": "Tardó poco", "actual_time_days": 3, "procedure_id": 1}
        self.mock_repo.create_experience.return_value = {"id": 1, **data}
        resultado = self.service.create_experience(data, user_id=1)
        assert resultado["id"] == 1

    def test_rechazar_tiempo_negativo(self):
        data = {"comment": "Tardó poco", "actual_time_days": -1, "procedure_id": 1}
        with pytest.raises(ValidationError, match="mayor a cero"):
            self.service.create_experience(data, user_id=1)

    def test_rechazar_tiempo_cero(self):
        data = {"comment": "Tardó poco", "actual_time_days": 0, "procedure_id": 1}
        with pytest.raises(ValidationError, match="mayor a cero"):
            self.service.create_experience(data, user_id=1)

    def test_rechazar_comentario_vacio(self):
        data = {"comment": "", "actual_time_days": 3, "procedure_id": 1}
        with pytest.raises(ValidationError, match="comentario"):
            self.service.create_experience(data, user_id=1)

    def test_rechazar_voto_duplicado(self):
        self.mock_repo.vote_exists.return_value = True
        with pytest.raises(ValidationError, match="ya votó"):
            self.service.like_experience(experience_id=1, user_id=1)

    def test_crear_voto_valido(self):
        self.mock_repo.vote_exists.return_value = False
        self.mock_repo.create_vote.return_value = {"experience_id": 1, "user_id": 1}
        resultado = self.service.like_experience(experience_id=1, user_id=1)
        assert resultado["experience_id"] == 1
