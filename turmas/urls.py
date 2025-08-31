from django.urls import path
from . import views

urlpatterns = [
    path('admin/turmas_crud/turmas/', views.listar_turmas, name='listar_turmas'),
    path('admin/turmas_crud/turmas/<int:turma_id>/', views.detalhar_turma, name='detalhar_turma'),
]