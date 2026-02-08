from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from metas import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Redireciona a raiz (/) para o dashboard
    path('', lambda request: redirect('dashboard', permanent=False)),

    # --- VISÃO OPERACIONAL ---
    path('dashboard/', views.dashboard_metas, name='dashboard'),
    path('cadastro/', views.cadastro, name="cadastro"),
    
    # --- INTELIGÊNCIA E ESTRATÉGIA ---
    path('analise/', views.analise_performance, name='analise_performance'),
    path('relatorios/', views.relatorio_geral, name='relatorio_geral'),
    path('relatorios/exportar/', views.exportar_relatorio_excel, name='exportar_excel'),

    # --- FUNÇÕES AUXILIARES ---
    path('excluir-arrecadacao/<int:id>/', views.excluir_arrecadacao, name='excluir_arrecadacao'),
]