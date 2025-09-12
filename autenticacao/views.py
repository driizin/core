from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from collections import defaultdict
from .forms import EmailAuthenticationForm
from core.models import Usuario, ProfessorMateriaTurma, Nota, Turma, AlunoTurma
from core.decorators import role_required

@login_required
def redirect_por_tipo(request):
    # CORREÇÃO: Acesse o tipo através do profile
    if hasattr(request.user, 'profile'):
        if request.user.profile.tipo == 'admin':
            return redirect('admin_dashboard')
        elif request.user.profile.tipo == 'professor':
            return redirect('professor_dashboard')
        elif request.user.profile.tipo == 'aluno':
            return redirect('aluno_dashboard')
    # Se não tem profile, redireciona para login
    return redirect('login')

def login_view(request):
    # CORREÇÃO: Verificação correta para evitar loop
    if request.user.is_authenticated:
        # Se já está autenticado, redireciona baseado no tipo
        if hasattr(request.user, 'profile'):
            if request.user.profile.tipo == 'admin':
                return redirect('admin_dashboard')
            elif request.user.profile.tipo == 'professor':
                return redirect('professor_dashboard')
            elif request.user.profile.tipo == 'aluno':
                return redirect('aluno_dashboard')
        # Se autenticado mas sem profile, faz logout e mostra erro
        logout(request)
        messages.error(request, "Perfil de usuário não configurado. Entre em contato com o administrador.")
        return redirect('login')
    
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                messages.success(
                    request, f"Bem-vindo(a), {user.first_name or user.email}")
                
                # CORREÇÃO: Acesse o tipo através do profile
                if hasattr(user, 'profile'):
                    if user.profile.tipo == 'admin':
                        return redirect('admin_dashboard')
                    elif user.profile.tipo == 'professor':
                        return redirect('professor_dashboard')
                    elif user.profile.tipo == 'aluno':
                        return redirect('aluno_dashboard')
                
                messages.warning(request, "Tipo de usuário não reconhecido ou profile não configurado.")
                logout(request)  # Desloga se não tem profile
                return redirect('login')
            else:
                messages.error(request, "Email ou senha inválidos.")
        else:
            messages.error(request, "Email ou senha inválidos.")
    else:
        form = EmailAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Você foi desconectado(a).")
    return redirect('login')

@login_required
@role_required('admin')
def admin_dashboard_view(request):
    return render(request, 'admin/admin_dashboard.html')

@login_required
@role_required('professor')
def professor_dashboard_view(request):
    vinculos = ProfessorMateriaTurma.objects.filter(professor=request.user).select_related('materia', 'turma')

    materias_com_turmas = defaultdict(list)
    for v in vinculos:
        materias_com_turmas[v.materia].append(v.turma)

    return render(request, 'professor/professor_dashboard.html', {
        'materias_com_turmas': dict(materias_com_turmas)
    })

@login_required
@role_required('aluno')
def aluno_dashboard_view(request):
    aluno = request.user
    notas = Nota.objects.filter(aluno=aluno).select_related('materia', 'turma')

    return render(request, 'aluno/aluno_dashboard.html', {
        'notas': notas,
        'aluno': aluno
    })

@login_required
def ver_perfil(request):
    user = request.user
    turmas = []
    vinculos = []

    # CORREÇÃO: Acesse o tipo através do profile
    if hasattr(user, 'profile'):
        if user.profile.tipo == 'aluno':
            turmas = Turma.objects.filter(alunoturma__aluno=user)
        elif user.profile.tipo == 'professor':
            vinculos = ProfessorMateriaTurma.objects.filter(
                professor=user).select_related('materia', 'turma')

    return render(request, 'perfil/ver_perfil.html', {
        'user': user,
        'turmas': turmas,
        'vinculos': vinculos
    })

@login_required
@role_required('professor', 'aluno')
def alterar_senha(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            print(f"[LOG] Senha alterada por: {user.username} em {now()}")
            
            # CORREÇÃO: Acesse o profile para alterar senha_temporaria
            if hasattr(user, 'profile'):
                user.profile.senha_temporaria = False
                user.profile.save()
            
            update_session_auth_hash(request, user)
            messages.success(request, "Senha atualizada com sucesso.")
            return redirect('ver_perfil')
        else:
            messages.error(request, "Corrija os erros abaixo.")
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'perfil/alterar_senha.html', {'form': form})