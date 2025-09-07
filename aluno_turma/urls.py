from django.urls import path
from . import views

urlpatterns = [
    path('admin/aluno_crud/alunos/', views.gerenciar_alunos, name='gerenciar_alunos'),
    path('admin/aluno_crud/alunos/novo/', views.cadastrar_aluno, name='cadastrar_aluno'),
    path('admin/aluno_crud/alunos/<int:aluno_id>/editar/', views.editar_aluno, name='editar_aluno'),
    path('admin/aluno_crud/alunos/<int:aluno_id>/remover/', views.remover_aluno, name='remover_aluno'),
    path('admin/aluno_crud/alunos/<int:aluno_id>/ver/', views.ver_detalhes_aluno, name='ver_detalhes_aluno'),
]