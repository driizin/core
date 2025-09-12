from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import Usuario, Turma, AlunoTurma
from autenticacao.forms import AlunoCreateForm
from core.decorators import role_required

@login_required
@role_required('admin')
def gerenciar_alunos(request):
    alunos = Usuario.objects.filter(tipo='aluno').prefetch_related('alunoturma_set__turma')
    return render(request, 'admin/aluno_crud/gerenciar_alunos.html', {'alunos': alunos})


@login_required
@role_required('admin')
def cadastrar_aluno(request):
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
@role_required('admin')
def editar_aluno(request, aluno_id):
    aluno = get_object_or_404(Usuario, id=aluno_id, tipo='aluno')
    turma_atual = AlunoTurma.objects.filter(aluno=aluno).first()

    form = AlunoCreateForm(
        request.POST or None,
        instance=aluno,
        initial={'turmas': turma_atual.turma if turma_atual else None}
    )

    if request.method == 'POST' and form.is_valid():
        form.save()
        AlunoTurma.objects.filter(aluno=aluno).delete()
        AlunoTurma.objects.create(aluno=aluno, turma=form.cleaned_data['turmas'])
        messages.success(request, "Aluno atualizado com sucesso.")
        return redirect('gerenciar_alunos')

    return render(request, 'admin/aluno_crud/editar_aluno.html', {'form': form, 'aluno': aluno})


@login_required
@role_required('admin')
def remover_aluno(request, aluno_id):
    aluno = get_object_or_404(Usuario, id=aluno_id, tipo='aluno')

    if request.method == 'POST':
        aluno.delete()
        messages.success(request, "Aluno removido com sucesso.")
        return redirect('gerenciar_alunos')

    return render(request, 'admin/aluno_crud/remover_aluno.html', {'aluno': aluno})


@login_required
@role_required('admin')
def ver_detalhes_aluno(request, aluno_id):
    aluno = get_object_or_404(Usuario, id=aluno_id, tipo='aluno')
    turmas = Turma.objects.filter(alunoturma__aluno=aluno)
    return render(request, 'admin/aluno_crud/detalhes_aluno.html', {'aluno': aluno, 'turmas': turmas})