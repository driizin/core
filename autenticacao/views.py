from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from collections import defaultdict
from .forms import EmailAuthenticationForm
from core.models import CustomUser, ProfessorMateriaTurma, Nota, Turma, AlunoTurma

@login_required
def redirect_por_tipo(request):
    if request.user.tipo == 'admin':
        return redirect('admin_dashboard')
    elif request.user.tipo == 'professor':
        return redirect('professor_dashboard')
    elif request.user.tipo == 'aluno':
        return redirect('aluno_dashboard')
    return redirect('login')


def login_view(request):
    if request.user.is_authenticated:
        return redirect_por_tipo(request)
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
                if user.tipo == 'admin':
                    return redirect('admin_dashboard')
                elif user.tipo == 'professor':
                    return redirect('professor_dashboard')
                elif user.tipo == 'aluno':
                    return redirect('aluno_dashboard')
                messages.warning(request, "Tipo de usuário não reconhecido.")
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
def admin_dashboard_view(request):
    if request.user.tipo != 'admin':
        messages.error(request, "Acesso negado.")
        return redirect('login')
    return render(request, 'admin/admin_dashboard.html')

@login_required
def professor_dashboard_view(request):
    if request.user.tipo != 'professor':
        return redirect('login')

    vinculos = ProfessorMateriaTurma.objects.filter(
        professor=request.user).select_related('materia', 'turma')

    materias_com_turmas = defaultdict(list)

    for v in vinculos:
        materias_com_turmas[v.materia].append(v.turma)

    materias_com_turmas = dict(materias_com_turmas)

    return render(request, 'professor/professor_dashboard.html', {
        'materias_com_turmas': materias_com_turmas
    })

@login_required
def aluno_dashboard_view(request):
    if request.user.tipo != 'aluno':
        return redirect('login')

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

    if user.tipo == 'aluno':
        turmas = Turma.objects.filter(alunoturma__aluno=user)
    elif user.tipo == 'professor':
        vinculos = ProfessorMateriaTurma.objects.filter(
            professor=user).select_related('materia', 'turma')

    return render(request, 'perfil/ver_perfil.html', {
        'user': user,
        'turmas': turmas,
        'vinculos': vinculos
    })


@login_required
def alterar_senha(request):
    if request.user.tipo not in ['professor', 'aluno']:
        messages.error(request, "Acesso negado.")
        return redirect('ver_perfil')

    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            print(f"[LOG] Senha alterada por: {user.username} em {now()}")
            user.senha_temporaria = False
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Senha atualizada com sucesso.")
            return redirect('ver_perfil')
        else:
            messages.error(request, "Corrija os erros abaixo.")
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'perfil/alterar_senha.html', {'form': form})