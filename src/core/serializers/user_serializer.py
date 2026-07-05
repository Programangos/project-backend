from rest_framework import serializers
from core.domain.user import User


class UserSerializer(serializers.ModelSerializer):
    is_characterized = serializers.SerializerMethodField()
    role_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'full_name', 'email', 'major', 'avatar_url',
            'current_semester', 'reputation_points', 'title', 'created_at',
            'is_characterized', 'role', 'role_name',
        ]
        read_only_fields = ['id', 'reputation_points', 'title', 'created_at', 'is_characterized', 'role_name']

    def get_is_characterized(self, obj):
        return bool(obj.major and obj.current_semester)

    def get_role_name(self, obj):
        return obj.role.name if obj.role else None


class RegisterSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    major = serializers.CharField(max_length=255)
    current_semester = serializers.IntegerField()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
