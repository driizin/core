from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    TIPO_CHOICES = (
        ('admin', 'Admin'),
        ('professor', 'Professor'),
        ('aluno', 'Aluno'),
    )

    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='admin')

    data_nascimento = models.DateField(null=True, blank=True)
    cpf = models.CharField(max_length=14, unique=True, null=True, blank=True)
    rg = models.CharField(max_length=12, unique=True, null=True, blank=True)
    SEXO_CHOICES = [
    ('M', 'Masculino'),
    ('F', 'Feminino'),
]

    COR_PELE_CHOICES = [
    ('branca', 'Branca'),
    ('preta', 'Preta'),
    ('parda', 'Parda'),
    ('amarela', 'Amarela'),
    ('indigena', 'Indígena'),
]

    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, null=True, blank=True)
    cor_pele = models.CharField(max_length=20, choices=COR_PELE_CHOICES, null=True, blank=True)


    senha_temporaria = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.get_full_name()} ({self.tipo})"


class Turma(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome


class Materia(models.Model):
    nome = models.CharField(max_length=100)
    professores = models.ManyToManyField(CustomUser, limit_choices_to={'tipo': 'professor'})
    turmas = models.ManyToManyField(Turma)

    def __str__(self):
        return self.nome

class ProfessorMateriaTurma(models.Model):
    professor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'tipo': 'professor'})
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('professor', 'materia', 'turma')

    def __str__(self):
        return f"{self.professor.get_full_name()} - {self.materia.nome} - {self.turma.nome}"


class AlunoTurma(models.Model):
    aluno = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'tipo': 'aluno'})
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('aluno', 'turma')

    def __str__(self):
        return f"{self.aluno.get_full_name()} - {self.turma.nome}"


class Nota(models.Model):
    aluno = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'tipo': 'aluno'})
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)

    nota_1_semestre1 = models.FloatField(null=True, blank=True)
    nota_2_semestre1 = models.FloatField(null=True, blank=True)
    paralela_1 = models.FloatField(null=True, blank=True)

    nota_1_semestre2 = models.FloatField(null=True, blank=True)
    nota_2_semestre2 = models.FloatField(null=True, blank=True)
    paralela_2 = models.FloatField(null=True, blank=True)

    nota_recuperacao = models.FloatField(null=True, blank=True)

    status_final = models.CharField(max_length=30, blank=True)

    def calcular_status(self):
        n1s1 = self.nota_1_semestre1 or 0
        n2s1 = self.nota_2_semestre1 or 0
        s1 = n1s1 + n2s1
        if self.paralela_1 is not None:
            s1 = max(s1, self.paralela_1)

        if self.nota_1_semestre2 is None or self.nota_2_semestre2 is None:
            return "Pendente"

        n1s2 = self.nota_1_semestre2
        n2s2 = self.nota_2_semestre2
        s2 = n1s2 + n2s2
        if self.paralela_2 is not None:
            s2 = max(s2, self.paralela_2)

        soma = s1 + s2

        if soma >= 120:
            return "Aprovado"

        if self.nota_recuperacao is not None:
            media_curricular = (s1 + s2) / 2
            media_final = (media_curricular * 0.6) + (self.nota_recuperacao * 0.4)
            return "Aprovado" if media_final >= 60 else "Reprovado na Final"

        return "Requer Final"

    def save(self, *args, **kwargs):
        self.status_final = self.calcular_status()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.aluno.get_full_name()} - {self.materia.nome} - {self.status_final}"