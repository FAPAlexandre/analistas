from django.db import models
from django.db.models import Sum, Q
from datetime import date, timedelta
from decimal import Decimal

class Empresa(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

class NivelMeta(models.Model):
    """Metas da Empresa que servem de base para os Analistas"""
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='metas', null=True)
    nome_periodo = models.CharField(max_length=50, help_text="Ex: Janeiro 2026", null=True)
    valor_bronze = models.DecimalField(max_digits=12, decimal_places=2)
    valor_prata = models.DecimalField(max_digits=12, decimal_places=2)
    valor_ouro = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = "Nível de Meta Sugerida"
        verbose_name_plural = "Níveis de Metas Sugeridas"

    def __str__(self):
        return f"Meta {self.empresa.nome} - {self.nome_periodo}"

class Analista(models.Model):
    nome = models.CharField(max_length=100)
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, related_name='analistas', null=True)
    # Mantivemos a individual caso queira usar como 'Ouro Personalizado', 
    # mas a lógica abaixo focará nos Níveis da Empresa.
    meta_individual = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return f"{self.nome} ({self.empresa.nome})"

    @property
    def total_arrecadado(self):
        """Soma total do analista no mês atual"""
        hoje = date.today()
        resultado = self.arrecadacoes.filter(
            data__month=hoje.month, 
            data__year=hoje.year
        ).aggregate(total=Sum('valor'))['total']
        return resultado or Decimal('0.00')

    # --- Lógica de "Quanto Falta" baseada nos Níveis da Empresa ---

    def calcular_falta(self, nivel):
        """Função genérica para calcular a diferença até o nível desejado"""
        # Busca a meta da empresa para o mês atual (ou a última cadastrada)
        meta_empresa = NivelMeta.objects.filter(empresa=self.empresa).last()
        
        if not meta_empresa:
            return Decimal('0.00')

        valor_meta = getattr(meta_empresa, f'valor_{nivel}', Decimal('0.00'))
        diferenca = valor_meta - self.total_arrecadado
        return max(Decimal('0.00'), diferenca)

    @property
    def falta_bronze(self):
        return self.calcular_falta('bronze')

    @property
    def falta_prata(self):
        return self.calcular_falta('prata')

    @property
    def falta_ouro(self):
        return self.calcular_falta('ouro')

    @classmethod
    def get_ranking_por_empresa(cls, empresa_obj):
        hoje = date.today()
        return cls.objects.filter(empresa=empresa_obj).annotate(
            total_mes=Sum(
                'arrecadacoes__valor',
                filter=Q(arrecadacoes__data__month=hoje.month, arrecadacoes__data__year=hoje.year)
            )
        ).order_by('-total_mes')

class ArrecadacaoDiaria(models.Model):
    analista = models.ForeignKey(Analista, on_delete=models.CASCADE, related_name='arrecadacoes')
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    data = models.DateField(default=date.today)

    class Meta:
        verbose_name = "Arrecadação Diária"
        verbose_name_plural = "Arrecadações Diárias"

    def __str__(self):
        return f"{self.analista.nome} - R$ {self.valor} ({self.data})"

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
        resultado = ArrecadacaoDiaria.objects.filter(
            analista__empresa=self.empresa,
            data__month=self.mes_referencia,
            data__year=self.ano_referencia
        ).aggregate(total=Sum('valor'))['total']
        return resultado or Decimal('0.00')

    @property
    def dias_uteis_restantes(self):
        hoje = date.today()
        if self.mes_referencia == 12:
            ultimo_dia = date(self.ano_referencia, 12, 31)
        else:
            proximo_mes = self.mes_referencia + 1
            ultimo_dia = date(self.ano_referencia, proximo_mes, 1) - timedelta(days=1)
        
        if hoje.month != self.mes_referencia or hoje.year != self.ano_referencia:
            return 0 if hoje > ultimo_dia else 20 # Valor genérico se for mês futuro

        dias_uteis = 0
        temp_data = hoje
        while temp_data <= ultimo_dia:
            if temp_data.weekday() < 5: 
                dias_uteis += 1
            temp_data += timedelta(days=1)
        return dias_uteis

    def calcular_ritmo(self, valor_meta):
        dias = self.dias_uteis_restantes
        if dias <= 0: return Decimal('0.00')
        falta = valor_meta - self.total_arrecadado_equipe
        return max(Decimal('0.00'), falta / Decimal(dias))

    @property
    def ritmo_diario_bronze(self): return self.calcular_ritmo(self.bronze_global)
    @property
    def ritmo_diario_prata(self): return self.calcular_ritmo(self.prata_global)
    @property
    def ritmo_diario_ouro(self): return self.calcular_ritmo(self.ouro_global)