from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.professor_dashboard_view, name='professor_dashboard'),
    path('professor/materia/<int:materia_id>/turma/<int:turma_id>/', views.detalhar_turma_professor, name='detalhar_turma_professor'),
    path('professor/materia/<int:materia_id>/turma/<int:turma_id>/', views.ver_turma_professor, name='ver_turma_professor'),
    path('professor/aluno/<int:aluno_id>/detalhes/', views.ver_detalhes_aluno_professor, name='ver_detalhes_aluno_professor'),
    path('professor/inserir-nota/', views.inserir_nota, name="inserir_nota"),
]