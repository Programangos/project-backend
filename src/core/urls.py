from django.urls import path
from core.controllers.role_controller import RoleController
from core.controllers.advices_controller import (
    AdvicesController, AdviceLikeController, AdviceDeleteController
)
from core.controllers.notices_controller import (
    NoticesController, NoticeLikeController,
    NoticeDeleteController, NoticeReportController
)
from core.controllers.auth_controller import (
    RegisterController, LoginController, ProfileController,
    ForgotPasswordController, ResetPasswordController,
)
from core.controllers.procedures_controller import (
    ProcedureListController,
    ProcedureCreateController,
    ProcedureDeleteController,
    ProcedureExperienceController,
    ProcedureAvgTimeController,
    ProcedureExperienceVoteController,
    ProcedureExperienceDeleteController,
)
from core.controllers.admin_controller import (
    AdminListUsersController,
    AdminDeleteUserController,
    AdminUpdateRoleController,
)
from core.controllers.buildings_controller import (
    BuildingCommentListCreateController,
    BuildingCommentDeleteController,
)
from core.controllers.reports_controller import (
    CreateReportController,
    AdminReportListController,
    AdminReportDismissController,
    AdminReportDeleteContentController,
)
from core.controllers.zone_controller import (
    ZoneListController,
    ZoneDetailController,
)

urlpatterns = [
    path('reports/', CreateReportController.as_view(), name='create-report'),
    path('notices/', NoticesController.as_view(), name='notices'),
    path('notices/<int:notice_id>/like/', NoticeLikeController.as_view(), name='notice-like'),
    path('notices/<int:notice_id>/', NoticeDeleteController.as_view(), name='notice-delete'),
    path('notices/<int:notice_id>/report/', NoticeReportController.as_view(), name='notice-report'),
    path('roles/', RoleController.as_view(), name='roles'),
    path('advices/', AdvicesController.as_view(), name='advices'),
    path('advices/<int:advice_id>/', AdviceDeleteController.as_view(), name='advice-delete'),
    path('advices/<int:advice_id>/like/', AdviceLikeController.as_view(), name='advice-like'),
    path('auth/register/', RegisterController.as_view(), name='register'),
    path('auth/login/', LoginController.as_view(), name='login'),
    path('auth/profile/<int:user_id>/', ProfileController.as_view(), name='profile'),
    path('auth/forgot-password/', ForgotPasswordController.as_view(), name='forgot-password'),
    path('auth/reset-password/', ResetPasswordController.as_view(), name='reset-password'),
    path('procedures/', ProcedureListController.as_view(), name='procedure-list'),
    path('procedures/create/', ProcedureCreateController.as_view(), name='procedure-create'),
    path('procedures/<int:procedure_id>/', ProcedureDeleteController.as_view(), name='procedure-delete'),
    path(
        'procedures/<int:procedure_id>/experiences/',
        ProcedureExperienceController.as_view(),
        name='procedure-experiences',
    ),
    path(
        'procedures/<int:procedure_id>/avg-time/',
        ProcedureAvgTimeController.as_view(),
        name='procedure-avg-time',
    ),
    path(
        'experiences/<int:experience_id>/',
        ProcedureExperienceDeleteController.as_view(),
        name='experience-delete',
    ),
    path(
        'experiences/<int:experience_id>/vote/',
        ProcedureExperienceVoteController.as_view(),
        name='experience-vote',
    ),
    path(
        'buildings/<int:building_id>/comments/',
        BuildingCommentListCreateController.as_view(),
        name='building-comments',
    ),
    path(
        'buildings/<int:building_id>/comments/<int:comment_id>/',
        BuildingCommentDeleteController.as_view(),
        name='building-comment-delete',
    ),
    path('admin/reports/', AdminReportListController.as_view(), name='admin-reports'),
    path('admin/reports/<int:report_id>/dismiss/', AdminReportDismissController.as_view(), name='admin-report-dismiss'),
    path('admin/reports/<int:report_id>/content/', AdminReportDeleteContentController.as_view(), name='admin-report-delete-content'),
    path('admin/users/', AdminListUsersController.as_view(), name='admin-users'),
    path('admin/users/<int:user_id>/', AdminDeleteUserController.as_view(), name='admin-delete-user'),
    path('admin/users/<int:user_id>/role/', AdminUpdateRoleController.as_view(), name='admin-update-role'),
    path('zones/', ZoneListController.as_view(), name='zone-list'),
    path('zones/<int:pk>/', ZoneDetailController.as_view(), name='zone-detail'),
]
