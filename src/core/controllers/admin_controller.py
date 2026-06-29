from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.services.auth_service import AuthService
from core.serializers.user_serializer import UserSerializer


class AdminListUsersController(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = AuthService()

    def get(self, request):
        users = self.service.get_all_users()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class AdminDeleteUserController(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = AuthService()

    def delete(self, request, user_id):
        self.service.delete_user(user_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminUpdateRoleController(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = AuthService()

    def patch(self, request, user_id):
        role_id = request.data.get('role_id')
        if not role_id:
            return Response({'error': 'role_id es obligatorio.'}, status=status.HTTP_400_BAD_REQUEST)
        user = self.service.update_user_role(user_id, role_id)
        return Response(UserSerializer(user).data)
