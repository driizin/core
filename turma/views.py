from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import Turma, Usuario
from core.decorators import role_required

@login_required
@role_required('admin')
def listar_turmas(request):
    turmas = Turma.objects.all()
    return render(request, 'admin/turmas_crud/listar_turmas.html', {'turmas': turmas})


@login_required
@role_required('admin')
def detalhar_turma(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    alunos = Usuario.objects.filter(alunoturma__turma=turma, tipo='aluno')
    return render(request, 'admin/turmas_crud/detalhar_turma.html', {'turma': turma, 'alunos': alunos})