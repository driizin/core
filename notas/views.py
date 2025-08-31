from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from core.models import CustomUser, Materia, Turma, Nota, AlunoTurma

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

    nota_obj.nota_1_semestre1 = parse_optional_float(request.POST.get("nota_1_semestre1"))
    nota_obj.nota_2_semestre1 = parse_optional_float(request.POST.get("nota_2_semestre1"))
    nota_obj.paralela_1 = parse_optional_float(request.POST.get("paralela_1"))

    nota_obj.nota_1_semestre2 = parse_optional_float(request.POST.get("nota_1_semestre2"))
    nota_obj.nota_2_semestre2 = parse_optional_float(request.POST.get("nota_2_semestre2"))
    nota_obj.paralela_2 = parse_optional_float(request.POST.get("paralela_2"))

    nota_obj.nota_recuperacao = parse_optional_float(request.POST.get("nota_recuperacao"))

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

@login_required
def ver_boletim_aluno(request):
    if request.user.tipo != 'aluno':
        return redirect('login')

    aluno = request.user

    turmas_ids = AlunoTurma.objects.filter(aluno=aluno).values_list('turma_id', flat=True)

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