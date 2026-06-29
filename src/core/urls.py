from django.urls import path
from core.controllers.role_controller import RoleController
from core.controllers.advices_controller import AdvicesController, AdviceLikeController
from core.controllers.notices_controller import (
    NoticesController, NoticeLikeController, NoticeReportController
)
from core.controllers.auth_controller import (
    RegisterController, LoginController, ProfileController,
    ForgotPasswordController, ResetPasswordController,
)
from core.controllers.procedures_controller import (
    ProcedureExperienceController,
    ProcedureAvgTimeController,
    ProcedureExperienceVoteController,
)

urlpatterns = [
    path('notices/', NoticesController.as_view(), name='notices'),
    path('notices/<int:notice_id>/like/', NoticeLikeController.as_view(), name='notice-like'),
    path('notices/<int:notice_id>/report/', NoticeReportController.as_view(), name='notice-report'),
    path('roles/', RoleController.as_view(), name='roles'),
    path('advices/', AdvicesController.as_view(), name='advices'),
    path('advices/<int:advice_id>/like/', AdviceLikeController.as_view(), name='advice-like'),
    path('auth/register/', RegisterController.as_view(), name='register'),
    path('auth/login/', LoginController.as_view(), name='login'),
    path('auth/profile/<int:user_id>/', ProfileController.as_view(), name='profile'),
    path('auth/forgot-password/', ForgotPasswordController.as_view(), name='forgot-password'),
    path('auth/reset-password/', ResetPasswordController.as_view(), name='reset-password'),
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
        'experiences/<int:experience_id>/vote/',
        ProcedureExperienceVoteController.as_view(),
        name='experience-vote',
    ),
]
