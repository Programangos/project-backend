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
