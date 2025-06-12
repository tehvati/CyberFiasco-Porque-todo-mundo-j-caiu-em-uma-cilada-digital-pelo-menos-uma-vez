import customtkinter as ctk
import subprocess
import sys
from bancousuario import criar_banco, validar_login


#Criando Janela
def abri_janela_login(janela_principal):
    janela = ctk.CTkToplevel()
    janela.title('Login')
    janela.geometry('300x250')
    janela.lift()
    janela.focus_force()
    janela.attributes('-topmost', True)
    janela.after(100, lambda: janela.attributes('-topmost', False))

    #Título da Janela
    titulo = ctk.CTkLabel(janela, text='Entrar', font=ctk.CTkFont(size=22, weight='bold'))
    titulo.pack(pady=10)

    #Campo Usuário
    entrada_usuario = ctk.CTkEntry(janela, placeholder_text='Usuário')
    entrada_usuario.pack(pady=5)

    #Campo Senha
    entrada_senha = ctk.CTkEntry(janela, placeholder_text='Senha', show='*')
    entrada_senha.pack(pady=5)

    #Mensagem de Status
    mensagem_status = ctk.CTkLabel(janela, text='', text_color='red')
    mensagem_status.pack()

    #Função para o botão entrar
    def entrar():
        usuario = entrada_usuario.get()
        senha = entrada_senha.get()

        if validar_login(usuario, senha):
            mensagem_status.configure(text='Login bem-sucedido!', text_color='green')
            janela.destroy()
            janela_principal.destroy()            
            subprocess.Popen([sys.executable, 'home.py'])
            
        else:
            mensagem_status.configure(text='Usuário ou senha inválidos.', text_color='red')

    #Função para recuperar senha
    def recuperar_senha():
        def verificar_usuario():
            usuario = entrada_usuario_rec.get().strip()
            from bancousuario import usuario_existe
            if usuario_existe(usuario):
                entrada_nova_senha.pack(pady=5)
                botao_salvar.pack(pady=5)
                mensagem.configure(text='Usuário encontrado. Digite a nova senha:', text_color='green')
            else:
                mensagem.configure(text='Usuário não encontrado.', text_color='red')

        def salvar_nova_senha():
            usuario = entrada_usuario_rec.get().strip()
            nova_senha = entrada_nova_senha.get().strip()
            from bancousuario import editar_senha
            editar_senha(usuario, nova_senha)
            mensagem.configure(text='Senha atualizada com sucesso!', text_color='green')
            janela_rec.after(2000, janela_rec.destroy)

        janela_rec = ctk.CTkToplevel(janela)
        janela_rec.title('Recuperar Senha')
        janela_rec.geometry('300x250')
        janela_rec.lift()
        janela_rec.focus_force()
        janela_rec.attributes('-topmost', True)

        ctk.CTkLabel(janela_rec, text='Digite o nome de usuário:').pack(pady=10)
        entrada_usuario_rec = ctk.CTkEntry(janela_rec, placeholder_text='Usuário')
        entrada_usuario_rec.pack(pady=5)
        ctk.CTkButton(janela_rec, text='Verificar', command=verificar_usuario).pack(pady=5)

        entrada_nova_senha = ctk.CTkEntry(janela_rec, placeholder_text='Nova Senha', show='*')
        botao_salvar = ctk.CTkButton(janela_rec, text='Salvar', command=salvar_nova_senha)
        mensagem = ctk.CTkLabel(janela_rec, text='')
        mensagem.pack(pady=5)


    botao_entrar = ctk.CTkButton(janela, text='Entrar', command=entrar)
    botao_entrar.pack(pady=10)
    botao_esqueci = ctk.CTkButton(janela, text='Esqueci minha senha', command=recuperar_senha)
    botao_esqueci.pack(pady=10)

    # Inicializa o banco
    criar_banco()