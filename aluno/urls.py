from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.aluno_dashboard_view, name='aluno_dashboard'),
    path('boletim/', views.ver_boletim_aluno, name='ver_boletim_aluno'),
]