from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import Turma, CustomUser

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