from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('autenticacao.urls')),
    path('materia/', include('materia.urls')),
    path('aluno_turma/', include('aluno_turma.urls')),
    path('nota/', include('nota.urls')),
    path('turma/', include('turma.urls')),
    path('professor_materia_turma/', include('professor_materia_turma.urls')),
]
