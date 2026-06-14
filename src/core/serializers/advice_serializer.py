from rest_framework import serializers
from core.domain.advice import Advice, AdviceLike


class AdviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advice
        fields = ['id', 'title', 'content', 'category', 'status', 'user_id', 'created_at']
        read_only_fields = ['id', 'status', 'user_id', 'created_at']


class AdviceLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdviceLike
        fields = ['id', 'user_id', 'advice_id', 'created_at']
        read_only_fields = ['id', 'user_id', 'created_at']
