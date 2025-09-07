from django.urls import path
from . import views

urlpatterns = [
    path('aluno/boletim/', views.ver_boletim_aluno, name='ver_boletim_aluno'),
    path('professor/inserir-nota/', views.inserir_nota, name="inserir_nota"),
]