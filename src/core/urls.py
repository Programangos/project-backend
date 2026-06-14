from django.urls import path
from core.controllers.role_controller import RoleController
from core.controllers.advices_controller import AdvicesController, AdviceLikeController
from core.controllers.auth_controller import RegisterController, LoginController, ProfileController
from core.controllers.procedures_controller import ProcedureExperienceController, ProcedureAvgTimeController, ProcedureExperienceVoteController

urlpatterns = [
    path('roles/', RoleController.as_view(), name='roles'),
    path('advices/', AdvicesController.as_view(), name='advices'),
    path('advices/<int:advice_id>/like/', AdviceLikeController.as_view(), name='advice-like'),
    path('auth/register/', RegisterController.as_view(), name='register'),
    path('auth/login/', LoginController.as_view(), name='login'),
    path('auth/profile/<int:user_id>/', ProfileController.as_view(), name='profile'),
    path('procedures/<int:procedure_id>/experiences/', ProcedureExperienceController.as_view(), name='procedure-experiences'),
    path('procedures/<int:procedure_id>/avg-time/', ProcedureAvgTimeController.as_view(), name='procedure-avg-time'),
    path('experiences/<int:experience_id>/vote/', ProcedureExperienceVoteController.as_view(), name='experience-vote'),
]
