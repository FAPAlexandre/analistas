import pandas as pd
import calendar
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Q
from django.http import HttpResponse
from datetime import date
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from decimal import Decimal

from .models import Empresa, Analista, MetaGlobalEmpresa, ArrecadacaoDiaria
from .forms import EmpresaForm, AnalistaForm, ArrecadacaoForm

# --- AUXILIAR ---
def e_administrador(user):
    return user.is_authenticated and user.is_staff

# --- 1. DASHBOARD PRINCIPAL ---
def dashboard_metas(request):
    empresas = Empresa.objects.all()
    dados_dashboard = []
    hoje = date.today()

    for empresa in empresas:
        analistas_query = Analista.objects.filter(empresa=empresa).annotate(
            total_mes=Sum(
                'arrecadacoes__valor',
                filter=Q(arrecadacoes__data__month=hoje.month, arrecadacoes__data__year=hoje.year)
            )
        ).order_by('-total_mes')

        total_equipe = analistas_query.aggregate(Sum('total_mes'))['total_mes__sum'] or Decimal('0.00')
        meta_global_obj = MetaGlobalEmpresa.objects.filter(
            empresa=empresa, mes_referencia=hoje.month, ano_referencia=hoje.year
        ).last()

        meta_data = {}
        if meta_global_obj:
            dias = meta_global_obj.dias_uteis_restantes if meta_global_obj.dias_uteis_restantes > 0 else 1
            f_bronze = max(Decimal('0.00'), (meta_global_obj.bronze_global or Decimal('0.00')) - total_equipe)
            f_prata = max(Decimal('0.00'), (meta_global_obj.prata_global or Decimal('0.00')) - total_equipe)
            f_ouro = max(Decimal('0.00'), (meta_global_obj.ouro_global or Decimal('0.00')) - total_equipe)

            meta_data = {
                'total_arrecadado_equipe': total_equipe,
                'bronze_global': meta_global_obj.bronze_global,
                'prata_global': meta_global_obj.prata_global,
                'ouro_global': meta_global_obj.ouro_global,
                'falta_bronze_global': f_bronze,
                'falta_prata_global': f_prata,
                'falta_ouro_global': f_ouro,
                'dias_uteis_restantes': meta_global_obj.dias_uteis_restantes,
                'diario_bronze': f_bronze / dias,
                'diario_prata': f_prata / dias,
                'diario_ouro': f_ouro / dias,
            }

        dados_dashboard.append({'empresa': empresa, 'analistas': analistas_query, 'meta_global': meta_data})

    return render(request, 'metas/dashboard.html', {'dados': dados_dashboard})

# --- 2. CADASTRO ---
@login_required
def cadastro(request):
    historico = ArrecadacaoDiaria.objects.all().order_by('-data', '-id')[:20]
    if request.method == 'POST':
        if 'btn_empresa' in request.POST: form = EmpresaForm(request.POST)
        elif 'btn_analista' in request.POST: form = AnalistaForm(request.POST)
        elif 'btn_arrecadacao' in request.POST: form = ArrecadacaoForm(request.POST)
        else: form = None

        if form and form.is_valid():
            form.save()
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect('cadastro')
        messages.error(request, "Erro no formulário.")

    context = {'form_empresa': EmpresaForm(), 'form_analista': AnalistaForm(), 'form_arrecadacao': ArrecadacaoForm(), 'historico': historico}
    return render(request, 'cadastro.html', context)

# --- 3. ANÁLISE DE PERFORMANCE (COM TERMÔMETRO GLOBAL) ---
@login_required
@user_passes_test(e_administrador, login_url='dashboard')
def analise_performance(request):
    """View que gera os dados para os gráficos de evolução diária e termômetro de metas"""
    empresas = Empresa.objects.all()
    dados_analise = []
    hoje = date.today()
    ultimo_dia = calendar.monthrange(hoje.year, hoje.month)[1]
    dias_do_mes = [dia for dia in range(1, ultimo_dia + 1)]

    # 1. Dados Individuais por Empresa (Gráficos)
    for empresa in empresas:
        datasets = []
        analistas = Analista.objects.filter(empresa=empresa)
        for analista in analistas:
            arrecadacoes = ArrecadacaoDiaria.objects.filter(
                analista=analista, data__month=hoje.month, data__year=hoje.year
            ).values('data__day').annotate(total=Sum('valor'))
            
            mapa = {d['data__day']: float(d['total']) for d in arrecadacoes}
            valores = [mapa.get(dia, 0) for dia in dias_do_mes]
            datasets.append({'label': analista.nome, 'data': valores})

        dados_analise.append({'empresa': empresa, 'labels': dias_do_mes, 'datasets': datasets})
    
    # 2. Cálculo do Termômetro Global (Soma de Todas as Empresas)
    total_arrecadado_geral = ArrecadacaoDiaria.objects.filter(
        data__month=hoje.month, data__year=hoje.year
    ).aggregate(Sum('valor'))['valor__sum'] or Decimal('0.00')

    meta_ouro_geral = MetaGlobalEmpresa.objects.filter(
        mes_referencia=hoje.month, ano_referencia=hoje.year
    ).aggregate(Sum('ouro_global'))['ouro_global__sum'] or Decimal('0.00')

    percentual_ouro = 0
    if meta_ouro_geral > 0:
        percentual_ouro = min(int((total_arrecadado_geral / meta_ouro_geral) * 100), 100)

    context = {
        'dados': dados_analise,
        'total_geral': total_arrecadado_geral,
        'meta_ouro_geral': meta_ouro_geral,
        'percentual_ouro': percentual_ouro,
    }
    
    return render(request, 'metas/analise.html', context)

# --- 4. RELATÓRIOS E EXCLUSÃO ---
@login_required
def excluir_arrecadacao(request, id):
    arrecadacao = get_object_or_404(ArrecadacaoDiaria, id=id)
    arrecadacao.delete()
    messages.success(request, "Lançamento excluído!")
    return redirect('cadastro')

@login_required
@user_passes_test(e_administrador, login_url='dashboard')
def relatorio_geral(request):
    hoje = date.today()
    mes_filtro = int(request.GET.get('mes', hoje.month))
    ano_filtro = int(request.GET.get('ano', hoje.year))
    
    empresas = Empresa.objects.all()
    relatorios = []
    for empresa in empresas:
        ranking = Analista.objects.filter(empresa=empresa).annotate(
            total=Sum('arrecadacoes__valor', filter=Q(arrecadacoes__data__month=mes_filtro, arrecadacoes__data__year=ano_filtro))
        ).order_by('-total')
        relatorios.append({'empresa': empresa, 'ranking_mensal': ranking})

    context = {
        'dados': relatorios, 
        'meses_lista': [(i, calendar.month_name[i].capitalize()) for i in range(1, 13)],
        'anos_disponiveis': range(hoje.year - 2, hoje.year + 1),
        'mes_selecionado': mes_filtro,
        'ano_selecionado': ano_filtro,
    }
    return render(request, 'metas/relatorios.html', context)

@login_required
@user_passes_test(e_administrador, login_url='dashboard')
def exportar_relatorio_excel(request):
    hoje = date.today()
    mes = int(request.GET.get('mes', hoje.month))
    ano = int(request.GET.get('ano', hoje.year))
    
    arrecadacoes = ArrecadacaoDiaria.objects.filter(data__month=mes, data__year=ano)
    
    if not arrecadacoes.exists():
        messages.warning(request, "Não há dados para exportar neste período.")
        return redirect('relatorio_geral')

    dados = [{
        'Empresa': a.analista.empresa.nome, 
        'Analista': a.analista.nome, 
        'Data': a.data.strftime('%d/%m/%Y'),
        'Valor': float(a.valor)
    } for a in arrecadacoes]
    
    df = pd.DataFrame(dados)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=relatorio_{mes}_{ano}.xlsx'
    
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    return response