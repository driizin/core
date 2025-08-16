from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    # Acesso e controle
    path('', views.redirect_por_tipo, name='inicio'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Perfil
    path('perfil/', views.ver_perfil, name='ver_perfil'),
    path('perfil/alterar_senha/', views.alterar_senha, name='alterar_senha'),

    # Dashboards
    path('admin/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('professor/dashboard/', views.professor_dashboard_view, name='professor_dashboard'),
    path('aluno/dashboard/', views.aluno_dashboard_view, name='aluno_dashboard'),

    # ADMIN - Dashboard
    path('admin/professor_crud/professores/', views.gerenciar_professores, name='gerenciar_professores'),
    path('admin/aluno_crud/alunos/', views.gerenciar_alunos, name='gerenciar_alunos'),
    path('admin/materias_crud/materias/', views.listar_materias, name='listar_materias'),
    path('admin/turmas_crud/turmas/', views.listar_turmas, name='listar_turmas'),
    
    # ADMIN -  Professores
    path('admin/professor_crud/professores/novo/', views.cadastrar_professor, name='cadastrar_professor'),
    path('admin/professor_crud/professores/<int:professor_id>/ver/', views.ver_detalhes_professor, name='ver_detalhes_professor'),
    path('admin/professor_crud/professores/<int:professor_id>/editar/', views.editar_professor, name='editar_professor'),
    path('admin/professor_crud/professores/<int:professor_id>/remover/', views.remover_professor, name='remover_professor'),
    
    # ADMIN - Alunos
    path('admin/aluno_crud/alunos/novo/', views.cadastrar_aluno, name='cadastrar_aluno'),
    path('admin/aluno_crud/alunos/<int:aluno_id>/editar/', views.editar_aluno, name='editar_aluno'),
    path('admin/aluno_crud/alunos/<int:aluno_id>/remover/', views.remover_aluno, name='remover_aluno'),
    path('admin/aluno_crud/alunos/<int:aluno_id>/ver/', views.ver_detalhes_aluno, name='ver_detalhes_aluno'),
    
    # ADMIN - Materias
    path('admin/materias_crud/materias/<int:materia_id>/', views.detalhar_materia, name='detalhar_materia'),
    
    # ADMIN - Turmas
    path('admin/turmas_crud/turmas/<int:turma_id>/', views.detalhar_turma, name='detalhar_turma'),
    
    # PROFESSOR - Dashboard
    path('professor/materia/<int:materia_id>/turma/<int:turma_id>/', views.detalhar_turma_professor, name='detalhar_turma_professor'),
    
    # PROFESSOR - Turmas/Matérias/Notas
    path('professor/materia/<int:materia_id>/turma/<int:turma_id>/', views.ver_turma_professor, name='ver_turma_professor'),
    path('professor/aluno/<int:aluno_id>/detalhes/', views.ver_detalhes_aluno_professor, name='ver_detalhes_aluno_professor'),
]
