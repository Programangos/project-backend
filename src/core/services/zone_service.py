from rest_framework.exceptions import ValidationError, PermissionDenied
from core.infra.zone_repository import ZoneRepository


class ZoneService:
    def __init__(self, repository=None):
        self.repository = repository or ZoneRepository()

    def _check_admin(self, user):
        if not user or not getattr(user, 'role', None) or user.role.name != 'Administrador':
            raise PermissionDenied('Solo el administrador puede realizar esta acción.')

    def list_zones(self):
        return self.repository.get_all()

    def get_zone(self, zone_id: str):
        zone = self.repository.find_by_id(zone_id)
        if not zone:
            raise ValidationError('Zona no encontrada.')
        return zone

    def create_zone(self, user, data: dict):
        self._check_admin(user)
        existing = self.repository.find_by_id(data.get('zone_id', ''))
        if existing:
            raise ValidationError('Ya existe una zona con ese ID.')
        required = ['zone_id', 'name', 'bounds_south', 'bounds_west', 'bounds_north', 'bounds_east']
        for field in required:
            if field not in data:
                raise ValidationError(f'El campo {field} es obligatorio.')
        return self.repository.create(data)

    def update_zone(self, user, pk: int, data: dict):
        self._check_admin(user)
        zone = self.repository.find_by_pk(pk)
        if not zone:
            raise ValidationError('Zona no encontrada.')
        allowed = {'name', 'description', 'route', 'bounds_south', 'bounds_west', 'bounds_north', 'bounds_east'}
        filtered = {k: v for k, v in data.items() if k in allowed}
        if not filtered:
            raise ValidationError('No hay campos válidos para actualizar.')
        return self.repository.update(pk, filtered)

    def delete_zone(self, user, pk: int):
        self._check_admin(user)
        zone = self.repository.find_by_pk(pk)
        if not zone:
            raise ValidationError('Zona no encontrada.')
        self.repository.delete(pk)
