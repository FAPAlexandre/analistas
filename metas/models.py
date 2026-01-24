from django.db import models
from django.db.models import Sum
from datetime import date, timedelta
from decimal import Decimal

class Empresa(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

class NivelMeta(models.Model):
    """Define as metas Bronze, Prata e Ouro para uma Empresa específica"""
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='metas', null=True)
    nome_periodo = models.CharField(max_length=50, help_text="Ex: Janeiro 2026", null=True)
    valor_bronze = models.DecimalField(max_digits=12, decimal_places=2)
    valor_prata = models.DecimalField(max_digits=12, decimal_places=2)
    valor_ouro = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = "Nível de Meta"
        verbose_name_plural = "Níveis de Metas"

    def __str__(self):
        return f"Meta {self.empresa.nome} - {self.nome_periodo}"

class Analista(models.Model):
    
    @classmethod
    def get_ranking_por_empresa(cls, empresa_obj):
        hoje = date.today()
        # Filtramos apenas os analistas da empresa fornecida
        return cls.objects.filter(empresa=empresa_obj).annotate(
            total_mes=models.Sum(
                'arrecadacoes__valor',
                filter=models.Q(
                    arrecadacoes__data__month=hoje.month,
                    arrecadacoes__data__year=hoje.year
                )
            )
        ).order_by('-total_mes')[:5]
    
    nome = models.CharField(max_length=100)
    # Atrela o analista a uma empresa
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, related_name='analistas', null=True)

    def __str__(self):
        return f"{self.nome} ({self.empresa.nome})"

    @property
    def meta_atual(self):
        """Busca a meta mais recente da empresa deste analista"""
        return self.empresa.metas.last()

    @property
    def total_arrecadado(self):
        hoje = date.today()
        return self.arrecadacoes.filter(
            data__month=hoje.month, 
            data__year=hoje.year
        ).aggregate(Sum('valor'))['valor__sum'] or Decimal(0)

    # Cálculos inteligentes: Agora eles buscam os valores da meta da EMPRESA do analista
    @property
    def falta_bronze(self):
        meta = self.meta_atual
        if not meta: return Decimal(0)
        return max(Decimal(0), meta.valor_bronze - self.total_arrecadado)

    @property
    def falta_prata(self):
        meta = self.meta_atual
        if not meta: return Decimal(0)
        return max(Decimal(0), meta.valor_prata - self.total_arrecadado)

    @property
    def falta_ouro(self):
        meta = self.meta_atual
        if not meta: return Decimal(0)
        return max(Decimal(0), meta.valor_ouro - self.total_arrecadado)

class ArrecadacaoDiaria(models.Model):
    analista = models.ForeignKey(Analista, on_delete=models.CASCADE, related_name='arrecadacoes')
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    data = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.analista.nome} - {self.data}"
    
    
    
    #O MODELS PARA ADICIONAR OS VALORES DAS EMPRESAS
    
class MetaGlobalEmpresa(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='metas_globais')
    mes_referencia = models.IntegerField(default=date.today().month)
    ano_referencia = models.IntegerField(default=date.today().year)
    
    bronze_global = models.DecimalField(max_digits=15, decimal_places=2)
    prata_global = models.DecimalField(max_digits=15, decimal_places=2)
    ouro_global = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        verbose_name = "Meta Global da Empresa"
        verbose_name_plural = "Metas Globais das Empresas"

    def __str__(self):
        return f"Meta Global {self.empresa.nome} - {self.mes_referencia}/{self.ano_referencia}"

    @property
    def total_arrecadado_equipe(self):
        return ArrecadacaoDiaria.objects.filter(
            analista__empresa=self.empresa,
            data__month=self.mes_referencia,
            data__year=self.ano_referencia
        ).aggregate(Sum('valor'))['valor__sum'] or Decimal(0)

    @property
    def dias_uteis_restantes(self):
        hoje = date.today()
        if self.mes_referencia == 12:
            ultimo_dia = date(self.ano_referencia, 12, 31)
        else:
            ultimo_dia = date(self.ano_referencia, self.mes_referencia + 1, 1) - timedelta(days=1)
        
        inicio_contagem = max(hoje, date(self.ano_referencia, self.mes_referencia, 1))
        dias_uteis = 0
        temp_data = inicio_contagem
        while temp_data <= ultimo_dia:
            if temp_data.weekday() < 5: 
                dias_uteis += 1
            temp_data += timedelta(days=1)
        return dias_uteis

    def calcular_ritmo_diario(self, valor_meta):
        dias = self.dias_uteis_restantes
        if dias <= 0: return Decimal(0)
        falta = valor_meta - self.total_arrecadado_equipe
        return max(Decimal(0), falta / dias)

    # No seu models.py, dentro de MetaGlobalEmpresa:
# Dentro da classe MetaGlobalEmpresa no models.py

    @property
    def falta_para_bronze(self): 
        return max(Decimal(0), self.bronze_global - self.total_arrecadado_equipe)

    @property
    def falta_para_prata(self):
        return max(Decimal(0), self.prata_global - self.total_arrecadado_equipe)

    @property
    def falta_para_ouro(self):
        return max(Decimal(0), self.ouro_global - self.total_arrecadado_equipe)

    @property
    def ritmo_diario_bronze(self): 
        return self.calcular_ritmo_diario(self.bronze_global)

    @property
    def ritmo_diario_prata(self):
        return self.calcular_ritmo_diario(self.prata_global)

    @property
    def ritmo_diario_ouro(self): 
        return self.calcular_ritmo_diario(self.ouro_global)