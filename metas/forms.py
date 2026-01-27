from django import forms
from .models import Empresa, Analista, ArrecadacaoDiaria, MetaGlobalEmpresa

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nome']
        widgets = {'nome': forms.TextInput(attrs={'class': 'form-control'})}

class AnalistaForm(forms.ModelForm):
    class Meta:
        model = Analista
        fields = ['nome', 'empresa']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'empresa': forms.Select(attrs={'class': 'form-select'}),
        }

class ArrecadacaoForm(forms.ModelForm):
    class Meta:
        model = ArrecadacaoDiaria
        fields = ['analista', 'valor', 'data']
        widgets = {
            'analista': forms.Select(attrs={'class': 'form-select'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }