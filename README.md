# 📈 Sistema de Gestão de Metas e BI (Analistas)

Sistema desenvolvido em **Django** para monitoramento de performance de arrecadação em tempo real. A ferramenta consolida dados de múltiplos analistas e empresas, oferecendo uma visão tática (operacional) e estratégica (BI).

## 🚀 Funcionalidades Principais

- **Dashboard Executivo:** Visualização rápida do total arrecadado por analista e empresa no mês vigente.
- **Inteligência Mensal (BI):** Gráficos de evolução diária (Stacked Bar Charts) utilizando **Chart.js**.
- **Termômetro de Meta Global:** Barra de progresso dinâmica que calcula o atingimento da Meta Ouro em todo o grupo empresarial.
- **Gestão de Arrecadação:** Interface estilo "Planilha Web" para lançamentos rápidos, edição e exclusão de registros.
- **Relatórios & Exportação:** - Filtros por mês e ano.
    - Exportação de dados para **Excel (.xlsx)** com Pandas.
    - Geração de **Relatórios em PDF** otimizados para impressão.

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3.12 / Django 5.x
* **Frontend:** Bootstrap 5 (UI), Chart.js (Gráficos)
* **Dados:** SQLite (Desenvolvimento), Pandas (Processamento de Excel)
* **Segurança:** Decorators de autenticação e restrição para administradores (Staff).

## 📋 Pré-requisitos

Antes de começar, você vai precisar ter instalado em sua máquina:
[Python](https://www.python.org/), [Git](https://git-scm.com/).

## 🔧 Instalação e Execução

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/FAPAlexandre/analistas.git](https://github.com/FAPAlexandre/analistas.git)
   cd analistas

    Crie e ative o ambiente virtual:
    Bash

    python -m venv venv
    # No Linux/macOS:
    source venv/bin/activate
    # No Windows:
    venv\Scripts\activate

    Instale as dependências:
    Bash

    pip install -r requirements.txt

    Execute as migrações do banco de dados:
    Bash

    python manage.py migrate

    Inicie o servidor:
    Bash

    python manage.py runserver

    Acesse: http://127.0.0.1:8000/

📁 Estrutura de Rotas (URLs)

    /dashboard/ - Painel principal de metas.

    /cadastro/ - Lançamentos diários e gestão de analistas.

    /analise/ - Gráficos de performance (BI).

    /relatorios/ - Filtros históricos e exportação.