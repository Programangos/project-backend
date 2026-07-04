import copy

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.services.procedures_service import ProceduresService
from core.serializers.procedure_serializer import (
    ProcedureSerializer,
    ProcedureExperienceSerializer,
    ProcedureExperienceVoteSerializer,
)
from core.domain.procedure import Procedure


class ProcedureListController(APIView):
    def get(self, request):
        search = request.query_params.get('search', '')
        type_filter = request.query_params.get('type', '')
        procedures = Procedure.objects.all()
        if search:
            procedures = procedures.filter(name__icontains=search)
        if type_filter:
            procedures = procedures.filter(type=type_filter)
        serializer = ProcedureSerializer(procedures, many=True)
        return Response(serializer.data)


class ProcedureCreateController(APIView):
    def post(self, request):
        user_id = getattr(request.user, 'id', None)
        if not user_id:
            return Response({'error': 'Debes iniciar sesión.'}, status=status.HTTP_401_UNAUTHORIZED)
        from core.domain.user import User
        requester = User.objects.filter(id=user_id).first()
        if not requester or not (requester.role and requester.role.name == 'Administrador'):
            return Response({'error': 'Solo los administradores pueden crear trámites.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = ProcedureSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        procedure = serializer.save()
        return Response(ProcedureSerializer(procedure).data, status=status.HTTP_201_CREATED)


class ProcedureExperienceController(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ProceduresService()

    def get(self, request, procedure_id):
        user_id = request.query_params.get('user_id')
        experiences = self.service.get_experiences_with_likes(procedure_id, user_id)
        return Response(experiences)

    def post(self, request, procedure_id):
        user_id = getattr(request.user, 'id', None)
        if not user_id:
            return Response({'error': 'Debes iniciar sesión para publicar una experiencia.'}, status=status.HTTP_401_UNAUTHORIZED)

        data = copy.deepcopy(request.data)
        if isinstance(data, dict):
            data['procedure_id'] = procedure_id
        serializer = ProcedureExperienceSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        result = self.service.create_experience(
            serializer.validated_data,
            user_id=user_id,
            procedure_id=procedure_id,
        )
        return Response(ProcedureExperienceSerializer(result).data, status=status.HTTP_201_CREATED)


class ProcedureAvgTimeController(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ProceduresService()

    def get(self, request, procedure_id):
        avg = self.service.get_avg_time(procedure_id)
        return Response(
            {'procedure_id': procedure_id, 'avg_time_days': avg},
            status=status.HTTP_200_OK,
        )


class ProcedureDeleteController(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ProceduresService()

    def delete(self, request, procedure_id):
        try:
            self.service.delete_procedure(procedure_id, request.user.id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PermissionError:
            return Response({'error': 'No tienes permiso para eliminar este trámite.'}, status=status.HTTP_403_FORBIDDEN)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)


class ProcedureExperienceDeleteController(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ProceduresService()

    def delete(self, request, experience_id):
        try:
            self.service.delete_experience(experience_id, request.user.id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PermissionError:
            return Response({'error': 'No tienes permiso para eliminar esta experiencia.'}, status=status.HTTP_403_FORBIDDEN)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)


class ProcedureExperienceVoteController(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ProceduresService()

    def post(self, request, experience_id):
        user_id = getattr(request.user, 'id', None)
        if not user_id:
            return Response({'error': 'Debes iniciar sesión para votar.'}, status=status.HTTP_401_UNAUTHORIZED)

        result = self.service.like_experience(
            experience_id=experience_id,
            user_id=user_id
        )
        serializer = ProcedureExperienceVoteSerializer(result) if result else None
        return Response(
            serializer.data if serializer else {'liked': False},
            status=status.HTTP_200_OK,
        )
