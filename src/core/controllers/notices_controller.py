from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.services.notices_service import NoticesService
from core.serializers.notice_serializer import (
    NoticeSerializer, CreateNoticeSerializer, NoticeLikeSerializer, ReportSerializer
)


class NoticesController(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = NoticesService()

    def get(self, request):
        search = request.query_params.get('search')
        user_id = request.query_params.get('user_id')
        notices = self.service.get_all_notices(search=search)
        serializer = NoticeSerializer(notices, many=True, context={'user_id': user_id})
        return Response(serializer.data)

    def post(self, request):
        serializer = CreateNoticeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id es obligatorio.'}, status=status.HTTP_400_BAD_REQUEST)
        result = self.service.create_notice(
            serializer.validated_data,
            user_id=user_id
        )
        return Response(NoticeSerializer(result).data, status=status.HTTP_201_CREATED)


class NoticeLikeController(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = NoticesService()

    def post(self, request, notice_id):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id es obligatorio.'}, status=status.HTTP_400_BAD_REQUEST)
        result = self.service.like_notice(
            notice_id=notice_id,
            user_id=user_id
        )
        serializer = NoticeLikeSerializer(result) if result else None
        return Response(
            serializer.data if serializer else {'liked': False},
            status=status.HTTP_200_OK
        )

    def delete(self, request, notice_id):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'error': 'user_id es obligatorio.'}, status=status.HTTP_400_BAD_REQUEST)
        self.service.unlike_notice(notice_id, user_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class NoticeDeleteController(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = NoticesService()

    def delete(self, request, notice_id):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id es obligatorio.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            self.service.delete_notice(notice_id, user_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PermissionError:
            return Response({'error': 'No tienes permiso para eliminar este aviso.'}, status=status.HTTP_403_FORBIDDEN)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)


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
