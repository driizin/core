from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import (
    Materia,
    Turma,
    CustomUser,
    ProfessorMateriaTurma,
    Nota
)

@login_required
def detalhar_turma_professor(request, materia_id, turma_id):
    if request.user.tipo != 'professor':
        return redirect('login')

    materia = get_object_or_404(Materia, id=materia_id)
    turma = get_object_or_404(Turma, id=turma_id)

    vinculado = ProfessorMateriaTurma.objects.filter(
        professor=request.user,
        materia=materia,
        turma=turma
    ).exists()

    if not vinculado:
        messages.error(request, "Você não tem permissão para acessar esta turma.")
        return redirect('professor_dashboard')

    alunos = CustomUser.objects.filter(
        tipo='aluno',
        alunoturma__turma=turma
    ).distinct()

    notas_dict = {
        nota.aluno.id: nota for nota in Nota.objects.filter(
            materia=materia,
            turma=turma,
            aluno__in=alunos
        )
    }

    return render(request, 'professor/detalhar_turma.html', {
        'materia': materia,
        'turma': turma,
        'alunos': alunos,
        'notas_dict': notas_dict,
    })
    
@login_required
def ver_turma_professor(request, materia_id, turma_id):
    if request.user.tipo != 'professor':
        return redirect('login')

    materia = get_object_or_404(Materia, id=materia_id)
    turma = get_object_or_404(Turma, id=turma_id)

    if not ProfessorMateriaTurma.objects.filter(
        professor=request.user,
        materia=materia,
        turma=turma
    ).exists():
        messages.error(request, "Você não tem acesso a essa turma.")
        return redirect('professor_dashboard')

    alunos = CustomUser.objects.filter(
        tipo='aluno',
        alunoturma__turma=turma
    ).distinct()
    
    notas_dict = {
        nota.aluno_id: nota
        for nota in Nota.objects.filter(materia=materia, turma=turma)
    }

    return render(request, 'professor/detalhar_turma.html', {
        'materia': materia,
        'turma': turma,
        'alunos': alunos,
        'notas_dict': notas_dict
    })

@login_required
def ver_detalhes_aluno_professor(request, aluno_id):
    if request.user.tipo != 'professor':
        return redirect('login')

    aluno = get_object_or_404(CustomUser, id=aluno_id, tipo='aluno')
    turmas = Turma.objects.filter(alunoturma__aluno=aluno)

    return render(request, 'professor/detalhes_aluno.html', {
        'aluno': aluno,
        'turmas': turmas
    })