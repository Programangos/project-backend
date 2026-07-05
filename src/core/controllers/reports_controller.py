from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.services.reports_service import ReportsService
from core.serializers.notice_serializer import ReportSerializer


class CreateReportController(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ReportsService()

    def post(self, request):
        user_id = getattr(request.user, 'id', None)
        if not user_id:
            return Response({'error': 'Debes iniciar sesión para reportar.'}, status=status.HTTP_401_UNAUTHORIZED)

        content_type = request.data.get('content_type', '')
        reference_id = request.data.get('reference_id')
        reason = request.data.get('reason', '')

        if not content_type:
            return Response({'error': 'El tipo de contenido es obligatorio.'}, status=status.HTTP_400_BAD_REQUEST)
        if not reference_id:
            return Response({'error': 'La referencia del contenido es obligatoria.'}, status=status.HTTP_400_BAD_REQUEST)
        if not reason.strip():
            return Response({'error': 'La razón del reporte es obligatoria.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = self.service.create_report(
                content_type=content_type,
                reference_id=reference_id,
                reporter_id=user_id,
                reason=reason,
            )
            return Response(ReportSerializer(result).data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AdminReportListController(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ReportsService()

    def get(self, request):
        user_id = getattr(request.user, 'id', None)
        if not user_id:
            return Response({'error': 'Debes iniciar sesión.'}, status=status.HTTP_401_UNAUTHORIZED)
        from core.domain.user import User
        requester = User.objects.filter(id=user_id).first()
        if not requester or not (requester.role and requester.role.name == 'Administrador'):
            return Response({'error': 'Solo administradores.'}, status=status.HTTP_403_FORBIDDEN)

        status_filter = request.query_params.get('status')
        grouped = self.service.get_grouped_reports(status=status_filter)
        # Enrich with content preview
        for g in grouped:
            g['content_preview'] = self.service.get_reported_content_preview(
                g['content_type'], g['reference_id']
            )
        return Response(grouped)


class AdminReportDismissController(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ReportsService()

    def post(self, request, report_id):
        user_id = getattr(request.user, 'id', None)
        if not user_id:
            return Response({'error': 'Debes iniciar sesión.'}, status=status.HTTP_401_UNAUTHORIZED)
        from core.domain.user import User
        requester = User.objects.filter(id=user_id).first()
        if not requester or not (requester.role and requester.role.name == 'Administrador'):
            return Response({'error': 'Solo administradores.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            self.service.dismiss_report(report_id)
            return Response({'status': 'resolved'})
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)


class AdminReportDeleteContentController(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ReportsService()

    def delete(self, request, report_id):
        user_id = getattr(request.user, 'id', None)
        if not user_id:
            return Response({'error': 'Debes iniciar sesión.'}, status=status.HTTP_401_UNAUTHORIZED)
        from core.domain.user import User
        requester = User.objects.filter(id=user_id).first()
        if not requester or not (requester.role and requester.role.name == 'Administrador'):
            return Response({'error': 'Solo administradores.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            self.service.delete_reported_content(report_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
