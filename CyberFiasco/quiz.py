import pandas as pd
import customtkinter as ctk
import random

# Carrega os dados
df = pd.read_csv("Global_Cybersecurity_Threats_2015-2024.csv")

def abri_janela_quiz():
    ano = df['Year'].sample(1).iloc[0]
    contagem_paises = df[df['Year'] == ano]['Country'].value_counts()

    pais_top = contagem_paises.idxmax()
    incidentes_pais_top = contagem_paises.max()
    pais_alt = contagem_paises.index[1]

    ataque_top = df['Attack Type'].value_counts().idxmax()
    ataque_alt = df['Attack Type'].value_counts().index[1]

    ano_top = df['Year'].value_counts().idxmax()
    ano_alt = df['Year'].value_counts().index[1]
    qtd_ataques = df['Year'].value_counts()[ano_top]

    pais_prejuizo = df.groupby('Country')['Financial Loss (in Million $)'].sum().idxmax()
    pais_prejuizo_alt = df.groupby('Country')['Financial Loss (in Million $)'].sum().nlargest(2).index[1]
    prejuizo = df.groupby('Country')['Financial Loss (in Million $)'].sum().max()

    ataque_usuarios = df.groupby('Attack Type')['Number of Affected Users'].sum().idxmax()
    ataque_usuarios_alt = df.groupby('Attack Type')['Number of Affected Users'].sum().nlargest(2).index[1]
    usuarios_afetados_max = df.groupby('Attack Type')['Number of Affected Users'].sum().max()

    setor_mais_visado = df['Target Industry'].value_counts().idxmax()
    setor_mais_visado_alt = df['Target Industry'].value_counts().index[1]
    setor_incidentes = df['Target Industry'].value_counts()[setor_mais_visado]

    tempo_medio_resolucao = str(round(df['Incident Resolution Time (in Hours)'].mean()))
    tempo_medio_resolucao_alt = str(round(df['Incident Resolution Time (in Hours)'].mean() + 10))

    usuarios_afetados = str(int(df['Number of Affected Users'].max()))
    usuarios_afetados_alt = str(int(df['Number of Affected Users'].nlargest(2).iloc[1]))
    usuarios_afetados_menor = str(int(df['Number of Affected Users'].min()))

    grupo_ataques_ano = df[df['Year'] == ano]['Attack Source'].value_counts().idxmax()
    grupo_ataques_ano_alt = df[df['Year'] == ano]['Attack Source'].value_counts().index[1]
    grupo_ataque_max = df[df['Year'] == ano]['Attack Source'].value_counts().max()

    perguntas = [
        (f"Qual país teve mais incidentes em {ano}?",
         pais_top,
         pais_alt,
         f"{pais_top} sofreu {incidentes_pais_top} incidentes em {ano}, sendo o mais afetado."),

        ("Qual foi o tipo de ataque mais comum entre 2015 e 2024?",
         ataque_top,
         ataque_alt,
         f"{ataque_top} foi o mais frequente em todo o período."),

        ("Em qual ano ocorreu o maior número de incidentes?",
         ano_top,
         ano_alt,
         f"{ano_top} teve {qtd_ataques} registros de incidentes cibernéticos, sendo o ano mais crítico."),

        ("Qual país teve o maior prejuízo financeiro total?",
         pais_prejuizo,
         pais_prejuizo_alt,
         f"Acumulou a maior perda financeira, de {prejuizo} em milhões de dólares."),

        ("Qual tipo de ataque afetou mais usuários no total?",
         ataque_usuarios,
         ataque_usuarios_alt,
         f"{ataque_usuarios} teve o maior número de usuários impactados, com {usuarios_afetados_max} pessoas afetadas."),

        ("Qual foi o setor mais visado por ataques cibernéticos?",
         setor_mais_visado,
         setor_mais_visado_alt,
         f"O setor de {setor_mais_visado} sofreu um total de {setor_incidentes} incidentes."),

        ("Qual foi o tempo médio de resolução de incidentes cibernéticos em horas?",
         tempo_medio_resolucao,
         tempo_medio_resolucao_alt,
         "Até que rápido, não?"),

        ("Qual foi o maior número de usuários afetados nos incidentes?",
         usuarios_afetados,
         usuarios_afetados_alt,
         f"Sabe qual foi a menor quantidade? {usuarios_afetados_menor}."),

        (f"Qual grupo foi responsável pelo maior número de ataques cibernéticos em {ano}?",
         grupo_ataques_ano,
         grupo_ataques_ano_alt,
         f"Este grupo liderou em número de ataques, com {grupo_ataque_max} incidentes."),

        ("Qual falha comum explorada em ataques de engenharia social?",
         "Phishing", "Cross-site scripting",
         "Phishing engana usuários para obter informações confidenciais."),

        ("Qual é o principal objetivo de um ransomware?",
         "Criptografar e exigir resgate", "Roubar dados silenciosamente",
         "O ransomware bloqueia os dados e exige pagamento para liberá-los."),

        ("O que é um zero-day vulnerability?",
         "Uma falha ainda não corrigida", "Uma falha de hardware",
         "Zero-day é uma vulnerabilidade desconhecida pelos desenvolvedores."),

        ("O que é um honeypot na segurança cibernética?",
         "Um sistema para atrair atacantes", "Uma rede interna segura",
         "Honeypots simulam sistemas vulneráveis para atrair hackers."),

        ("Qual dos ataques explora falhas de validação em formulários web?",
         "SQL Injection", "Man-in-the-Middle",
         "SQL Injection permite a manipulação de consultas a bancos de dados."),

        ("Qual desses é um exemplo de ataque passivo?",
         "Interceptação de tráfego", "Defacement de site",
         "Ataques passivos monitoram dados sem alterar sistemas."),
    ]

    random.shuffle(perguntas)

    app = ctk.CTk()
    app.title("Quiz de Cibersegurança")
    app.geometry("700x340")

    indice = pontos = 0

    pergunta_label = ctk.CTkLabel(app, text="", wraplength=650, font=("Roboto", 25))
    pergunta_label.pack(pady=20)

    botoes = [ctk.CTkButton(app, text="", font=("Roboto", 16)) for _ in range(2)]
    for botao in botoes:
        botao.pack(pady=5)

    resultado_label = ctk.CTkLabel(app, text="", font=("Roboto", 16), wraplength=650, justify="center")
    resultado_label.pack(pady=15)

    progresso_bar = ctk.CTkProgressBar(app)
    progresso_bar.pack(pady=30)
    progresso_bar.set(0)

    def mostrar_pergunta():
        nonlocal indice
        total = len(perguntas)
        progresso_bar.set(indice / total)

        if indice >= total:
            progresso_bar.set(1)
            pergunta_label.configure(text="✅ Quiz finalizado!")
            for b in botoes:
                b.pack_forget()
            resultado_label.configure(text=f"Sua pontuação final: {pontos}/{total}")
            return

        texto, correta, incorreta, _ = perguntas[indice]
        pergunta_label.configure(text=f"{indice + 1}. {texto}")
        opcoes = [correta, incorreta]
        random.shuffle(opcoes)

        for i, texto_opcao in enumerate(opcoes):
            botoes[i].configure(text=texto_opcao, command=lambda t=texto_opcao: verificar_resposta(t))

        resultado_label.configure(text="")

    def verificar_resposta(escolha):
        nonlocal indice, pontos
        _, correta, _, comentario = perguntas[indice]

        if str(escolha).lower() == str(correta).lower():
            resultado_label.configure(text=f"✅ Correto!\n{comentario}", text_color="green")
            pontos += 1
        else:
            resultado_label.configure(text=f"❌ Errado! Resposta certa: {correta}\n{comentario}", text_color="red")

        indice += 1
        app.after(4000, mostrar_pergunta)

    mostrar_pergunta()
    app.mainloop()