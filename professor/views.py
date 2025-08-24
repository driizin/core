from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from collections import defaultdict

from core.models import (
    Materia,
    Turma,
    CustomUser,
    ProfessorMateriaTurma,
    AlunoTurma,
    Nota
)

# === DASHBOARD ===

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

    print("DEBUG:", materias_com_turmas)

    return render(request, 'professor/professor_dashboard.html', {
        'materias_com_turmas': materias_com_turmas
    })

# === TURMAS COM MATÉRIAS ===


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
        messages.error(
            request, "Você não tem permissão para acessar esta turma.")
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


@csrf_exempt
@login_required
def inserir_nota(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Requisição inválida"}, status=400)

    aluno_id = request.POST.get("aluno_id")
    materia_id = request.POST.get("materia_id")
    turma_id = request.POST.get("turma_id")

    aluno = get_object_or_404(CustomUser, id=aluno_id)
    materia = get_object_or_404(Materia, id=materia_id)
    turma = get_object_or_404(Turma, id=turma_id)

    nota_obj, _ = Nota.objects.get_or_create(
        aluno=aluno,
        materia=materia,
        turma=turma
    )

    def parse_optional_float(val):
        try:
            if val == '' or val is None:
                return None
            f = float(val)
            return min(f, 100)
        except ValueError:
            return None

    nota_obj.nota_1_semestre1 = parse_optional_float(
        request.POST.get("nota_1_semestre1"))
    nota_obj.nota_2_semestre1 = parse_optional_float(
        request.POST.get("nota_2_semestre1"))
    nota_obj.paralela_1 = parse_optional_float(request.POST.get("paralela_1"))

    nota_obj.nota_1_semestre2 = parse_optional_float(
        request.POST.get("nota_1_semestre2"))
    nota_obj.nota_2_semestre2 = parse_optional_float(
        request.POST.get("nota_2_semestre2"))
    nota_obj.paralela_2 = parse_optional_float(request.POST.get("paralela_2"))

    nota_obj.nota_recuperacao = parse_optional_float(
        request.POST.get("nota_recuperacao"))

    try:
        nota_obj.save()
    except TypeError as e:
        return JsonResponse({"error": f"Erro ao calcular status: {str(e)}"}, status=500)

    status = nota_obj.status_final or "Pendente"
    badge_map = {
        "Aprovado": "bg-success text-white",
        "Reprovado na Final": "bg-danger text-white",
        "Reprovado": "bg-danger-subtle text-dark",
        "Requer Final": "bg-warning text-dark",
        "Pendente": "bg-warning text-dark"
    }
    badge_class = badge_map.get(status, "bg-secondary")

    return JsonResponse({
        "status": status,
        "badge_class": badge_class
    })
