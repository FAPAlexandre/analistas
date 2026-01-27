from django.shortcuts import render, redirect
from django.db.models import Sum, Q
from datetime import date
from .models import Empresa, Analista, MetaGlobalEmpresa
from .forms import EmpresaForm, AnalistaForm, ArrecadacaoForm

def dashboard_metas(request):
    """View principal do Dashboard"""
    empresas = Empresa.objects.all()
    dados_dashboard = []
    hoje = date.today()

    for empresa in empresas:
        # Busca analistas com a soma de arrecadação do mês atual
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

def cadastro(request):
    """View de cadastro (Antiga painel_cadastro)"""
    # Se o formulário for enviado (POST)
    if request.method == 'POST':
        if 'btn_empresa' in request.POST:
            form = EmpresaForm(request.POST)
            if form.is_valid(): form.save()
            
        elif 'btn_analista' in request.POST:
            form = AnalistaForm(request.POST)
            if form.is_valid(): form.save()
            
        elif 'btn_arrecadacao' in request.POST:
            form = ArrecadacaoForm(request.POST)
            if form.is_valid(): form.save()
            
        # O nome aqui deve ser o 'name' definido no seu urls.py
        return redirect('cadastro') 

    # Se for apenas acesso visual (GET)
    context = {
        'form_empresa': EmpresaForm(),
        'form_analista': AnalistaForm(),
        'form_arrecadacao': ArrecadacaoForm(),
    }
    return render(request, 'cadastro.html', context)