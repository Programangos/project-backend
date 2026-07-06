from core.domain.zone import Zone


class ZoneRepository:
    def get_all(self):
        return Zone.objects.all().order_by('zone_id')

    def find_by_id(self, zone_id: str):
        return Zone.objects.filter(zone_id=zone_id).first()

    def find_by_pk(self, pk: int):
        return Zone.objects.filter(id=pk).first()

    def create(self, data: dict):
        return Zone.objects.create(**data)

    def update(self, pk: int, data: dict):
        Zone.objects.filter(id=pk).update(**data)
        return Zone.objects.get(id=pk)

    def delete(self, pk: int):
        Zone.objects.filter(id=pk).delete()
