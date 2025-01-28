# No terminal:
# "pip install tk"
# "pip install customtkinter"

import tkinter as tk
from customtkinter import *
from tkinter import messagebox


# Lista para cadastrar/consultar produtos 
produtos = []


# ========== PARTE FUNÇÕES  ========== #

def cadastrar_produto():
    nome = entry_nome.get()  # "entry_nome" = Entry (campo de texto) criado na parte de interface gráfica
    preco = entry_preco.get() # Mesma função que a descrita acima

    if not nome or not preco:
        messagebox.showwarning("Erro", "Por favor, preencha todos os campos.") # Caso "nome" ou "preco" estiverem vazios, retorna erro
        return


    preco = preco.replace(",", ".") # Faz com que aceite tanto vírgulas quanto pontos na hora de registrar um preço
    try:
        preco = float(preco)
    except ValueError:
        messagebox.showwarning("Erro", "O preço deve ser um número válido.") # Retorna erro caso não seja enviado um numero 
        return

    produtos.append({"nome": nome, "preco": preco}) # Adiciona o que foi inserido a lista "produtos" (criada no inicio do código)
    messagebox.showinfo("Sucesso", f"Produto '{nome}' cadastrado com sucesso!") # Retorna mensagem de sucesso
    entry_nome.delete(0, tk.END) # Limpa o campo de texto "nome"
    entry_preco.delete(0, tk.END) # Limpa o campo de texto "preco"








# ========== PARTE INTERFACE GRÁFICA CONSULTA + SCROLLBAR ========== #

def consultar_produtos():
    janela_consulta = CTkToplevel(root)  # Gera uma nova interface grafica
    janela_consulta.title("Produtos Cadastrados")
    janela_consulta.geometry("400x300")

    janela_consulta.attributes("-topmost", True) # Sempre que a janela de consulta for aberta, ela ficará por cima da antes aberta

    # Cria um "canvas" para caso haja mais itens do que se pode ser visualizado na tela
    canvas = tk.Canvas(janela_consulta) 
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Scrollbar
    scrollbar = tk.Scrollbar(janela_consulta, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Frame dentro do canvas
    frame_produtos = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame_produtos, anchor="nw")

    # Configura a scrollbar para o canvas
    canvas.configure(yscrollcommand=scrollbar.set)

    if not produtos:
        tk.Label(frame_produtos, text="Nenhum produto cadastrado.", font=("Arial", 10, "bold")).pack(pady=10) # Caso tente abrir a aba de consulta, sem nenhum antes cadastrado
    else:
        for produto in produtos:
            preco_formatado = f"{produto['preco']:.2f}".replace(".", ",") # Converte "." em "," para visualização de preço caso necessário (2f = mostra apenas 2 casas após a vírgula)
            texto = f"Produto: {produto['nome']}   |   Preço: R$ {preco_formatado}"
            tk.Label(frame_produtos, text=texto).pack(anchor="w", padx=10, pady=5)

     # Ajusta o tamanho do canvas automaticamente
    frame_produtos.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    # Adiciona suporte ao scroll pelo mouse
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # PARA FUNCIONAR NO Windows
    canvas.bind_all("<MouseWheel>", on_mousewheel)

    # PARA FUNCIONAR NO Linux/MacOS
    canvas.bind_all("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
    canvas.bind_all("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))








# ========== PARTE INTERFACE GRÁFICA PRINCIPAL ========== #

# Criação da janela principal
root = CTk()
root.title("Cadastro e Consulta de Produtos")
root.geometry("400x300")

set_appearance_mode("light")


# Titulo
CTkLabel(master=root, text="Cadastro de Produtos", font=("Arial", 16, "bold")).pack(pady=30)

frame_form = CTkFrame(root)
frame_form.pack(pady=15) #pady = Espaçamento do Titulo para os demais itens

# Widgets
CTkLabel(frame_form, text="Produto:").grid(row=0, column=0, padx=5, pady=5) #pady = Espaçamento entre campos de inserir o texto
entry_nome = CTkEntry(frame_form)
entry_nome.grid(row=0, column=1)  

CTkLabel(frame_form, text="Preço:").grid(row=1, column=0, padx=5, pady=5)
entry_preco = CTkEntry(frame_form)
entry_preco.grid(row=1, column=1)

# Botões
CTkButton(root, text="Cadastrar Produto", corner_radius=32, font=("Arial", 13, "bold"), command=cadastrar_produto).pack(pady=10)  
CTkButton(root, text="Consultar Produtos", corner_radius=32, font=("Arial", 13, "bold"), command=consultar_produtos).pack(pady=5)  


root.mainloop()