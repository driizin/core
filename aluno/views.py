from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.models import AlunoTurma, Materia, Nota

# === DASHBOARD ===

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

# === BOLETIM ===


@login_required
def ver_boletim_aluno(request):
    if request.user.tipo != 'aluno':
        return redirect('login')

    aluno = request.user

    turmas_ids = AlunoTurma.objects.filter(
        aluno=aluno).values_list('turma_id', flat=True)

    materias = Materia.objects.filter(turmas__id__in=turmas_ids).distinct()

    boletim = []
    for materia in materias:
        nota = Nota.objects.filter(aluno=aluno, materia=materia).first()
        boletim.append({
            'materia': materia,
            'nota': nota
        })

    return render(request, 'aluno/boletim.html', {
        'boletim': boletim,
        'aluno': aluno
    })
