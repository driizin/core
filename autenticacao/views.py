from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from collections import defaultdict
from django.utils.timezone import now

from .forms import (
    EmailAuthenticationForm,
    ProfessorCreateForm,
    ProfessorMateriaTurmaFormSet,
    ProfessorMateriaTurmaForm,
    AlunoCreateForm
)

from core.models import Materia, Turma, CustomUser, ProfessorMateriaTurma, AlunoTurma


# === AUTENTICAÇÃO ===

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


# === DASHBOARDS ===

@login_required
def admin_dashboard_view(request):
    if request.user.tipo != 'admin':
        messages.error(request, "Acesso negado.")
        return redirect('login')
    return render(request, 'admin/admin_dashboard.html')


@login_required
def professor_dashboard_view(request):
    if request.user.tipo != 'professor':
        messages.error(request, "Acesso negado.")
        return redirect('login')
    return render(request, 'professor/professor_dashboard.html')


@login_required
def aluno_dashboard_view(request):
    if request.user.tipo != 'aluno':
        messages.error(request, "Acesso negado.")
        return redirect('login')
    return render(request, 'aluno/aluno_dashboard.html')


# === ADMIN - PROFESSORES ===

@login_required
def gerenciar_professores(request):
    if request.user.tipo != 'admin':
        messages.error(request, "Acesso negado.")
        return redirect('login')

    professores = CustomUser.objects.filter(tipo='professor')
    return render(request, 'admin/professor_crud/gerenciar_professores.html', {'professores': professores})


@login_required
def ver_detalhes_professor(request, professor_id):
    if request.user.tipo != 'admin':
        messages.error(request, "Acesso negado.")
        return redirect('login')

    professor = get_object_or_404(
        CustomUser, id=professor_id, tipo='professor')
    vinculos = ProfessorMateriaTurma.objects.filter(professor=professor)

    return render(request, 'admin/professor_crud/detalhes_professor.html', {
        'professor': professor,
        'vinculos': vinculos,
    })


@login_required
def cadastrar_professor(request):
    if request.user.tipo != 'admin':
        messages.error(request, "Acesso negado.")
        return redirect('login')

    if request.method == 'POST':
        form = ProfessorCreateForm(request.POST)
        formset = ProfessorMateriaTurmaFormSet(
            request.POST, queryset=ProfessorMateriaTurma.objects.none())

        if form.is_valid() and formset.is_valid():
            professor = form.save(commit=False)
            professor.tipo = 'professor'
            professor.username = professor.cpf
            professor.email = f"{professor.cpf}@docente.com"
            professor.set_password("Senha123#")
            professor.senha_temporaria = True
            professor.save()

            for f in formset:
                if f.cleaned_data:
                    vinculo = f.save(commit=False)
                    vinculo.professor = professor
                    vinculo.save()

                    vinculo.materia.professores.add(professor)
                    vinculo.materia.turmas.add(vinculo.turma)

            messages.success(request, "Professor cadastrado com sucesso.")
            return redirect('gerenciar_professores')
        else:
            print("ERROS DO FORMULÁRIO:")
            print(form.errors)
            print("ERROS DO FORMSET:")
            print(formset.errors)
            messages.error(
                request, "Erro ao cadastrar o professor. Verifique os campos abaixo.")
    else:
        form = ProfessorCreateForm()
        formset = ProfessorMateriaTurmaFormSet(
            queryset=ProfessorMateriaTurma.objects.none())

    return render(request, 'admin/professor_crud/cadastrar_professor.html', {
        'form': form,
        'formset': formset
    })


@login_required
def editar_professor(request, professor_id):
    if request.user.tipo != 'admin':
        messages.error(request, "Acesso negado.")
        return redirect('login')

    professor = get_object_or_404(
        CustomUser, id=professor_id, tipo='professor')

    formset = ProfessorMateriaTurmaFormSet(
        request.POST or None,
        queryset=ProfessorMateriaTurma.objects.filter(professor=professor)
    )
    form = ProfessorCreateForm(request.POST or None, instance=professor)

    if request.method == 'POST':
        if form.is_valid() and formset.is_valid():
            form.save()

            ProfessorMateriaTurma.objects.filter(professor=professor).delete()

            for f in formset:
                if f.cleaned_data:
                    vinculo = f.save(commit=False)
                    vinculo.professor = professor
                    vinculo.save()

                    vinculo.materia.professores.add(professor)
                    vinculo.materia.turmas.add(vinculo.turma)

            messages.success(request, "Professor atualizado com sucesso.")
            return redirect('gerenciar_professores')
        else:
            print("FORM ERROS:", form.errors)
            print("FORMSET ERROS:", formset.errors)

    return render(request, 'admin/professor_crud/editar_professor.html', {
        'form': form,
        'formset': formset,
        'professor': professor
    })


@login_required
def remover_professor(request, professor_id):
    if request.user.tipo != 'admin':
        messages.error(request, "Acesso negado.")
        return redirect('login')

    professor = get_object_or_404(
        CustomUser, id=professor_id, tipo='professor')

    if request.method == 'POST':
        professor.delete()
        messages.success(request, "Professor removido com sucesso.")
        return redirect('gerenciar_professores')

    return render(request, 'admin/professor_crud/remover_professor.html', {
        'professor': professor
    })


# === PERFIL ===

@login_required
def ver_perfil(request):
    user = request.user
    turmas = []
    vinculos = []

    if user.tipo == 'aluno':
        turmas = Turma.objects.filter(alunoturma__aluno=user)
    elif user.tipo == 'professor':
        vinculos = ProfessorMateriaTurma.objects.filter(professor=user).select_related('materia', 'turma')

    return render(request, 'perfil/ver_perfil.html', {
        'user': user,
        'turmas': turmas,
        'vinculos': vinculos
    })

# === ADMIN - ALUNOS ===


@login_required
def gerenciar_alunos(request):
    if request.user.tipo != 'admin':
        messages.error(request, "Acesso negado.")
        return redirect('login')

    alunos = CustomUser.objects.filter(
        tipo='aluno').prefetch_related('alunoturma_set__turma')

    return render(request, 'admin/aluno_crud/gerenciar_alunos.html', {
        'alunos': alunos,
    })


@login_required
def cadastrar_aluno(request):
    if request.user.tipo != 'admin':
        messages.error(request, "Acesso negado.")
        return redirect('login')

    if request.method == 'POST':
        form = AlunoCreateForm(request.POST)
        if form.is_valid():
            aluno = form.save(commit=False)
            aluno.tipo = 'aluno'
            aluno.username = aluno.cpf
            aluno.email = f"{aluno.cpf}@discente.com"
            aluno.set_password("Senha123#")
            aluno.senha_temporaria = True
            aluno.save()
            form.save_m2m()

            turma = form.cleaned_data['turmas']
            AlunoTurma.objects.create(aluno=aluno, turma=turma)

            messages.success(request, "Aluno cadastrado com sucesso.")
            return redirect('gerenciar_alunos')
    else:
        form = AlunoCreateForm()

    return render(request, 'admin/aluno_crud/cadastrar_aluno.html', {'form': form})


@login_required
def editar_aluno(request, aluno_id):
    if request.user.tipo != 'admin':
        messages.error(request, "Acesso negado.")
        return redirect('login')

    aluno = get_object_or_404(CustomUser, id=aluno_id, tipo='aluno')

    turma_atual = AlunoTurma.objects.filter(aluno=aluno).first()
    initial_data = {
        'turmas': turma_atual.turma if turma_atual else None,
    }

    form = AlunoCreateForm(request.POST or None, instance=aluno, initial=initial_data)

    if request.method == 'POST':
        if form.is_valid():
            form.save()

            AlunoTurma.objects.filter(aluno=aluno).delete()
            AlunoTurma.objects.create(aluno=aluno, turma=form.cleaned_data['turmas'])

            messages.success(request, "Aluno atualizado com sucesso.")
            return redirect('gerenciar_alunos')

    return render(request, 'admin/aluno_crud/editar_aluno.html', {
        'form': form,
        'aluno': aluno
    })


@login_required
def remover_aluno(request, aluno_id):
    if request.user.tipo != 'admin':
        messages.error(request, "Acesso negado.")
        return redirect('login')

    aluno = get_object_or_404(CustomUser, id=aluno_id, tipo='aluno')

    if request.method == 'POST':
        aluno.delete()
        messages.success(request, "Aluno removido com sucesso.")
        return redirect('gerenciar_alunos')

    return render(request, 'admin/aluno_crud/remover_aluno.html', {'aluno': aluno})


@login_required
def ver_detalhes_aluno(request, aluno_id):
    if request.user.tipo != 'admin':
        messages.error(request, "Acesso negado.")
        return redirect('login')

    aluno = get_object_or_404(CustomUser, id=aluno_id, tipo='aluno')
    turmas = Turma.objects.filter(alunoturma__aluno=aluno)

    return render(request, 'admin/aluno_crud/detalhes_aluno.html', {
        'aluno': aluno,
        'turmas': turmas
    })

# === ADMIN - TURMAS ===


@login_required
def listar_turmas(request):
    if request.user.tipo != 'admin':
        messages.error(request, "Acesso negado.")
        return redirect('login')

    turmas = Turma.objects.all()
    return render(request, 'admin/turmas_crud/listar_turmas.html', {'turmas': turmas})


@login_required
def detalhar_turma(request, turma_id):
    if request.user.tipo != 'admin':
        messages.error(request, "Acesso negado.")
        return redirect('login')

    turma = get_object_or_404(Turma, id=turma_id)
    alunos = CustomUser.objects.filter(alunoturma__turma=turma, tipo='aluno')

    return render(request, 'admin/turmas_crud/detalhar_turma.html', {
        'turma': turma,
        'alunos': alunos
    })

# === ADMIN - MATÉRIAS ===


@login_required
def listar_materias(request):
    if request.user.tipo != 'admin':
        messages.error(request, "Acesso negado.")
        return redirect('login')

    materias = Materia.objects.all()
    return render(request, 'admin/materias_crud/listar_materias.html', {'materias': materias})


@login_required
def detalhar_materia(request, materia_id):
    if request.user.tipo != 'admin':
        messages.error(request, "Acesso negado.")
        return redirect('login')

    materia = get_object_or_404(Materia, id=materia_id)
    vinculos = ProfessorMateriaTurma.objects.filter(
        materia=materia).select_related('professor', 'turma')

    professores_com_turmas = defaultdict(list)

    for v in vinculos:
        professores_com_turmas[v.professor].append(v.turma.nome)

    context_data = [
        (prof, turmas) for prof, turmas in professores_com_turmas.items()
    ]

    return render(request, 'admin/materias_crud/detalhar_materia.html', {
        'materia': materia,
        'professores_com_turmas': context_data
    })