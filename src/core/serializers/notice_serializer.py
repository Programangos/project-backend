from rest_framework import serializers
from core.domain.notice import Notice, NoticeLike
from core.domain.report import Report


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['id', 'title', 'description', 'category',
                  'is_official', 'expiration_date', 'user_id', 'created_at']
        read_only_fields = ['id', 'is_official', 'user_id', 'created_at']


class NoticeLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeLike
        fields = ['user_id', 'notice_id', 'created_at']
        read_only_fields = ['user_id', 'created_at']


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'content_type', 'reference_id',
                  'reporter_id', 'reason', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']
