from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('autenticacao.urls')),
    path('disciplinas/', include('disciplinas.urls')),
    path('matriculas/', include('matriculas.urls')),
    path('notas/', include('notas.urls')),
    path('turmas/', include('turmas.urls')),
    path('turmas_disciplinas/', include('turmas_disciplinas.urls')),
]
