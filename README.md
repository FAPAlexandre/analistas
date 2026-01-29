<<<<<<< HEAD
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
=======
Essa é uma excelente ideia. Um repositório com uma boa documentação (README) é o que diferencia um "amontoado de arquivos" de um projeto profissional.

Aqui está um modelo completo de README.md que escrevi especificamente para a estrutura que construímos (Django + Metas + Bootstrap). Basta copiar e salvar como README.md na pasta raiz do seu projeto e dar git push.
🚀 Sistema de Gestão de Metas e Performance

Um dashboard dinâmico desenvolvido em Django para monitoramento em tempo real da performance de arrecadação de analistas e empresas. O sistema calcula automaticamente o ritmo necessário para atingir metas globais (Bronze, Prata e Ouro) com base nos dias úteis restantes.
✨ Funcionalidades

    Dashboard de Performance: Visualização clara do total arrecadado pela equipe e individualmente.

    Cálculo Automático de Ritmo: O sistema indica quanto a equipe precisa arrecadar por dia para atingir cada nível de meta.

    Gamificação por Metais: Cores dinâmicas (Bronze, Prata, Ouro) que mudam conforme a meta é batida.

    Gestão Dinâmica: Painel de cadastro para Empresas, Analistas e Arrecadações.

    Inteligência de Datas: Cálculo automático de dias úteis restantes no mês atual.

🛠️ Tecnologias Utilizadas

    Backend: Python 3.x & Django Framework.

    Frontend: HTML5, CSS3, Bootstrap 5.

    Banco de Dados: SQLite (padrão de desenvolvimento).

    Localização: Padrão monetário brasileiro (pt-br).

📂 Estrutura do Projeto
Plaintext

analistas/
├── core/                # Configurações principais do Django
├── metas/               # App principal do sistema
│   ├── forms.py         # Formulários de entrada de dados
│   ├── models.py        # Modelagem de dados (Empresa, Analista, Arrecadação)
│   ├── views.py         # Lógica de negócio e cálculos de metas
│   └── templates/       # Arquivos HTML (Dashboard e Cadastro)
└── manage.py            # Utilitário de execução do Django

🚀 Como Executar o Projeto

    Clone o repositório:
    Bash

    git clone https://github.com/FAPAlexandre/analistas.git
    cd analistas

    Crie e ative um ambiente virtual (Opcional, mas recomendado):
    Bash

    python -m venv venv
    source venv/bin/activate  # No Linux
    # venv\Scripts\activate   # No Windows

    Instale o Django:
    Bash

    pip install django

    Execute as migrações do banco de dados:
>>>>>>> 397be7e (feat: proteção de acesso, sistema de mensagens e documentação README)
    Bash

    python manage.py migrate

<<<<<<< HEAD
    Criar Superusuário (Admin):
    Bash

    python manage.py createsuperuser

    Rodar o Servidor:
=======
    Inicie o servidor:
>>>>>>> 397be7e (feat: proteção de acesso, sistema de mensagens e documentação README)
    Bash

    python manage.py runserver

<<<<<<< HEAD
🔒 Segurança e Acessos

    Público: Apenas o Dashboard (opcional, dependendo da configuração da View).

    Restrito (@login_required):

        Cadastro: Registro de novos analistas e lançamentos.

        Análise: Acesso aos gráficos de performance.

        Relatórios: Acesso aos dados consolidados e financeiros.
=======
    Acesse no navegador:

        Dashboard: http://127.0.0.1:8000/

        Cadastro: http://127.0.0.1:8000/cadastro/

📈 Lógica de Cálculo de Metas

O sistema utiliza os seguintes cálculos em tempo real:

    Ritmo Diário: (Valor da Meta - Total Arrecadado) / Dias Úteis Restantes.

    Status da Equipe: Definido pela soma total de todos os analistas vinculados à empresa no mês vigente.

🤝 Contato

Desenvolvido por Alexandre - [Seu LinkedIn aqui]
>>>>>>> 397be7e (feat: proteção de acesso, sistema de mensagens e documentação README)
