import customtkinter as ctk
import pandas as pd

# Criando janela
def abrir_janela_cadastro():
    # Lista de países completa (Inglês)
    lista_paises = [ "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Argentina", "Armenia", "Australia",
        "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Belarus", "Belgium", "Belize",
        "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria",
        "Burkina Faso", "Burundi", "Cambodia", "Cameroon", "Canada", "Chad", "Chile", "China", "Colombia",
        "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Dominican Republic",
        "Ecuador", "Egypt", "El Salvador", "Estonia", "Ethiopia", "Finland", "France", "Gabon", "Gambia",
        "Georgia", "Germany", "Ghana", "Greece", "Guatemala", "Haiti", "Honduras", "Hungary", "Iceland",
        "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan",
        "Kazakhstan", "Kenya", "Kuwait", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya",
        "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta",
        "Mauritania", "Mexico", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique",
        "Myanmar", "Namibia", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria",
        "North Korea", "Norway", "Oman", "Pakistan", "Panama", "Paraguay", "Peru", "Philippines", "Poland",
        "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saudi Arabia", "Senegal", "Serbia", "Singapore",
        "Slovakia", "Slovenia", "Somalia", "South Africa", "South Korea", "Spain", "Sri Lanka", "Sudan",
        "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand",
        "Togo", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Uganda", "Ukraine",
        "United Arab Emirates", "UK", "USA", "Uruguay", "Uzbekistan", "Venezuela",
        "Vietnam", "Yemen", "Zambia", "Zimbabwe"
    ]
    
    # Lista de anos de 2000 até 2100
    lista_anos = [str(ano) for ano in range (2014, 2100)]

    df = pd.read_csv('Global_Cybersecurity_Threats_2015-2024.csv')
    df.columns = df.columns.str.strip()

    colunas = df.columns.to_list()
    valores_existentes = {col: sorted(df[col].dropna().astype(str).unique().tolist()) for col in colunas}

    janela = ctk.CTkToplevel()
    janela.geometry('1280x720')
    janela.title('Cadastro de novos ataques')
    janela.lift()
    janela.focus_force()
    janela.attributes('-topmost', True)
    janela.after(100, lambda: janela.attributes('-topmost', False))

    titulo = ctk.CTkLabel(janela, text='Cadastros de Novo Ataque', font=ctk.CTkFont(size=22, weight='bold'))
    titulo.pack(pady=10)

    # Frame central para os campos
    campos_frame = ctk.CTkFrame(janela)
    campos_frame.pack(pady=20)

    entradas = {}

    for i, coluna in enumerate(colunas):
        linha = i // 2
        coluna_grid = i % 2

        label = ctk.CTkLabel(campos_frame, text=coluna + ':')
        label.grid(row=linha*2, column=coluna_grid, padx=15, pady=(10, 0), sticky='w')

        if coluna.lower() == 'country':
            entrada = ctk.CTkComboBox(campos_frame, values=sorted(lista_paises))
            entrada.set(lista_paises[0])

        elif coluna.lower() == 'year':
            entrada = ctk.CTkComboBox(campos_frame, values=lista_anos)
            entrada.set(lista_anos[0])

        elif len(valores_existentes[coluna]) <= 100:
            entrada = ctk.CTkComboBox(campos_frame, values=valores_existentes[coluna])
            entrada.set(valores_existentes[coluna][0] if valores_existentes[coluna] else '')

        else:
            entrada = ctk.CTkEntry(campos_frame, placeholder_text=f'digite o valor de {coluna}')

        entrada.grid(row=linha*2+1, column=coluna_grid, padx=15, pady=(0,10), sticky='we')
        entradas[coluna.strip()] = entrada


    # função de salvar
    def salvar_dado():
        novo_dado = []
        for coluna in colunas:
            valor = entradas[coluna.strip()].get()
            novo_dado.append(valor)

        # Adiciona a nova linha
        df.loc[len(df)] = novo_dado
        df.to_csv('Global_Cybersecurity_Threats_2015-2024.csv', index=False)
        sucesso.configure(text='Dado cadastrado com sucesso!', text_color='green')

    # Botão de Salvar
    ctk.CTkButton(janela, text='Salvar', command=salvar_dado).pack(pady=10)
    sucesso = ctk.CTkLabel(janela, text='')
    sucesso.pack()
        
