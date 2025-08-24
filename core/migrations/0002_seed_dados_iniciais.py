from django.db import migrations


def criar_materias_turmas(apps, schema_editor):
    Materia = apps.get_model('core', 'Materia')
    Turma = apps.get_model('core', 'Turma')

    materias = [
        'Português',
        'Matemática',
        'Geografia',
        'História',
        'Química',
        'Física',
        'Biologia',
    ]

    turmas = [
        '1ºA', '1ºB',
        '2ºA', '2ºB',
        '3ºA', '3ºB',
    ]

    for nome in materias:
        Materia.objects.get_or_create(nome=nome)

    for nome in turmas:
        Turma.objects.get_or_create(nome=nome)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),  
    ]

    operations = [
        migrations.RunPython(criar_materias_turmas),
    ]
