from rest_framework import serializers
from core.domain.procedure import Procedure, ProcedureExperience, ProcedureExperienceVote


class ProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = ['id', 'name', 'official_description', 'type', 'department', 'avg_time_days']


class ProcedureExperienceSerializer(serializers.ModelSerializer):
    user_full_name = serializers.SerializerMethodField()
    user_role_name = serializers.SerializerMethodField()
    user_title = serializers.SerializerMethodField()

    class Meta:
        model = ProcedureExperience
        fields = ['id', 'comment', 'actual_time_days', 'user_id', 'procedure_id',
                  'created_at', 'user_full_name', 'user_role_name', 'user_title']
        read_only_fields = ['id', 'user_id', 'created_at',
                            'user_full_name', 'user_role_name', 'user_title']

    def get_user_full_name(self, obj):
        return obj.user.full_name if obj.user else None

    def get_user_role_name(self, obj):
        if obj.user and obj.user.role:
            return obj.user.role.name
        return None

    def get_user_title(self, obj):
        return obj.user.title if obj.user else None


class ProcedureExperienceVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcedureExperienceVote
        fields = ['user_id', 'experience_id', 'created_at']
        read_only_fields = ['user_id', 'created_at']
