from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.services.zone_service import ZoneService
from core.serializers.zone_serializer import ZoneSerializer


class ZoneListController(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ZoneService()

    def get(self, request):
        zones = self.service.list_zones()
        serializer = ZoneSerializer(zones, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            zone = self.service.create_zone(request.user, request.data)
            serializer = ZoneSerializer(zone)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ZoneDetailController(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ZoneService()

    def put(self, request, pk):
        try:
            zone = self.service.update_zone(request.user, pk, request.data)
            serializer = ZoneSerializer(zone)
            return Response(serializer.data)
        except Exception as e:
            err = getattr(e, 'status_code', status.HTTP_400_BAD_REQUEST)
            return Response({'error': str(e)}, status=err)

    def delete(self, request, pk):
        try:
            self.service.delete_zone(request.user, pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            err = getattr(e, 'status_code', status.HTTP_400_BAD_REQUEST)
            return Response({'error': str(e)}, status=err)
