from core.domain.procedure import ProcedureExperience, ProcedureExperienceVote


class ProceduresRepository:
    def create_experience(self, data: dict, user_id: int):
        return ProcedureExperience.objects.create(**data, user_id=user_id)

    def get_avg_time(self, procedure_id: int):
        experiences = ProcedureExperience.objects.filter(procedure_id=procedure_id)
        if not experiences.exists():
            return 0
        total = sum(e.actual_time_days for e in experiences)
        return total / experiences.count()

    def vote_exists(self, experience_id: int, user_id: int) -> bool:
        return ProcedureExperienceVote.objects.filter(
            experience_id=experience_id, user_id=user_id
        ).exists()

    def create_vote(self, experience_id: int, user_id: int):
        return ProcedureExperienceVote.objects.create(
            experience_id=experience_id, user_id=user_id
        )
