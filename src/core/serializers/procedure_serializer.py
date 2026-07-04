from rest_framework import serializers
from core.domain.procedure import Procedure, ProcedureExperience, ProcedureExperienceVote


class ProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = ['id', 'name', 'official_description', 'type', 'department', 'avg_time_days']


class ProcedureExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcedureExperience
        fields = ['id', 'comment', 'actual_time_days', 'user_id', 'procedure_id', 'created_at']
        read_only_fields = ['id', 'user_id', 'created_at']


class ProcedureExperienceVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcedureExperienceVote
        fields = ['user_id', 'experience_id', 'created_at']
        read_only_fields = ['user_id', 'created_at']
