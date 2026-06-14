from django.urls import path
from core.controllers.role_controller import RoleController
from core.controllers.advices_controller import AdvicesController, AdviceLikeController
from core.controllers.auth_controller import RegisterController, LoginController, ProfileController

urlpatterns = [
    path('roles/', RoleController.as_view(), name='roles'),
    path('advices/', AdvicesController.as_view(), name='advices'),
    path('advices/<int:advice_id>/like/', AdviceLikeController.as_view(), name='advice-like'),
    path('auth/register/', RegisterController.as_view(), name='register'),
    path('auth/login/', LoginController.as_view(), name='login'),
    path('auth/profile/<int:user_id>/', ProfileController.as_view(), name='profile'),
]
