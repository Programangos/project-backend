from rest_framework import serializers
from core.domain.advice import Advice, AdviceLike


class AdviceSerializer(serializers.ModelSerializer):
    user_full_name = serializers.SerializerMethodField()
    user_role_name = serializers.SerializerMethodField()
    user_title = serializers.SerializerMethodField()
    like_count = serializers.IntegerField(read_only=True, default=0)
    user_has_liked = serializers.SerializerMethodField()

    class Meta:
        model = Advice
        fields = ['id', 'title', 'content', 'category', 'status',
                  'user_id', 'created_at', 'user_full_name',
                  'user_role_name', 'user_title', 'like_count', 'user_has_liked']
        read_only_fields = ['id', 'status', 'user_id', 'created_at',
                            'user_full_name', 'user_role_name', 'user_title',
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
        return AdviceLike.objects.filter(user_id=user_id, advice_id=obj.id).exists()


class AdviceLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdviceLike
        fields = ['id', 'user_id', 'advice_id', 'created_at']
        read_only_fields = ['id', 'user_id', 'created_at']