from django.shortcuts import render
from .models import Empresa, Analista, MetaGlobalEmpresa
from django.db.models import Sum, Q
from datetime import date

def dashboard_metas(request):
    empresas = Empresa.objects.all()
    dados_dashboard = []
    hoje = date.today()

    for empresa in empresas:
        # Buscamos TODOS os analistas da empresa
        # Usamos Left Join (annotate) para trazer quem tem zero também
        todos_analistas = Analista.objects.filter(empresa=empresa).annotate(
            total_mes=Sum(
                'arrecadacoes__valor',
                filter=Q(
                    arrecadacoes__data__month=hoje.month,
                    arrecadacoes__data__year=hoje.year
                )
            )
        ).order_by('-total_mes') # Ordena do maior para o menor

        meta_global = MetaGlobalEmpresa.objects.filter(empresa=empresa).last()

        dados_dashboard.append({
            'empresa': empresa,
            'analistas': todos_analistas, # Agora passamos a lista completa
            'meta_global': meta_global,
        })

    return render(request, 'metas/dashboard.html', {'dados': dados_dashboard})