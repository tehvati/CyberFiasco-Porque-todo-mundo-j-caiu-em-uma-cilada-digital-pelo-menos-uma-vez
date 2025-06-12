import customtkinter as ctk
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image, ImageDraw, ImageOps
from cadastro import abrir_janela_cadastro
from atualizardeletar import abrir_janela_atualizar
from quiz import abri_janela_quiz

# Carregando a base de dados
df = pd.read_csv("Global_Cybersecurity_Threats_2015-2024.csv")

# Criando Janela Home
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')
janela = ctk.CTk()
janela.title("Segurança Cibernética")
janela.geometry('1280x720')

# Cabeçalho
cabecalho = ctk.CTkFrame(janela, corner_radius=15)
cabecalho.pack(fill="x", padx=20, pady=10)

ctk.CTkLabel(cabecalho, text="Segurança Cibernética: \nAnálise de Dados e Dicas de Proteção", font=ctk.CTkFont(family='Segoe UI', size=26, weight='bold')).pack(side="left", padx=10)
ctk.CTkButton(cabecalho, text='Atualizar/ Deletar\n Dados', font=ctk.CTkFont(size=14), command=abrir_janela_atualizar).pack(side="right", padx=10)
ctk.CTkButton(cabecalho, text="Cadastrar Novo\n Ataque", font=ctk.CTkFont(size=14), command=abrir_janela_cadastro).pack(side="right", padx=10)

# Frame Principal
frame_central = ctk.CTkFrame(janela, fg_color='transparent')
frame_central.pack(pady=20, padx=20, expand=True, fill='both')

#Frame para mascote
frame_imagem = ctk.CTkFrame(frame_central, fg_color='transparent')
frame_imagem.pack(side='left', padx=20, fill='y')

# Frame para ficar do lado direito da página
frame_direita = ctk.CTkFrame(frame_central, fg_color='transparent')
frame_direita.pack(side='right', fill='both', expand=True)

# Frame filtro
filtro_frame = ctk.CTkFrame(frame_direita)
filtro_frame.pack(pady=10)

# Frame Botões gerar gráfico e limpar filtros
botao_frame = ctk.CTkFrame(frame_direita)
botao_frame.pack(pady=10)

# Frame botão quiz
botao_quiz_frame = ctk.CTkFrame(frame_direita)
botao_quiz_frame.pack(pady=10)

# Função para arrendondar Imagem
def arredondar_imagem(img, raio=30):
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([0, 0, img.size[0], img.size[1]], radius=raio, fill=255)
    img = img.convert("RGBA")
    resultado = ImageOps.fit(img, img.size, centering=(0.5, 0.5))
    resultado.putalpha(mask)
    return resultado

# Adicionando Imagem do Mascote
imagem_raposa = arredondar_imagem(Image.open('imagem2.png'), raio=40)
imagem_ajustada = ctk.CTkImage(light_image=imagem_raposa, size=(500, 500))
ctk.CTkLabel(frame_imagem, image=imagem_ajustada, text='').pack(pady=20)

# Variaveis para armazenar checkbox
checkbox_anos, checkbox_paises, checkbox_tipos = {}, {}, {}

# Filtro Ano
anos_disponiveis = sorted(df["Year"].dropna().unique())
frame_anos = ctk.CTkScrollableFrame(filtro_frame, width=180, height=180, label_text="Ano")
frame_anos.grid(row=0, column=0, padx=10, pady=10)
for ano in anos_disponiveis:
    var = ctk.BooleanVar()
    ctk.CTkCheckBox(frame_anos, text=str(ano), variable=var).pack(anchor='w')
    checkbox_anos[ano] = var

# Filtro País
paises_disponiveis = sorted(df["Country"].dropna().unique())
frame_paises = ctk.CTkScrollableFrame(filtro_frame, width=180, height=180, label_text="País")
frame_paises.grid(row=0, column=1, padx=10, pady=10)
for pais in paises_disponiveis:
    var = ctk.BooleanVar()
    ctk.CTkCheckBox(frame_paises, text=pais, variable=var).pack(anchor='w')
    checkbox_paises[pais] = var

# Filtro Tipo de Ataque
tipos_ataque = sorted(df["Attack Type"].dropna().unique())
frame_tipos = ctk.CTkScrollableFrame(filtro_frame, width=180, height=180, label_text="Tipo de Ataque")
frame_tipos.grid(row=0, column=2, padx=10, pady=10)
for tipo in tipos_ataque:
    var = ctk.BooleanVar()
    ctk.CTkCheckBox(frame_tipos, text=tipo, variable=var).pack(anchor='w')
    checkbox_tipos[tipo] = var

# Filtro tipo de gráfico
combo_grafico = ctk.CTkComboBox(filtro_frame, values=["Barras", "Pizza", "Linha"])
combo_grafico.set("Tipo de Gráfico")
combo_grafico.grid(row=1, column=0, padx=10, pady=10)

combo_orientacao = ctk.CTkComboBox(filtro_frame, values=["Eixo X: Tipo de ataque", "Eixo X: País"])
combo_orientacao.set("Barra: Eixo X")
combo_orientacao.grid(row=1, column=1, padx=10, pady=10)

combo_orientacao_y = ctk.CTkComboBox(filtro_frame, values=["Eixo y: Nº infectados", "Eixo y: Perdas Financeiras"])
combo_orientacao_y.set("Barra: Eixo Y")
combo_orientacao_y.grid(row=1, column=2, padx=10, pady=10)

# Função para gerar gráficos
def gerar_grafico():
    tipo_grafico = combo_grafico.get()
    orientacao_X = combo_orientacao.get()
    orientacao_y = combo_orientacao_y.get()
    df = pd.read_csv("Global_Cybersecurity_Threats_2015-2024.csv")
    df.columns = df.columns.str.strip()

    anos_selecionados = [ano for ano, var in checkbox_anos.items() if var.get()]
    paises_selecionados = [pais for pais, var in checkbox_paises.items() if var.get()]
    tipos_selecionados = [tipo for tipo, var in checkbox_tipos.items() if var.get()]

    if anos_selecionados:
        df = df[df['Year'].isin(anos_selecionados)]
    if paises_selecionados:
        df = df[df['Country'].isin(paises_selecionados)]
    if tipos_selecionados:
        df = df[df['Attack Type'].isin(tipos_selecionados)]

    if df.empty:
        print('Nenhum dado encontrado com os filtros aplicados.')
        return

    resumo = df.groupby("Attack Type")["Number of Affected Users"].sum().sort_values(ascending=False)
    print("Resumo de ataques:")
    print(resumo.head(5))

    if tipo_grafico == 'Barras':
        if orientacao_X == "Eixo X: País" and orientacao_y == 'Eixo y: Nº infectados':
            fig = px.bar(df, y='Number of Affected Users', x='Country', color='Attack Type', barmode='stack', title='Ameaça por País')
        elif orientacao_X == "Eixo X: País" and orientacao_y == 'Eixo y: Perdas Financeiras':
            fig = px.bar(df, y='Financial Loss (in Million $)', x='Country', color='Attack Type', barmode='stack', title='Ameaça por País')
        elif orientacao_X == "Eixo X: Tipo de ataque" and orientacao_y == 'Eixo y: Nº infectados':
            fig = px.bar(df, x='Attack Type', y='Number of Affected Users', color='Country', barmode='stack', title='Tipos de Ameaças')
        else:
            fig = px.bar(df, x='Attack Type', y='Financial Loss (in Million $)', color='Country', barmode='stack', title='Tipos de Ameaças')
        fig.show()

    elif tipo_grafico == 'Pizza':
        if paises_selecionados:
            cols = 2
            rows = (len(paises_selecionados) + 1) // cols
            fig = make_subplots(rows=rows, cols=cols, specs=[[{"type": "domain"}]*cols for _ in range(rows)])
            for i, pais in enumerate(paises_selecionados):
                df_pais = df[df['Country'] == pais]
                if not df_pais.empty:
                    row, col = divmod(i, cols)
                    fig.add_trace(go.Pie(labels=df_pais['Attack Type'], values=df_pais['Number of Affected Users'], name=pais), row=row+1, col=col+1)
            fig.update_layout(title_text="Distribuição de Ameaças por País")
            fig.show()
        else:
            fig = px.pie(df, names='Attack Type', title='Distribuição de Ameaças (Todos os Países)')
            fig.show()

    elif tipo_grafico == 'Linha':
        df_linha = df.copy()
        df_linha = df_linha.groupby(['Year', 'Attack Type']).size().reset_index(name='Número de ataques por ano')                
        fig = px.line(df_linha, x='Year', y='Número de ataques por ano', color='Attack Type', title='Evolução de Ameaças por ano')
        fig.show()
    else:
        print('Tipo de gráfico inválido.')
        return

# Função para limpar filtros
def limpar_filtros():
    for var in checkbox_anos.values(): var.set(False)
    for var in checkbox_paises.values(): var.set(False)
    for var in checkbox_tipos.values(): var.set(False)
    combo_grafico.set('Tipo de Gráfico')
    combo_orientacao.set('Barra: Eixo X')
    combo_orientacao_y.set('Barra: Eixo Y')

# Botões de aplicar Filtro, limpar filtro e quiz
ctk.CTkButton(botao_frame, text="Gerar Gráfico", font=ctk.CTkFont(size=14), command=gerar_grafico).grid(row=0, column=0, padx=10, pady=10)
ctk.CTkButton(botao_frame, text='Limpar Filtros', font=ctk.CTkFont(size=14), fg_color='green', hover_color="#054B03", command=limpar_filtros).grid(row=0, column=1, padx=10, pady=10)
ctk.CTkButton(botao_quiz_frame, text='Que tal um quiz?', font=ctk.CTkFont(size=14), command=abri_janela_quiz).pack(pady=10)

janela.mainloop()