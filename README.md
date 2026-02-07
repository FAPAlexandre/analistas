🚀 Sistema de Gestão de Arrecadação e Metas

Este aplicativo é uma plataforma de Business Intelligence (BI) e Gestão Operacional voltada para o monitoramento de performance de equipes de arrecadação em tempo real.
📌 Arquitetura do Sistema

O sistema está dividido em três pilares principais para garantir que cada perfil de usuário (Analista, Gerente e Diretor) tenha as informações necessárias sem poluição visual.
1. Dashboard Operacional (/dashboard/)

O "Placar do Jogo". Focado no dia a dia da operação.

    Ranking em Tempo Real: Lista analistas por volume arrecadado no mês.

    Status de Metas (Bronze/Prata/Ouro): Indicadores visuais que mudam de cor conforme o atingimento.

    Cálculo de Ritmo: Informa quanto a equipe precisa arrecadar por dia para bater as próximas metas.

    Atualização Automática: Auto-refresh a cada 60 segundos.

2. Inteligência de Performance (/analise/)

Visão estratégica baseada em tendências temporais.

    Gráfico de Evolução Mensal: Gráfico de barras empilhadas mostrando os dias 1 a 31 do mês.

    Segmentação por Analista: Cada cor no gráfico representa um analista, permitindo ver a contribuição individual no volume total diário.

    Interface Interativa: Gráficos responsivos (Chart.js) com scroll horizontal para visualização detalhada.

3. Relatórios de Fechamento (/relatorios/)

Visão gerencial para tomada de decisão e auditoria.

    Consolidado Mensal: Tabela de fechamento com a produção total de cada analista no mês corrente.

    Acumulado Anual: Monitoramento de longo prazo para identificar os melhores talentos do ano.

    Modo de Impressão: CSS otimizado para geração de PDFs e relatórios físicos em reuniões.

🛠️ Tecnologias Utilizadas

    Backend: Python 3.x / Django (Framework)

    Banco de Dados: SQLite (Desenvolvimento) / PostgreSQL (Recomendado para Produção)

    Frontend: Bootstrap 5 (Styling) / Chart.js (Gráficos)

    Lógica de Negócio:

        Sum e Q objects para agregações complexas.

        ExtractWeekDay e calendar para inteligência temporal.

🗄️ Estrutura de Modelos (Models)

    Empresa: Entidade pai que agrupa analistas e metas.

    Analista: Usuário operacional vinculado a uma empresa.

    MetaGlobalEmpresa: Define os gatilhos (R$) para os níveis Bronze, Prata e Ouro de cada mês.

    ArrecadacaoDiaria: Registro individual de cada entrada financeira (Data, Analista, Valor).

🚀 Como Executar

    Migrar o Banco:
    Bash

    python manage.py migrate

    Criar Superusuário (Admin):
    Bash

    python manage.py createsuperuser

    Rodar o Servidor:
    Bash

    python manage.py runserver

🔒 Segurança e Acessos

    Público: Apenas o Dashboard (opcional, dependendo da configuração da View).

    Restrito (@login_required):

        Cadastro: Registro de novos analistas e lançamentos.

        Análise: Acesso aos gráficos de performance.

        Relatórios: Acesso aos dados consolidados e financeiros.
