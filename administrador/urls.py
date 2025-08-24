from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('professores/', views.gerenciar_professores, name='gerenciar_professores'),
    path('alunos/', views.gerenciar_alunos, name='gerenciar_alunos'),
    path('materias/', views.listar_materias, name='listar_materias'),
    path('turmas/', views.listar_turmas, name='listar_turmas'),
    path('professores/novo/', views.cadastrar_professor, name='cadastrar_professor'),
    path('professores/<int:professor_id>/ver/', views.ver_detalhes_professor, name='ver_detalhes_professor'),
    path('professores/<int:professor_id>/editar/', views.editar_professor, name='editar_professor'),
    path('professores/<int:professor_id>/remover/', views.remover_professor, name='remover_professor'),
    path('alunos/novo/', views.cadastrar_aluno, name='cadastrar_aluno'),
    path('alunos/<int:aluno_id>/editar/', views.editar_aluno, name='editar_aluno'),
    path('alunos/<int:aluno_id>/remover/', views.remover_aluno, name='remover_aluno'),
    path('alunos/<int:aluno_id>/ver/', views.ver_detalhes_aluno, name='ver_detalhes_aluno'),
    path('materias/<int:materia_id>/', views.detalhar_materia, name='detalhar_materia'),
    path('turmas/<int:turma_id>/', views.detalhar_turma, name='detalhar_turma'),
]