from unittest.mock import MagicMock
import pytest
from datetime import date, timedelta
from rest_framework.exceptions import ValidationError
from core.services.notices_service import NoticesService


class TestNoticesService:

    def setup_method(self):
        self.mock_repo = MagicMock()
        self.service = NoticesService(repository=self.mock_repo)

    def test_crear_aviso_valido(self):
        data = {
            'title': 'Paro estudiantil',
            'description': 'Manana no hay clases',
            'category': 'evento',
            'expiration_date': date.today() + timedelta(days=3)
        }
        self.mock_repo.create.return_value = {'id': 1, **data}
        resultado = self.service.create_notice(data, user_id=1)
        assert resultado['id'] == 1
        self.mock_repo.create.assert_called_once_with(data, 1)

    def test_rechazar_aviso_sin_titulo(self):
        data = {
            'title': '',
            'description': 'Descripcion',
            'category': 'evento',
            'expiration_date': date.today() + timedelta(days=3)
        }
        with pytest.raises(ValidationError, match='titulo'):
            self.service.create_notice(data, user_id=1)

    def test_rechazar_aviso_titulo_espacios(self):
        data = {
            'title': '   ',
            'description': 'Descripcion',
            'category': 'evento',
            'expiration_date': date.today() + timedelta(days=3)
        }
        with pytest.raises(ValidationError, match='titulo'):
            self.service.create_notice(data, user_id=1)

    def test_rechazar_fecha_pasada(self):
        data = {
            'title': 'Evento viejo',
            'description': 'Ya paso',
            'category': 'evento',
            'expiration_date': date.today() - timedelta(days=1)
        }
        with pytest.raises(ValidationError, match='pasado'):
            self.service.create_notice(data, user_id=1)

    def test_crear_aviso_sin_fecha_expiracion(self):
        data = {
            'title': 'Aviso sin fecha',
            'description': 'Sin vencimiento',
            'category': 'general',
            'expiration_date': None
        }
        self.mock_repo.create.return_value = {'id': 2, **data}
        resultado = self.service.create_notice(data, user_id=1)
        assert resultado['id'] == 2

    def test_like_duplicado_quita_like(self):
        self.mock_repo.like_exists.return_value = True
        resultado = self.service.like_notice(notice_id=1, user_id=1)
        assert resultado is None
        self.mock_repo.delete_like.assert_called_once_with(1, 1)

    def test_crear_like_valido(self):
        self.mock_repo.like_exists.return_value = False
        self.mock_repo.create_like.return_value = {'notice_id': 1, 'user_id': 1}
        resultado = self.service.like_notice(notice_id=1, user_id=1)
        assert resultado['notice_id'] == 1
        self.mock_repo.create_like.assert_called_once_with(1, 1)

    def test_reportar_aviso_valido(self):
        self.mock_repo.create_report.return_value = {'id': 1, 'status': 'pending'}
        resultado = self.service.report_notice(
            notice_id=1, reporter_id=2, reason='Contenido falso'
        )
        assert resultado['status'] == 'pending'

    def test_rechazar_reporte_sin_razon(self):
        with pytest.raises(ValidationError, match='razon'):
            self.service.report_notice(notice_id=1, reporter_id=2, reason='')

    def test_rechazar_reporte_razon_espacios(self):
        with pytest.raises(ValidationError, match='razon'):
            self.service.report_notice(notice_id=1, reporter_id=2, reason='   ')
