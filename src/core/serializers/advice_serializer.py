from rest_framework import serializers
from core.domain.advice import Advice, AdviceLike


class AdviceSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(read_only=True, default=0)
    user_has_liked = serializers.SerializerMethodField()

    class Meta:
        model = Advice
        fields = ['id', 'title', 'content', 'category', 'status',
                  'user_id', 'created_at', 'like_count', 'user_has_liked']
        read_only_fields = ['id', 'status', 'user_id', 'created_at',
                             'like_count', 'user_has_liked']

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