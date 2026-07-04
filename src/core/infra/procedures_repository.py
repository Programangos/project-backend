from django.db.models import Avg
from core.domain.procedure import ProcedureExperience, ProcedureExperienceVote
from core.serializers.procedure_serializer import ProcedureExperienceSerializer


class ProceduresRepository:
    def create_experience(self, data: dict, user_id: int, procedure_id: int = None):
        return ProcedureExperience.objects.create(
            **data, user_id=user_id, procedure_id=procedure_id
        )

    def get_avg_time(self, procedure_id: int):
        result = ProcedureExperience.objects.filter(
            procedure_id=procedure_id
        ).aggregate(avg=Avg('actual_time_days'))
        return result['avg'] or 0

    def get_experiences_with_likes(self, procedure_id: int, user_id=None):
        experiences = ProcedureExperience.objects.filter(
            procedure_id=procedure_id
        ).order_by('-created_at')
        data = []
        for exp in experiences:
            entry = ProcedureExperienceSerializer(exp).data
            entry['like_count'] = ProcedureExperienceVote.objects.filter(
                experience_id=exp.id
            ).count()
            entry['user_has_liked'] = False
            if user_id:
                entry['user_has_liked'] = ProcedureExperienceVote.objects.filter(
                    experience_id=exp.id, user_id=user_id
                ).exists()
            data.append(entry)
        return data

    def vote_exists(self, experience_id: int, user_id: int) -> bool:
        return ProcedureExperienceVote.objects.filter(
            experience_id=experience_id, user_id=user_id
        ).exists()

    def create_vote(self, experience_id: int, user_id: int):
        return ProcedureExperienceVote.objects.create(
            experience_id=experience_id, user_id=user_id
        )

    def delete_vote(self, experience_id: int, user_id: int):
        ProcedureExperienceVote.objects.filter(
            experience_id=experience_id, user_id=user_id
        ).delete()
