import customtkinter as ctk
from PIL import Image
from login import abri_janela_login
from cadastrousuario import abri_janela_cadastro

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AplicativoSegurancaCibernetica(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Segurança Cibernética: Análise de dados e dicas de proteção")
        self.geometry("1100x700")
        self.resizable(False, False)
        self.iconbitmap('icon.ico')

        # Título
        self.rotulo_titulo = ctk.CTkLabel(
            self,
            text="🔒 Segurança Cibernética:\nAnálise de dados e dicas de proteção",
            font=ctk.CTkFont(size=26, weight="bold"),
            justify="center"
        )
        self.rotulo_titulo.pack(pady=(20, 10))

        self.rotulo_descricao = ctk.CTkLabel(
            self,
            text="Ferramenta de análise e proteção contra ameaças cibernéticas.",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        self.rotulo_descricao.pack(pady=(0, 20))

        # Frame principal horizontal
        frame_principal = ctk.CTkFrame(self)
        frame_principal.pack(pady=10, padx=20, fill="both", expand=True)

        # Frame da imagem (esquerda)
        frame_imagem = ctk.CTkFrame(frame_principal, width=400, fg_color='transparent')
        frame_imagem.pack(side="left", padx=20, pady=20, fill="y")

        imagem = Image.open("imagem_main.jpeg")
        imagem_ajustada = ctk.CTkImage(light_image = imagem, size = (300,300 ))

        label_imagem = ctk.CTkLabel(frame_imagem, image = imagem_ajustada, text = "")
        label_imagem.pack(pady = 20)

        # Botão iniciar abaixo da legenda
        self.botao_login = ctk.CTkButton(
            frame_imagem,
            text="Login",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=lambda: abri_janela_login(self)
            
        )
        self.botao_login.pack(pady=10)
        
        self.botao_registrar = ctk.CTkButton(
            frame_imagem,
            text="Criar Conta",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=abri_janela_cadastro
        )
        self.botao_registrar.pack(pady=10)


        # Frame de curiosidades (direita)
        frame_curiosidades = ctk.CTkFrame(frame_principal)
        frame_curiosidades.pack(side="right", padx=20, pady=20, fill="both", expand=True)

        texto_informativo = (
            "========= CURIOSIDADES =========\n\n"
            "📊 Em 2024, o Brasil foi alvo de 356 bilhões de tentativas de ataque cibernético.\n\n"
            "🔍 Média de 1.876 ataques semanais por organização no 3º trimestre de 2024.\n\n"
            "🚨 38,7% de toda a atividade maliciosa na América Latina foi direcionada ao Brasil.\n\n"
            "📈 Crescimento de 75% em comparação com 2023 no número de incidentes registrados."
        )

        self.rotulo_info = ctk.CTkLabel(
            frame_curiosidades,
            text=texto_informativo,
            font=ctk.CTkFont(size=22),
            wraplength=400,
            justify="left"
        )
        self.rotulo_info.pack(pady=10, padx=10)


if __name__ == "__main__":
    aplicativo = AplicativoSegurancaCibernetica()
    aplicativo.mainloop()