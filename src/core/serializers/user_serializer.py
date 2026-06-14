from rest_framework import serializers
from core.domain.user import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'major', 'current_semester', 'reputation_points', 'created_at']
        read_only_fields = ['id', 'reputation_points', 'created_at']


class RegisterSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    major = serializers.CharField(max_length=255)
    current_semester = serializers.IntegerField()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
