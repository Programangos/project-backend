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
        user_id = getattr(request.user, 'id', None)
        if not user_id:
            return Response({'error': 'Debes iniciar sesión para publicar un aviso.'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = CreateNoticeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
        user_id = getattr(request.user, 'id', None)
        if not user_id:
            return Response({'error': 'Debes iniciar sesión para dar me gusta.'}, status=status.HTTP_401_UNAUTHORIZED)

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
        user_id = getattr(request.user, 'id', None)
        if not user_id:
            return Response({'error': 'Debes iniciar sesión.'}, status=status.HTTP_401_UNAUTHORIZED)

        self.service.unlike_notice(notice_id, user_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class NoticeDeleteController(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = NoticesService()

    def delete(self, request, notice_id):
        user_id = getattr(request.user, 'id', None)
        if not user_id:
            return Response({'error': 'Debes iniciar sesión.'}, status=status.HTTP_401_UNAUTHORIZED)

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
        user_id = getattr(request.user, 'id', None)
        if not user_id:
            return Response({'error': 'Debes iniciar sesión para reportar.'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = ReportSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        result = self.service.report_notice(
            notice_id=notice_id,
            reporter_id=user_id,
            reason=request.data.get('reason', '')
        )
        return Response(ReportSerializer(result).data, status=status.HTTP_201_CREATED)
