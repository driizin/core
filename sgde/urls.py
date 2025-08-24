from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('autenticacao.urls')),
    path('administrador/', include('administrador.urls')),
    path('professor/', include('professor.urls')),
    path('aluno/', include('aluno.urls')),
]
