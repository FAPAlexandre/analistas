from django.contrib import admin
from .models import Empresa, NivelMeta, Analista, ArrecadacaoDiaria, MetaGlobalEmpresa

# --- INLINES ---
class ArrecadacaoInline(admin.TabularInline):
    model = ArrecadacaoDiaria
    extra = 1
    fields = ('valor', 'data')

# --- ADMINS ---

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(NivelMeta)
class NivelMetaAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'nome_periodo', 'valor_bronze', 'valor_prata', 'valor_ouro')
    list_filter = ('empresa', 'nome_periodo')

@admin.register(Analista)
class AnalistaAdmin(admin.ModelAdmin):
    # ATUALIZADO: Mostra quanto falta para cada nível no Admin
    list_display = (
        'nome', 
        'get_empresa', 
        'get_total', 
        'get_falta_bronze', 
        'get_falta_prata', 
        'get_falta_ouro'
    )
    list_filter = ('empresa',)
    inlines = [ArrecadacaoInline]
    search_fields = ('nome',)

    def get_empresa(self, obj):
        return obj.empresa.nome
    get_empresa.short_description = 'Empresa'

    def get_total(self, obj):
        return f"R$ {obj.total_arrecadado:,.2f}"
    get_total.short_description = 'Total Mês'

    # Funções para exibir "Quanto Falta" na lista do Admin
    def get_falta_bronze(self, obj):
        valor = obj.falta_bronze
        return "✅ OK" if valor <= 0 else f"R$ {valor:,.2f}"
    get_falta_bronze.short_description = 'Falta Bronze'

    def get_falta_prata(self, obj):
        valor = obj.falta_prata
        return "✅ OK" if valor <= 0 else f"R$ {valor:,.2f}"
    get_falta_prata.short_description = 'Falta Prata'

    def get_falta_ouro(self, obj):
        valor = obj.falta_ouro
        return "🏆 META OURO!" if valor <= 0 else f"R$ {valor:,.2f}"
    get_falta_ouro.short_description = 'Falta Ouro'

@admin.register(ArrecadacaoDiaria)
class ArrecadacaoAdmin(admin.ModelAdmin):
    list_display = ('analista', 'get_empresa', 'valor', 'data')
    list_filter = ('data', 'analista__empresa', 'analista')
    date_hierarchy = 'data'
    
    def get_empresa(self, obj):
        return obj.analista.empresa.nome
    get_empresa.short_description = 'Empresa'

@admin.register(MetaGlobalEmpresa)
class MetaGlobalEmpresaAdmin(admin.ModelAdmin):
    list_display = (
        'empresa', 
        'mes_referencia', 
        'get_arrecadado', 
        'dias_uteis_restantes',
        'get_ritmo_bronze',
        'get_ritmo_prata',  
        'get_ritmo_ouro'
    )
    list_filter = ('empresa', 'mes_referencia')

    def get_arrecadado(self, obj):
        return f"R$ {obj.total_arrecadado_equipe:,.2f}"
    get_arrecadado.short_description = "Total Equipe"

    def get_ritmo_bronze(self, obj):
        return f"R$ {obj.ritmo_diario_bronze:,.2f}"
    get_ritmo_bronze.short_description = "Ritmo Bronze"

    def get_ritmo_prata(self, obj):
        return f"R$ {obj.ritmo_diario_prata:,.2f}"
    get_ritmo_prata.short_description = "Ritmo Prata"

    def get_ritmo_ouro(self, obj):
        return f"R$ {obj.ritmo_diario_ouro:,.2f}"
    get_ritmo_ouro.short_description = "Ritmo Ouro"