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

    def post(self, request):
        serializer = AdviceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = self.service.create_advice(
            serializer.validated_data,
            user_id=request.data.get('user_id')
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
        result = self.service.like_advice(
            advice_id=advice_id,
            user_id=request.data.get('user_id')
        )

        return Response(
            AdviceLikeSerializer(result).data,
            status=status.HTTP_201_CREATED
        )
