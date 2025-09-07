from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from collections import defaultdict
from autenticacao.forms import (
    ProfessorCreateForm,
    ProfessorMateriaTurmaFormSet
)
from core.models import Materia, CustomUser, ProfessorMateriaTurma, Turma
from core.decorators import role_required

@login_required
@role_required('admin')
def listar_materias(request):
    materias = Materia.objects.all()
    return render(request, 'admin/materias_crud/listar_materias.html', {'materias': materias})


@login_required
@role_required('admin')
def detalhar_materia(request, materia_id):
    materia = get_object_or_404(Materia, id=materia_id)
    vinculos = ProfessorMateriaTurma.objects.filter(materia=materia).select_related('professor', 'turma')

    professores_com_turmas = defaultdict(list)
    for v in vinculos:
        professores_com_turmas[v.professor].append(v.turma.nome)

    context_data = [(prof, turmas) for prof, turmas in professores_com_turmas.items()]
    return render(request, 'admin/materias_crud/detalhar_materia.html', {
        'materia': materia,
        'professores_com_turmas': context_data
    })
    
@login_required
@role_required('admin')
def gerenciar_professores(request):
    professores = CustomUser.objects.filter(tipo='professor')
    return render(request, 'admin/professor_crud/gerenciar_professores.html', {'professores': professores})


@login_required
@role_required('admin')
def ver_detalhes_professor(request, professor_id):
    professor = get_object_or_404(CustomUser, id=professor_id, tipo='professor')
    vinculos = ProfessorMateriaTurma.objects.filter(professor=professor)

    return render(request, 'admin/professor_crud/detalhes_professor.html', {
        'professor': professor,
        'vinculos': vinculos,
    })


@login_required
@role_required('admin')
def cadastrar_professor(request):
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
            messages.error(request, "Erro ao cadastrar o professor. Verifique os campos abaixo.")
    else:
        form = ProfessorCreateForm()
        formset = ProfessorMateriaTurmaFormSet(queryset=ProfessorMateriaTurma.objects.none())

    return render(request, 'admin/professor_crud/cadastrar_professor.html', {
        'form': form,
        'formset': formset
    })


@login_required
@role_required('admin')
def editar_professor(request, professor_id):
    professor = get_object_or_404(CustomUser, id=professor_id, tipo='professor')

    formset = ProfessorMateriaTurmaFormSet(
        request.POST or None,
        queryset=ProfessorMateriaTurma.objects.filter(professor=professor)
    )
    form = ProfessorCreateForm(request.POST or None, instance=professor)

    if request.method == 'POST' and form.is_valid() and formset.is_valid():
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

    return render(request, 'admin/professor_crud/editar_professor.html', {
        'form': form,
        'formset': formset,
        'professor': professor
    })


@login_required
@role_required('admin')
def remover_professor(request, professor_id):
    professor = get_object_or_404(CustomUser, id=professor_id, tipo='professor')

    if request.method == 'POST':
        professor.delete()
        messages.success(request, "Professor removido com sucesso.")
        return redirect('gerenciar_professores')

    return render(request, 'admin/professor_crud/remover_professor.html', {'professor': professor})