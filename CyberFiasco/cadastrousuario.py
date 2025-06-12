import customtkinter as ctk
from bancousuario import cadastrar_usuario

# Criando Janela de Cadastro
def abri_janela_cadastro():
    janela_cadastro = ctk.CTkToplevel()
    janela_cadastro.title('Cadastro')
    janela_cadastro.geometry('300x250')
    janela_cadastro.lift()
    janela_cadastro.focus_force()
    janela_cadastro.attributes('-topmost', True)

    titulo = ctk.CTkLabel(janela_cadastro, text='Cadastrar-se', font=ctk.CTkFont(size=22, weight='bold'))
    titulo.pack(pady=10)

    entrada_novo_usuario = ctk.CTkEntry(janela_cadastro, placeholder_text='Nome de Usuário')
    entrada_novo_usuario.pack(pady=5)

    entrada_nova_senha = ctk.CTkEntry(janela_cadastro, placeholder_text='Senha', show='*')
    entrada_nova_senha.pack(pady=5)

    entrada_confirmar_senha = ctk.CTkEntry(janela_cadastro, placeholder_text='Confirmar Senha', show='*')
    entrada_confirmar_senha.pack(pady=5)

    mensagem_status_cadastro = ctk.CTkLabel(janela_cadastro, text='', text_color='red')
    mensagem_status_cadastro.pack()

    # Função cadastrar usuário
    def cadastrar():
        nome = entrada_novo_usuario.get().strip()
        senha = entrada_nova_senha.get().strip()
        confirmar = entrada_confirmar_senha.get().strip()

        if senha == confirmar:
            cadastrar_usuario(nome, senha)
            mensagem_status_cadastro.configure(text='Usuário cadastrado com sucesso!', text_color='green')
            janela_cadastro.after(3000, janela_cadastro.destroy) # Fecha após 3 segundos            
        else:
            mensagem_status_cadastro.configure(text='Senha incorreta', text_color='red')

    botao_cadastrar = ctk.CTkButton(janela_cadastro, text='Cadastrar', command=cadastrar)
    botao_cadastrar.pack(pady=10)
