# psw-sgde/autenticacao/forms.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model, authenticate
from django.forms import modelformset_factory, BaseModelFormSet
from core.models import Materia, Turma, ProfessorMateriaTurma, AlunoTurma

CustomUser = get_user_model()


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.TextInput(attrs={'autofocus': True, 'name': 'email'})
    )

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(self.request, username=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
        return self.cleaned_data


class ProfessorCreateForm(forms.ModelForm):
    cor_pele_choices = [
        ('branca', 'Branca'),
        ('preta', 'Preta'),
        ('parda', 'Parda'),
        ('amarela', 'Amarela'),
        ('indigena', 'Indígena'),
    ]

    sexo_choices = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    ]

    cor_pele = forms.ChoiceField(choices=cor_pele_choices, label='Cor da Pele')
    sexo = forms.ChoiceField(choices=sexo_choices, label='Sexo')

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name',
            'data_nascimento', 'cor_pele',
            'cpf', 'rg', 'sexo',
        ]

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        return ''.join(filter(str.isdigit, cpf))

    def clean_rg(self):
        rg = self.cleaned_data['rg']
        return ''.join(filter(str.isdigit, rg))

    def save(self, commit=True):
        professor = super().save(commit=commit)
        return professor

class ProfessorMateriaTurmaForm(forms.ModelForm):
    class Meta:
        model = ProfessorMateriaTurma
        fields = ['materia', 'turma']
        widgets = {
            'materia': forms.Select(attrs={'class': 'form-select'}),
            'turma': forms.Select(attrs={'class': 'form-select'}),
        }

class RequiredIdFormSet(BaseModelFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)
        if 'id' in form.fields:
            form.fields['id'].required = False

ProfessorMateriaTurmaFormSet = modelformset_factory(
    ProfessorMateriaTurma,
    form=ProfessorMateriaTurmaForm,
    extra=3,
    can_delete=False,
    formset=RequiredIdFormSet 
)

class AlunoCreateForm(forms.ModelForm):
    cor_pele_choices = [
        ('branca', 'Branca'),
        ('preta', 'Preta'),
        ('parda', 'Parda'),
        ('amarela', 'Amarela'),
        ('indigena', 'Indígena'),
    ]

    sexo_choices = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    ]

    cor_pele = forms.ChoiceField(choices=cor_pele_choices, label='Cor da Pele')
    sexo = forms.ChoiceField(choices=sexo_choices, label='Sexo')
    turmas = forms.ModelChoiceField(
        queryset=Turma.objects.all(),
        widget=forms.RadioSelect,
        label='Turma'
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.data_nascimento:
            self.initial['data_nascimento'] = self.instance.data_nascimento.strftime('%d/%m/%Y')


    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name',
            'data_nascimento', 'cor_pele',
            'cpf', 'rg', 'sexo',
        ]

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        return ''.join(filter(str.isdigit, cpf))

    def clean_rg(self):
        rg = self.cleaned_data['rg']
        return ''.join(filter(str.isdigit, rg))

    def save(self, commit=True):
        aluno = super().save(commit=False)
        aluno.tipo = 'aluno'
        aluno.username = aluno.cpf
        aluno.email = f"{aluno.cpf}@discente.com"
        aluno.set_password("Senha123#")
        aluno.senha_temporaria = True

        if commit:
            aluno.save()
            AlunoTurma.objects.filter(aluno=aluno).delete()
            AlunoTurma.objects.create(aluno=aluno, turma=self.cleaned_data['turmas'])

        return aluno