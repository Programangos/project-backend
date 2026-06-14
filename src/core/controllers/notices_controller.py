from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.services.notices_service import NoticesService
from core.serializers.notice_serializer import (
    NoticeSerializer, NoticeLikeSerializer, ReportSerializer
)


class NoticesController(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = NoticesService()

    def post(self, request):
        serializer = NoticeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        result = self.service.create_notice(
            serializer.validated_data,
            user_id=request.data.get('user_id')
        )
        return Response(NoticeSerializer(result).data, status=status.HTTP_201_CREATED)


class NoticeLikeController(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = NoticesService()

    def post(self, request, notice_id):
        result = self.service.like_notice(
            notice_id=notice_id,
            user_id=request.data.get('user_id')
        )
        return Response(NoticeLikeSerializer(result).data, status=status.HTTP_201_CREATED)


class NoticeReportController(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = NoticesService()

    def post(self, request, notice_id):
        serializer = ReportSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        result = self.service.report_notice(
            notice_id=notice_id,
            reporter_id=request.data.get('user_id'),
            reason=request.data.get('reason', '')
        )
        return Response(ReportSerializer(result).data, status=status.HTTP_201_CREATED)
