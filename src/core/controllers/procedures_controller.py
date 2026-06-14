from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.services.procedures_service import ProceduresService
from core.serializers.procedure_serializer import ProcedureExperienceSerializer, ProcedureExperienceVoteSerializer


class ProcedureExperienceController(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ProceduresService()

    def post(self, request, procedure_id):
        serializer = ProcedureExperienceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        result = self.service.create_experience(
            serializer.validated_data,
            user_id=request.data.get('user_id')
        )
        return Response(ProcedureExperienceSerializer(result).data, status=status.HTTP_201_CREATED)


class ProcedureAvgTimeController(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ProceduresService()

    def get(self, request, procedure_id):
        avg = self.service.get_avg_time(procedure_id)
        return Response({'procedure_id': procedure_id, 'avg_time_days': avg}, status=status.HTTP_200_OK)


class ProcedureExperienceVoteController(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ProceduresService()

    def post(self, request, experience_id):
        result = self.service.like_experience(
            experience_id=experience_id,
            user_id=request.data.get('user_id')
        )
        return Response(ProcedureExperienceVoteSerializer(result).data, status=status.HTTP_201_CREATED)
