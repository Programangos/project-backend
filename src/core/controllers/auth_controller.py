from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from core.services.auth_service import AuthService
from core.serializers.user_serializer import UserSerializer, RegisterSerializer, LoginSerializer


class RegisterController(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = AuthService()

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = self.service.register(serializer.validated_data)
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data,
        }, status=status.HTTP_201_CREATED)


class LoginController(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = AuthService()

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = self.service.login(
            serializer.validated_data['email'],
            serializer.validated_data['password']
        )
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data,
        }, status=status.HTTP_200_OK)


class ProfileController(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = AuthService()

    def patch(self, request, user_id):
        result = self.service.update_profile(user_id, request.data)
        return Response(UserSerializer(result).data, status=status.HTTP_200_OK)
