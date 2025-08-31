from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirect_por_tipo, name='inicio'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard_admin/', views.admin_dashboard_view, name='admin_dashboard'),
    path('dashboard_professor/', views.professor_dashboard_view, name='professor_dashboard'),
    path('dashboard_aluno/', views.aluno_dashboard_view, name='aluno_dashboard'),
    path('perfil/', views.ver_perfil, name='ver_perfil'),
    path('perfil/alterar_senha/', views.alterar_senha, name='alterar_senha'),
]