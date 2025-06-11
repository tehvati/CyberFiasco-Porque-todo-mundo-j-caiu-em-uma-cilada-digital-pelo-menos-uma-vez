# Cybersecurity Data Analyzer - Manual de Uso #

🔐 Descrição Geral

Projeto em Python com interface gráfica baseada em CustomTkinter, que permite a visualização, cadastro, atualização e análise interativa de dados sobre ataques cibernéticos ao redor do mundo. Ideal para fins educacionais, acadêmicos ou de conscientização sobre segurança da informação.

🚀 Funcionalidades

• Interface de Login com recuperação de senha
• Cadastro de novos usuários com confirmação de senha
• Tela principal com curiosidades sobre segurança cibernética
• Visualização de dados com filtros por país, ano e tipo de ataque
• Geração de gráficos interativos (barras, pizza, linha)
• Cadastro de novos ataques diretamente na base
• Edição e exclusão de registros por meio da interface
• Quiz interativo sobre cibersegurança

🧰 Requisitos

• Python 3.10 ou superior
• customtkinter
• pandas
• plotly
• Pillow

📂 Organização dos Arquivos

cybersecurity-app/
├── data/ (contém o CSV com os ataques)
├── images/ (imagens da interface)
├── src/ (código-fonte)
│   ├── main.py
│   ├── home.py
│   ├── login.py
│   ├── cadastrousuario.py
│   ├── bancousuario.py
│   ├── cadastro.py
│   ├── atualizardeletar.py
│   └── quiz.py
├── icon.ico
└── README.md

🧑‍💻 Como Executar

1. Clone ou baixe o repositório
2. Certifique-se de que o arquivo CSV está em /data
3. Acesse a pasta src
4. Execute: python main.py

🗃️ Banco de Dados

O sistema cria automaticamente o banco 'usuarios.db' (SQLite) ao abrir a tela de login, se ele não existir.

📊 Dados

Utiliza o arquivo CSV com colunas como:
- Year
- Country
- Attack Type
- Target Industry
- Attack Source
- Financial Loss
- Incident Resolution Time
- Number of Affected Users

❓ Dúvidas Frequentes

• Posso cadastrar ataques manualmente? Sim, pelo botão 'Cadastrar Novo Ataque'
• Consigo editar ou apagar registros? Sim, usando 'Atualizar/Deletar Dados'
• E se eu esquecer minha senha? Use 'Esqueci minha senha' na tela de login

🧠 Sobre o Projeto

Este projeto foi desenvolvido como parte de um trabalho acadêmico, com foco em segurança da informação, ciência de dados e interfaces amigáveis ao usuário.
