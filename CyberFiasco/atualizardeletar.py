import pandas as pd
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk

# Função abrir janela de Atualizar e Deletar dados
def abrir_janela_atualizar():
    df = pd.read_csv("Global_Cybersecurity_Threats_2015-2024.csv")
    df.columns = df.columns.str.strip()

    historico = []

    janela = ctk.CTkToplevel()
    janela.geometry("1280x720")
    janela.title("Atualizar/Deletar Dados")
    janela.lift()
    janela.focus_force()
    janela.attributes('-topmost', True)
    janela.after(100, lambda: janela.attributes('-topmost', False))

    colunas = df.columns.tolist()
    entradas_filtros = {}

    # Filtros em duas linhas
    filtros_frame = ctk.CTkFrame(janela)
    filtros_frame.pack(pady=10)

    for i, coluna in enumerate(colunas):
        linha = 0 if i < 5 else 2
        coluna_grid = i % 5

        label = ctk.CTkLabel(filtros_frame, text=coluna)
        label.grid(row=linha, column=coluna_grid, padx=5, pady=5)

        entrada = ctk.CTkEntry(filtros_frame, placeholder_text=f"Filtrar {coluna}")
        entrada.grid(row=linha + 1, column=coluna_grid, padx=5, pady=5)

        entradas_filtros[coluna] = entrada

    # Frame da tabela com scroll
    tabela_frame = tk.Frame(janela)
    tabela_frame.pack(pady=20, fill="both", expand=True)

    scroll_y = tk.Scrollbar(tabela_frame, orient="vertical")
    scroll_x = tk.Scrollbar(tabela_frame, orient="horizontal")

    tree = ttk.Treeview(
        tabela_frame,
        columns=colunas,
        show="headings",
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set
    )

    scroll_y.pack(side="right", fill="y")
    scroll_x.pack(side="bottom", fill="x")
    tree.pack(fill="both", expand=True)

    scroll_y.config(command=tree.yview)
    scroll_x.config(command=tree.xview)

    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center")

    # Atualizar a tabela com os filtros
    def atualizar_tabela():
        for item in tree.get_children():
            tree.delete(item)

        df_filtrado = df.copy()
        for col in colunas:
            valor = entradas_filtros[col].get().strip()
            if valor:
                df_filtrado = df_filtrado[df_filtrado[col].astype(str).str.contains(valor, case=False)]

        for index, row in df_filtrado.iterrows():
            tree.insert("", "end", iid=index, values=list(row))

    # Editar célula com duplo clique
    def editar_celula(event):
        item_id = tree.focus()
        if not item_id:
            return

        col = tree.identify_column(event.x)
        col_index = int(col.replace("#", "")) - 1
        coluna_nome = colunas[col_index]

        x, y, width, height = tree.bbox(item_id, col)
        valor_atual = tree.item(item_id, "values")[col_index]

        editor = tk.Entry(tabela_frame)
        editor.place(x=x, y=y + 2, width=width, height=height)
        editor.insert(0, valor_atual)
        editor.focus()

        def salvar(event):
            novo_valor = editor.get()
            valores = list(tree.item(item_id, "values"))
            valor_antigo = valores[col_index]

            if novo_valor != valor_antigo:
                historico.append(("edit", int(item_id), colunas[col_index], valor_antigo))

                valores[col_index] = novo_valor
                tree.item(item_id, values=valores)
                df.loc[int(item_id), colunas[col_index]] = novo_valor
                df.to_csv("Global_Cybersecurity_Threats_2015-2024.csv", index=False)

            editor.destroy()

        editor.bind("<Return>", salvar)
        editor.bind("<FocusOut>", lambda e: editor.destroy())

    tree.bind("<Double-1>", editar_celula)

    # Excluir linha selecionada
    def deletar_linha():
        item = tree.focus()
        if item:
            index = int(item)
            linha = df.loc[index].copy() 
            historico.append(('delete', index, linha))

            df.drop(index, inplace=True)
            df.to_csv("Global_Cybersecurity_Threats_2015-2024.csv", index=False)
            atualizar_tabela()

    # Desfaz a ultima alteração feita 
    def desfazer_ultima_acao():
        if not historico:
            print("Nada para desfazer.")
            return
        
        acao = historico.pop()

        if acao[0] == "edit":
            index, coluna, valor_antigo = acao[1], acao[2], acao[3]
            df.loc[index, coluna] = valor_antigo
            df.to_csv("Global_Cybersecurity_Threats_2015-2024.csv", index=False)
            atualizar_tabela()

        elif acao[0] == "delete":
            index, linha_restaurada = acao[1], acao[2]
            df.loc[index] = linha_restaurada
            df.sort_index(inplace=True)
            df.to_csv("Global_Cybersecurity_Threats_2015-2024.csv", index=False)
            atualizar_tabela()

    # Botões
    botoes_frame = ctk.CTkFrame(janela, fg_color="transparent")
    botoes_frame.pack(pady=10)

    ctk.CTkButton(botoes_frame, text="Aplicar Filtros", command=atualizar_tabela).pack(side="left", padx=10)
    ctk.CTkButton(botoes_frame, text="Deletar Linha", command=deletar_linha, fg_color="red").pack(side="left", padx=10)
    ctk.CTkButton(botoes_frame, text="Desfazer", command=desfazer_ultima_acao, fg_color="green").pack(side="left", padx=10)

    atualizar_tabela()

