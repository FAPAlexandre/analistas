from django.shortcuts import render, redirect
from django.db.models import Sum, Q
from datetime import date
from django.contrib.auth.decorators import login_required # Para segurança
from django.contrib import messages # Para alertas de sucesso
from .models import Empresa, Analista, MetaGlobalEmpresa
from .forms import EmpresaForm, AnalistaForm, ArrecadacaoForm

def dashboard_metas(request):
    """View pública do Dashboard"""
    empresas = Empresa.objects.all()
    dados_dashboard = []
    hoje = date.today()

    for empresa in empresas:
        todos_analistas = Analista.objects.filter(empresa=empresa).annotate(
            total_mes=Sum(
                'arrecadacoes__valor',
                filter=Q(
                    arrecadacoes__data__month=hoje.month,
                    arrecadacoes__data__year=hoje.year
                )
            )
        ).order_by('-total_mes')

        meta_global = MetaGlobalEmpresa.objects.filter(
            empresa=empresa, 
            mes_referencia=hoje.month, 
            ano_referencia=hoje.year
        ).last()

        dados_dashboard.append({
            'empresa': empresa,
            'analistas': todos_analistas,
            'meta_global': meta_global,
        })

    return render(request, 'metas/dashboard.html', {'dados': dados_dashboard})

@login_required # Só quem estiver logado acessa a página de cadastro
def cadastro(request):
    """View de cadastro protegida"""
    if request.method == 'POST':
        # Dicionário para mapear o botão ao formulário
        form_map = {
            'btn_empresa': EmpresaForm,
            'btn_analista': AnalistaForm,
            'btn_arrecadacao': ArrecadacaoForm
        }
        
        for btn_name, FormClass in form_map.items():
            if btn_name in request.POST:
                form = FormClass(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, f"Cadastro realizado com sucesso!")
                    return redirect('cadastro')
                else:
                    messages.error(request, "Erro ao validar o formulário. Verifique os dados.")

    context = {
        'form_empresa': EmpresaForm(),
        'form_analista': AnalistaForm(),
        'form_arrecadacao': ArrecadacaoForm(),
    }
    return render(request, 'cadastro.html', context)