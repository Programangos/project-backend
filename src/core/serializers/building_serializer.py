from rest_framework import serializers
from core.domain.building import BuildingComment


class BuildingCommentSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = BuildingComment
        fields = ['id', 'content', 'user_id', 'user_full_name', 'building_id', 'created_at']

    def create(self, validated_data):
        validated_data.pop('user', None)
        return super().create(validated_data)
