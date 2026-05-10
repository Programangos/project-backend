from rest_framework.views import APIView
from rest_framework.response import Response
from core.services.role_service import RoleService
from core.serializers.role_serializer import RoleSerializer

class RoleController(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = RoleService()

    def get(self, request):
        roles = self.service.get_all_roles()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)
