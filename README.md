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
    Bash

    python manage.py migrate

    Inicie o servidor:
    Bash

    python manage.py runserver

    Acesse no navegador:

        Dashboard: http://127.0.0.1:8000/

        Cadastro: http://127.0.0.1:8000/cadastro/

📈 Lógica de Cálculo de Metas

O sistema utiliza os seguintes cálculos em tempo real:

    Ritmo Diário: (Valor da Meta - Total Arrecadado) / Dias Úteis Restantes.

    Status da Equipe: Definido pela soma total de todos os analistas vinculados à empresa no mês vigente.

🤝 Contato

Desenvolvido por Alexandre - [Seu LinkedIn aqui]
