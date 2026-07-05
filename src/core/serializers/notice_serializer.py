from rest_framework import serializers
from core.domain.notice import Notice, NoticeLike
from core.domain.report import Report


class NoticeSerializer(serializers.ModelSerializer):
    user_full_name = serializers.SerializerMethodField()
    user_role_name = serializers.SerializerMethodField()
    user_title = serializers.SerializerMethodField()
    like_count = serializers.IntegerField(read_only=True, default=0)
    user_has_liked = serializers.SerializerMethodField()

    class Meta:
        model = Notice
        fields = ['id', 'title', 'description', 'category',
                  'is_official', 'expiration_date', 'user_id',
                  'created_at', 'user_full_name', 'user_role_name', 'user_title',
                  'like_count', 'user_has_liked']
        read_only_fields = ['id', 'is_official', 'user_id',
                            'created_at', 'user_full_name', 'user_role_name', 'user_title',
                            'like_count', 'user_has_liked']

    def get_user_full_name(self, obj):
        return obj.user.full_name if obj.user else None

    def get_user_role_name(self, obj):
        if obj.user and obj.user.role:
            return obj.user.role.name
        return None

    def get_user_title(self, obj):
        return obj.user.title if obj.user else None

    def get_user_has_liked(self, obj):
        user_id = self.context.get('user_id')
        if not user_id:
            return False
        from core.domain.notice import NoticeLike
        return NoticeLike.objects.filter(user_id=user_id, notice_id=obj.id).exists()


class CreateNoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['title', 'description', 'category', 'expiration_date']

    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('El título es obligatorio.')
        if len(value) > 255:
            raise serializers.ValidationError('El título no puede exceder 255 caracteres.')
        return value.strip()

    def validate_description(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('La descripción es obligatoria.')
        return value.strip()


class NoticeLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeLike
        fields = ['user_id', 'notice_id', 'created_at']
        read_only_fields = ['user_id', 'created_at']


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'content_type', 'reference_id',
                  'reporter_id', 'reason', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']
