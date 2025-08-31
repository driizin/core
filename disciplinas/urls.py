from django.urls import path
from . import views

urlpatterns = [
    path('admin/materias_crud/materias/', views.listar_materias, name='listar_materias'),
    path('admin/materias_crud/materias/<int:materia_id>/', views.detalhar_materia, name='detalhar_materia'),
    path('admin/professor_crud/professores/', views.gerenciar_professores, name='gerenciar_professores'),
    path('admin/professor_crud/professores/novo/', views.cadastrar_professor, name='cadastrar_professor'),
    path('admin/professor_crud/professores/<int:professor_id>/ver/', views.ver_detalhes_professor, name='ver_detalhes_professor'),
    path('admin/professor_crud/professores/<int:professor_id>/editar/', views.editar_professor, name='editar_professor'),
    path('admin/professor_crud/professores/<int:professor_id>/remover/', views.remover_professor, name='remover_professor'),
]