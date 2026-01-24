from django.contrib import admin
from .models import Empresa, NivelMeta, Analista, ArrecadacaoDiaria, MetaGlobalEmpresa


# 1. Inline para lançar arrecadação direto no Analista
class ArrecadacaoInline(admin.TabularInline):
    model = ArrecadacaoDiaria
    extra = 1
    fields = ('valor', 'data')

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(NivelMeta)
class NivelMetaAdmin(admin.ModelAdmin):
    # Exibe a empresa e os valores das metas na listagem
    list_display = ('empresa', 'nome_periodo', 'valor_bronze', 'valor_prata', 'valor_ouro')
    list_filter = ('empresa', 'nome_periodo')
    search_fields = ('empresa__nome', 'nome_periodo')

@admin.register(Analista)
class AnalistaAdmin(admin.ModelAdmin):
    list_display = ('posicao_no_ranking_interno', 'nome', 'get_empresa', 'get_total', 'get_falta_bronze', 'get_falta_prata', 'get_falta_ouro')
    list_filter = ('empresa',)
    inlines = [ArrecadacaoInline]

    def posicao_no_ranking_interno(self, obj):
        # Busca o ranking exclusivo da empresa deste analista
        top_5_da_empresa = list(Analista.get_ranking_por_empresa(obj.empresa))
        
        if obj in top_5_da_empresa:
            posicao = top_5_da_empresa.index(obj) + 1
            medalhas = {1: "🥇", 2: "🥈", 3: "🥉"}
            return f"{medalhas.get(posicao, '')} {posicao}º na {obj.empresa.nome}"
        return "-"
    posicao_no_ranking_interno.short_description = 'Posição na Empresa'

    # ... (outros métodos get_total, get_falta_bronze, etc)
    
    

    # --- Métodos para exibir os campos calculados no Admin ---
    
    def get_empresa(self, obj):
        return obj.empresa.nome
    get_empresa.short_description = 'Empresa'
    get_empresa.admin_order_field = 'empresa' # Permite ordenar pela coluna empresa

    def get_total(self, obj):
        return f"R$ {obj.total_arrecadado:,.2f}"
    get_total.short_description = 'Total Mês'

    def get_falta_bronze(self, obj):
        return f"R$ {obj.falta_bronze:,.2f}"
    get_falta_bronze.short_description = 'Falta p/ Bronze'

    def get_falta_prata(self, obj):
        return f"R$ {obj.falta_prata:,.2f}"
    get_falta_prata.short_description = 'Falta p/ Prata'

    def get_falta_ouro(self, obj):
        return f"R$ {obj.falta_ouro:,.2f}"
    get_falta_ouro.short_description = 'Falta p/ Ouro'

@admin.register(ArrecadacaoDiaria)
class ArrecadacaoAdmin(admin.ModelAdmin):
    list_display = ('analista', 'get_empresa', 'valor', 'data')
    list_filter = ('data', 'analista__empresa', 'analista')
    date_hierarchy = 'data'
    
    def get_empresa(self, obj):
        return obj.analista.empresa.nome
    get_empresa.short_description = 'Empresa'
    
    
@admin.register(MetaGlobalEmpresa)  # Aqui vai o MODEL
class MetaGlobalEmpresaAdmin(admin.ModelAdmin):  # Aqui vai a classe ADMIN
    list_display = (
        'empresa', 
        'mes_referencia', 
        'get_arrecadado', 
        'dias_uteis_restantes',
        'get_falta_bronze',
        'get_falta_prata',  
        'get_falta_ouro',   
        'get_ritmo_bronze',
        'get_ritmo_prata',  
        'get_ritmo_ouro'
    )
    list_filter = ('empresa', 'mes_referencia')

    def get_arrecadado(self, obj):
        return f"R$ {obj.total_arrecadado_equipe:,.2f}"
    get_arrecadado.short_description = "Total Equipe"

    def get_falta_bronze(self, obj):
        return f"R$ {obj.falta_para_bronze:,.2f}"
    get_falta_bronze.short_description = "Falta p/ Bronze"

    def get_falta_prata(self, obj):
        return f"R$ {obj.falta_para_prata:,.2f}"
    get_falta_prata.short_description = "Falta p/ Prata"

    def get_falta_ouro(self, obj):
        return f"R$ {obj.falta_para_ouro:,.2f}"
    get_falta_ouro.short_description = "Falta p/ Ouro"

    def get_ritmo_bronze(self, obj):
        return f"R$ {obj.ritmo_diario_bronze:,.2f}"
    get_ritmo_bronze.short_description = "Ritmo Diário Bronze"

    def get_ritmo_prata(self, obj):
        return f"R$ {obj.ritmo_diario_prata:,.2f}"
    get_ritmo_prata.short_description = "Ritmo Diário Prata"

    def get_ritmo_ouro(self, obj):
        return f"R$ {obj.ritmo_diario_ouro:,.2f}"
    get_ritmo_ouro.short_description = "Ritmo Diário Ouro"