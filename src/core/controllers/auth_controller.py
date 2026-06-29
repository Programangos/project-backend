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


class ForgotPasswordController(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = AuthService()

    def post(self, request):
        email = request.data.get('email', '')
        if not email:
            return Response({'email': 'El correo es obligatorio.'}, status=status.HTTP_400_BAD_REQUEST)
        self.service.forgot_password(email)
        return Response({'message': 'Si el correo está registrado, recibirás un enlace de recuperación.'}, status=status.HTTP_200_OK)


class ResetPasswordController(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = AuthService()

    def post(self, request):
        token = request.data.get('token', '')
        password = request.data.get('password', '')
        if not token or not password:
            return Response({'error': 'Token y contraseña son obligatorios.'}, status=status.HTTP_400_BAD_REQUEST)
        if len(password) < 6:
            return Response({'error': 'La contraseña debe tener al menos 6 caracteres.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            self.service.reset_password(token, password)
            return Response({'message': 'Contraseña actualizada correctamente.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
