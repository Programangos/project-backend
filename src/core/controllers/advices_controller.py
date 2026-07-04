from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.services.advices_service import AdvicesService
from core.serializers.advice_serializer import (
    AdviceSerializer,
    AdviceLikeSerializer
)


class AdvicesController(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = AdvicesService()

    def get(self, request):
        search = request.query_params.get('search')
        user_id = request.query_params.get('user_id')
        advices = self.service.get_all_advices(search=search)
        serializer = AdviceSerializer(advices, many=True, context={'user_id': user_id})
        return Response(serializer.data)

    def post(self, request):
        user_id = getattr(request.user, 'id', None)
        if not user_id:
            return Response({'error': 'Debes iniciar sesión para publicar un consejo.'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = AdviceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = self.service.create_advice(
            serializer.validated_data,
            user_id=user_id
        )

        return Response(
            AdviceSerializer(result).data,
            status=status.HTTP_201_CREATED
        )


class AdviceLikeController(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = AdvicesService()

    def post(self, request, advice_id):
        user_id = getattr(request.user, 'id', None)
        if not user_id:
            return Response({'error': 'Debes iniciar sesión para dar me gusta.'}, status=status.HTTP_401_UNAUTHORIZED)

        result = self.service.like_advice(
            advice_id=advice_id,
            user_id=user_id
        )

        serializer = AdviceLikeSerializer(result) if result else None
        return Response(
            serializer.data if serializer else {'liked': False},
            status=status.HTTP_200_OK
        )


class AdviceDeleteController(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = AdvicesService()

    def delete(self, request, advice_id):
        try:
            self.service.delete_advice(advice_id, request.user.id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PermissionError:
            return Response({'error': 'No tienes permiso para eliminar este consejo.'}, status=status.HTTP_403_FORBIDDEN)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
