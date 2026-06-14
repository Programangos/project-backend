from django.urls import path
from core.controllers.role_controller import RoleController
from core.controllers.advices_controller import AdvicesController, AdviceLikeController

urlpatterns = [
    path('roles/', RoleController.as_view(), name='roles'),
    path('advices/', AdvicesController.as_view(), name='advices'),
    path('advices/<int:advice_id>/like/', AdviceLikeController.as_view(), name='advice-like'),
]
