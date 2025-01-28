import tkinter as tk
from tkinter import messagebox

# Lista para cadastrar/consultar produtos 
produtos = []

# ========== PARTE FUNÇÕES  ========== #
def cadastrar_produto():
    nome = entry_nome.get()
    preco = entry_preco.get()

    if not nome or not preco:
        messagebox.showwarning("Erro", "Por favor, preencha todos os campos.")
        return

    preco = preco.replace(",", ".")
    try:
        preco = float(preco)
    except ValueError:
        messagebox.showwarning("Erro", "O preço deve ser um número válido.")
        return

    produtos.append({"nome": nome, "preco": preco})
    messagebox.showinfo("Sucesso", f"Produto '{nome}' cadastrado com sucesso!")
    entry_nome.delete(0, tk.END)
    entry_preco.delete(0, tk.END)

# ========== PARTE INTERFACE GRÁFICA CONSULTA + SCROLLBAR ========== #
def consultar_produtos():
    janela_consulta = tk.Toplevel(root)
    janela_consulta.title("Produtos Cadastrados")
    janela_consulta.geometry("400x300")
    janela_consulta.attributes("-topmost", True)

    canvas = tk.Canvas(janela_consulta)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(janela_consulta, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    frame_produtos = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame_produtos, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    if not produtos:
        tk.Label(frame_produtos, text="Nenhum produto cadastrado.", font=("Arial", 10, "bold")).pack(pady=10)
    else:
        for produto in produtos:
            preco_formatado = f"{produto['preco']:.2f}".replace(".", ",")
            texto = f"Produto: {produto['nome']}   |   Preço: R$ {preco_formatado}"
            tk.Label(frame_produtos, text=texto).pack(anchor="w", padx=10, pady=5)

    frame_produtos.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", on_mousewheel)
    canvas.bind_all("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
    canvas.bind_all("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))

# ========== PARTE INTERFACE GRÁFICA PRINCIPAL ========== #
root = tk.Tk()
root.title("Cadastro e Consulta de Produtos")
root.geometry("400x300")

# Título
tk.Label(root, text="Cadastro de Produtos", font=("Arial", 16, "bold")).pack(pady=30)

frame_form = tk.Frame(root)
frame_form.pack(pady=15)

# Widgets
tk.Label(frame_form, text="Produto:").grid(row=0, column=0, padx=5, pady=5)
entry_nome = tk.Entry(frame_form)
entry_nome.grid(row=0, column=1)

tk.Label(frame_form, text="Preço:").grid(row=1, column=0, padx=5, pady=5)
entry_preco = tk.Entry(frame_form)
entry_preco.grid(row=1, column=1)

# Botões
tk.Button(root, text="Cadastrar Produto", font=("Arial", 13, "bold"), command=cadastrar_produto).pack(pady=10)
tk.Button(root, text="Consultar Produtos", font=("Arial", 13, "bold"), command=consultar_produtos).pack(pady=5)

root.mainloop()
