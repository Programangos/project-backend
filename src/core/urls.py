from django.urls import path
from core.controllers.role_controller import RoleController

urlpatterns = [
    path('roles/', RoleController.as_view(), name='roles'),
]
