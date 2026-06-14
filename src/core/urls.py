from django.urls import path
from core.controllers.role_controller import RoleController
from core.controllers.advices_controller import AdvicesController, AdviceLikeController
from core.controllers.notices_controller import (
    NoticesController, NoticeLikeController, NoticeReportController
)


urlpatterns = [
    path('notices/', NoticesController.as_view(), name='notices'),
    path('notices/<int:notice_id>/like/', NoticeLikeController.as_view(), name='notice-like'),
    path('notices/<int:notice_id>/report/', NoticeReportController.as_view(), name='notice-report'),
    path('roles/', RoleController.as_view(), name='roles'),
    path('advices/', AdvicesController.as_view(), name='advices'),
    path('advices/<int:advice_id>/like/', AdviceLikeController.as_view(), name='advice-like'),
]
