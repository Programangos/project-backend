from core.domain.report import Report
from core.services.base_service import BaseService


CONTENT_TYPE_MAP = {
    'advice': ('core.domain.advice', 'Advice'),
    'notice': ('core.domain.notice', 'Notice'),
    'procedure_experience': ('core.domain.procedure', 'ProcedureExperience'),
    'building_comment': ('core.domain.building', 'BuildingComment'),
}


class ReportsService(BaseService):
    def create_report(self, content_type: str, reference_id: int, reporter_id: int, reason: str):
        if content_type not in CONTENT_TYPE_MAP:
            raise ValueError(f"Tipo de contenido no válido: {content_type}")
        reason_stripped = reason.strip()
        if not reason_stripped:
            raise ValueError('La razón del reporte es obligatoria.')
        return Report.objects.create(
            content_type=content_type,
            reference_id=reference_id,
            reporter_id=reporter_id,
            reason=reason_stripped,
            status='pending'
        )

    def get_reports(self, status: str = None):
        qs = Report.objects.select_related('reporter').all()
        if status:
            qs = qs.filter(status=status)
        return qs.order_by('-created_at')

    def get_grouped_reports(self, status: str = None):
        from django.db.models import Count
        qs = Report.objects.values('content_type', 'reference_id')
        if status:
            qs = qs.filter(status=status)
        qs = qs.annotate(count=Count('id')).order_by('content_type', 'reference_id')
        result = []
        for g in qs:
            reports = Report.objects.filter(
                content_type=g['content_type'],
                reference_id=g['reference_id']
            ).select_related('reporter').order_by('-created_at')
            first = reports.first()
            result.append({
                'content_type': g['content_type'],
                'reference_id': g['reference_id'],
                'count': g['count'],
                'latest_report': {
                    'id': first.id,
                    'reporter_id': first.reporter_id,
                    'reporter_name': first.reporter.full_name if first.reporter else 'Anónimo',
                    'reason': first.reason,
                    'status': first.status,
                    'created_at': first.created_at.isoformat(),
                },
                'reports': [
                    {
                        'id': r.id,
                        'reporter_id': r.reporter_id,
                        'reporter_name': r.reporter.full_name if r.reporter else 'Anónimo',
                        'reason': r.reason,
                        'status': r.status,
                        'created_at': r.created_at.isoformat(),
                    }
                    for r in reports
                ],
            })
        return result

    def get_reported_content_preview(self, content_type: str, reference_id: int):
        module_path, class_name = CONTENT_TYPE_MAP.get(content_type, (None, None))
        if not module_path:
            return None
        import importlib
        module = importlib.import_module(module_path)
        model = getattr(module, class_name)
        obj = model.objects.filter(id=reference_id).first()
        if not obj:
            return None
        preview = {}
        if content_type == 'advice':
            preview = {'title': obj.title, 'content': obj.content[:200], 'user_id': obj.user_id}
            preview['user_name'] = obj.user.full_name if obj.user else 'Anónimo'
        elif content_type == 'notice':
            preview = {'title': obj.title, 'content': obj.description[:200], 'user_id': obj.user_id}
            preview['user_name'] = obj.user.full_name if obj.user else 'Anónimo'
        elif content_type == 'procedure_experience':
            preview = {'content': obj.comment[:200], 'user_id': obj.user_id}
            preview['user_name'] = obj.user.full_name if obj.user else 'Anónimo'
        elif content_type == 'building_comment':
            preview = {'content': obj.content[:200], 'user_id': obj.user_id}
            preview['user_name'] = obj.user.full_name if obj.user else 'Anónimo'
        return preview

    def dismiss_report(self, report_id: int):
        report = Report.objects.filter(id=report_id).first()
        if not report:
            raise ValueError('Reporte no encontrado.')
        report.status = 'resolved'
        report.save()
        # Also resolve all reports for same content
        Report.objects.filter(
            content_type=report.content_type,
            reference_id=report.reference_id
        ).update(status='resolved')

    def delete_reported_content(self, report_id: int):
        from core.domain.user import User
        report = Report.objects.filter(id=report_id).first()
        if not report:
            raise ValueError('Reporte no encontrado.')
        module_path, class_name = CONTENT_TYPE_MAP.get(report.content_type, (None, None))
        if not module_path:
            raise ValueError(f"Tipo de contenido no soportado: {report.content_type}")
        import importlib
        module = importlib.import_module(module_path)
        model = getattr(module, class_name)
        obj = model.objects.filter(id=report.reference_id).first()
        if obj:
            obj.delete()
        # Resolve all reports for this content
        Report.objects.filter(
            content_type=report.content_type,
            reference_id=report.reference_id
        ).update(status='resolved')
