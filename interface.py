
import tkinter as tk
from tkinter import messagebox
from banco import Kroche
from database import criar_tabelas

# Inicialização
criar_tabelas()
loja = Kroche()

# Configuração da janela
janela = tk.Tk()
janela.title("Sistema de Gerenciamento de Crochê")
janela.geometry("650x850")
janela.minsize(520, 650)
janela.configure(bg= "#2df744")

COR_FUNDO = "#586D4A"
COR_TITULO = "#22211F"
COR_BOTAO = "#48453D"

# Área principal com rolagem
container = tk.Frame(janela, bg=COR_FUNDO)
container.pack(fill="both", expand=True)

canvas = tk.Canvas(
    container,
    bg=COR_FUNDO,
    highlightthickness=0
)
barra = tk.Scrollbar(
    container,
    orient="vertical",
    command=canvas.yview
)

conteudo = tk.Frame(canvas, bg=COR_FUNDO)

janela_conteudo = canvas.create_window(
    (0, 0),
    window=conteudo,
    anchor="nw"
)

conteudo.bind(
    "<Configure>",
    lambda evento: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.configure(yscrollcommand=barra.set)
canvas.pack(side="left", fill="both", expand=True)
barra.pack(side="right", fill="y")

canvas.bind(
    "<Configure>",
    lambda evento: canvas.itemconfig(
        janela_conteudo,
        width=evento.width
    )
)

# Funções auxiliares
def criar_secao(titulo):
    quadro = tk.LabelFrame(
        conteudo,
        text=titulo,
        padx=12,
        pady=10,
        font=("Arial", 10, "bold")
    )
    quadro.pack(fill="x", padx=15, pady=9)
    return quadro


def criar_campo(quadro, texto):
    tk.Label(quadro, text=texto).pack(anchor="w")
    entrada = tk.Entry(quadro)
    entrada.pack(fill="x", pady=4)
    return entrada


def criar_botao(quadro, texto, comando):
    tk.Button(
        quadro,
        text=texto,
        command=comando,
        bg=COR_BOTAO,
        fg="white",
        activebackground="#4444DD",
        activeforeground="white",
        relief="flat",
        padx=10,
        pady=5,
        cursor="hand2"
    ).pack(pady=5)


def mostrar_resultados(titulo, dados):
    tela = tk.Toplevel(janela)
    tela.title(titulo)
    tela.geometry("650x400")

    tk.Label(
        tela,
        text=titulo,
        font=("Arial", 13, "bold")
    ).pack(pady=10)

    frame = tk.Frame(tela)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    barra = tk.Scrollbar(frame)
    barra.pack(side="right", fill="y")

    area = tk.Text(
        frame,
        wrap="word",
        yscrollcommand=barra.set
    )
    area.pack(side="left", fill="both", expand=True)
    barra.config(command=area.yview)

    if dados:
        for registro in dados:
            area.insert(tk.END, f"{registro}\n\n")
    else:
        area.insert(tk.END, "Nenhum registro encontrado.")

    area.config(state="disabled")


def executar_acao(funcao, mensagem, limpar=None):
    try:
        sucesso = funcao()

        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)

            if limpar:
                for campo in limpar:
                    campo.delete(0, tk.END)

        elif sucesso is False:
            messagebox.showwarning(
                "Atenção",
                "A operação não foi realizada. Verifique os dados."
            )

    except Exception as erro:
        messagebox.showerror(
            "Erro",
            f"Não foi possível realizar a operação:\n{erro}"
        )


# Título
tk.Label(
    conteudo,
    text="Sistema de Gerenciamento de Crochê",
    font=("Arial", 18, "bold"),
    bg=COR_TITULO,
    fg="white",
    pady=18
).pack(fill="x")


# ==================================================
# CROCHÊS
# ==================================================

secao = criar_secao("Cadastrar Crochê")
nome_kroche = criar_campo(secao, "Nome do crochê:")


def cadastrar_kroche():
    nome = nome_kroche.get().strip()

    if not nome:
        messagebox.showwarning("Atenção", "Informe o nome.")
        return

    executar_acao(
        lambda: loja.cadastrar_kroche(nome),
        "Crochê cadastrado com sucesso!",
        [nome_kroche]
    )


def listar_kroches():
    try:
        dados = loja.listar_kroche()
        mostrar_resultados("Crochês cadastrados", dados)
    except Exception as erro:
        messagebox.showerror("Erro", str(erro))


criar_botao(secao, "Cadastrar Crochê", cadastrar_kroche)
criar_botao(secao, "Listar Crochês", listar_kroches)


# ==================================================
# CLIENTES
# ==================================================

secao = criar_secao("Clientes")

nome_cliente = criar_campo(secao, "Nome:")
cpf_cliente = criar_campo(secao, "CPF:")
telefone_cliente = criar_campo(secao, "Telefone:")


def cadastrar_cliente():
    nome = nome_cliente.get().strip()
    cpf = cpf_cliente.get().strip()
    telefone = telefone_cliente.get().strip()

    if not nome or not cpf or not telefone:
        messagebox.showwarning(
            "Atenção",
            "Preencha todos os campos."
        )
        return

    executar_acao(
        lambda: loja.cadastrar_cliente(nome, cpf, telefone),
        "Cliente cadastrado com sucesso!",
        [nome_cliente, cpf_cliente, telefone_cliente]
    )


def listar_clientes():
    try:
        dados = loja.listar_clientes()
        mostrar_resultados("Clientes cadastrados", dados)
    except Exception as erro:
        messagebox.showerror("Erro", str(erro))


cpf_busca = criar_campo(secao, "CPF para buscar cliente:")


def buscar_cliente():
    cpf = cpf_busca.get().strip()

    if not cpf:
        messagebox.showwarning("Atenção", "Informe o CPF.")
        return

    try:
        cliente = loja.buscar_cliente(cpf)

        if cliente:
            mostrar_resultados("Cliente encontrado", [cliente])
        else:
            messagebox.showinfo("Busca", "Cliente não encontrado.")

    except Exception as erro:
        messagebox.showerror("Erro", str(erro))


id_cliente = criar_campo(secao, "ID do cliente para excluir:")


def excluir_cliente():
    try:
        identificador = int(id_cliente.get().strip())
    except ValueError:
        messagebox.showwarning("Atenção", "Informe um ID válido.")
        return

    executar_acao(
        lambda: loja.excluir_cliente(identificador),
        "Cliente excluído com sucesso!",
        [id_cliente]
    )


criar_botao(secao, "Cadastrar Cliente", cadastrar_cliente)
criar_botao(secao, "Listar Clientes", listar_clientes)
criar_botao(secao, "Buscar Cliente", buscar_cliente)
criar_botao(secao, "Excluir Cliente", excluir_cliente)


# ==================================================
# VENDEDORES
# ==================================================

secao = criar_secao("Vendedores")

nome_vendedor = criar_campo(secao, "Nome:")
cpf_vendedor = criar_campo(secao, "CPF:")
telefone_vendedor = criar_campo(secao, "Telefone:")


def cadastrar_vendedor():
    nome = nome_vendedor.get().strip()
    cpf = cpf_vendedor.get().strip()
    telefone = telefone_vendedor.get().strip()

    if not nome or not cpf or not telefone:
        messagebox.showwarning(
            "Atenção",
            "Preencha todos os campos."
        )
        return

    executar_acao(
        lambda: loja.cadastrar_vendedor(nome, cpf, telefone),
        "Vendedor cadastrado com sucesso!",
        [nome_vendedor, cpf_vendedor, telefone_vendedor]
    )


def listar_vendedores():
    try:
        dados = loja.listar_vendedores()
        mostrar_resultados("Vendedores cadastrados", dados)
    except Exception as erro:
        messagebox.showerror("Erro", str(erro))


id_vendedor = criar_campo(secao, "ID do vendedor para excluir:")


def excluir_vendedor():
    try:
        identificador = int(id_vendedor.get().strip())
    except ValueError:
        messagebox.showwarning("Atenção", "Informe um ID válido.")
        return

    executar_acao(
        lambda: loja.excluir_vendedor(identificador),
        "Vendedor excluído com sucesso!",
        [id_vendedor]
    )


criar_botao(secao, "Cadastrar Vendedor", cadastrar_vendedor)
criar_botao(secao, "Listar Vendedores", listar_vendedores)
criar_botao(secao, "Excluir Vendedor", excluir_vendedor)


# ==================================================
# PRODUTOS E ESTOQUE
# ==================================================

secao = criar_secao("Produtos e Estoque")

nome_produto = criar_campo(secao, "Nome do produto:")
preco_produto = criar_campo(secao, "Preço (R$):")
quantidade_produto = criar_campo(secao, "Quantidade em estoque:")


def cadastrar_produto():
    nome = nome_produto.get().strip()

    try:
        preco = float(
            preco_produto.get().strip().replace(",", ".")
        )
        quantidade = int(quantidade_produto.get().strip())
    except ValueError:
        messagebox.showwarning(
            "Atenção",
            "Informe preço e quantidade válidos."
        )
        return

    if not nome:
        messagebox.showwarning("Atenção", "Informe o nome.")
        return

    executar_acao(
        lambda: loja.cadastrar_produto(
            nome, preco, quantidade
        ),
        "Produto cadastrado com sucesso!",
        [nome_produto, preco_produto, quantidade_produto]
    )


def listar_produtos():
    try:
        dados = loja.listar_produtos()
        mostrar_resultados("Produtos cadastrados", dados)
    except Exception as erro:
        messagebox.showerror("Erro", str(erro))


id_busca_produto = criar_campo(secao, "ID do produto para buscar:")


def buscar_produto():
    try:
        identificador = int(id_busca_produto.get().strip())
    except ValueError:
        messagebox.showwarning("Atenção", "Informe um ID válido.")
        return

    try:
        produto = loja.buscar_produto(identificador)

        if produto:
            mostrar_resultados("Produto encontrado", [produto])
        else:
            messagebox.showinfo("Busca", "Produto não encontrado.")

    except Exception as erro:
        messagebox.showerror("Erro", str(erro))


id_estoque = criar_campo(secao, "ID do produto:")
nova_quantidade = criar_campo(secao, "Nova quantidade em estoque:")


def atualizar_estoque():
    try:
        identificador = int(id_estoque.get().strip())
        quantidade = int(nova_quantidade.get().strip())
    except ValueError:
        messagebox.showwarning(
            "Atenção",
            "Informe ID e quantidade válidos."
        )
        return

    executar_acao(
        lambda: loja.atualizar_estoque(
            identificador, quantidade
        ),
        "Estoque atualizado com sucesso!",
        [id_estoque, nova_quantidade]
    )


id_excluir_produto = criar_campo(secao, "ID do produto para excluir:")


def excluir_produto():
    try:
        identificador = int(id_excluir_produto.get().strip())
    except ValueError:
        messagebox.showwarning("Atenção", "Informe um ID válido.")
        return

    executar_acao(
        lambda: loja.excluir_produto(identificador),
        "Produto excluído com sucesso!",
        [id_excluir_produto]
    )


criar_botao(secao, "Cadastrar Produto", cadastrar_produto)
criar_botao(secao, "Listar Produtos", listar_produtos)
criar_botao(secao, "Buscar Produto", buscar_produto)
criar_botao(secao, "Atualizar Estoque", atualizar_estoque)
criar_botao(secao, "Excluir Produto", excluir_produto)


# ==================================================
# MÉTODOS DE PAGAMENTO
# ==================================================

secao = criar_secao("Métodos de Pagamento")

nome_pagamento = criar_campo(secao, "Nome do método:")
preco_pagamento = criar_campo(secao, "Valor (R$):")
quantidade_pagamento = criar_campo(secao, "Quantidade:")
historico_pagamento = criar_campo(secao, "Histórico:")


def cadastrar_pagamento():
    nome = nome_pagamento.get().strip()
    historico = historico_pagamento.get().strip()

    try:
        preco = float(
            preco_pagamento.get().strip().replace(",", ".")
        )
        quantidade = int(quantidade_pagamento.get().strip())
    except ValueError:
        messagebox.showwarning(
            "Atenção",
            "Informe valor e quantidade válidos."
        )
        return

    if not nome or not historico:
        messagebox.showwarning(
            "Atenção",
            "Preencha o nome e o histórico."
        )
        return

    executar_acao(
        lambda: loja.cadastrar_pagamento(
            nome, preco, quantidade, historico
        ),
        "Método de pagamento cadastrado!",
        [
            nome_pagamento,
            preco_pagamento,
            quantidade_pagamento,
            historico_pagamento
        ]
    )


def listar_pagamentos():
    try:
        dados = loja.listar_pagamentos()
        mostrar_resultados("Métodos de pagamento", dados)
    except Exception as erro:
        messagebox.showerror("Erro", str(erro))


id_pagamento = criar_campo(secao, "ID do método para excluir:")


def excluir_pagamento():
    try:
        identificador = int(id_pagamento.get().strip())
    except ValueError:
        messagebox.showwarning("Atenção", "Informe um ID válido.")
        return

    executar_acao(
        lambda: loja.excluir_pagamento(identificador),
        "Método de pagamento excluído!",
        [id_pagamento]
    )


criar_botao(secao, "Cadastrar Método", cadastrar_pagamento)
criar_botao(secao, "Listar Métodos", listar_pagamentos)
criar_botao(secao, "Excluir Método", excluir_pagamento)


# ==================================================
# INFORMAÇÕES GERAIS
# ==================================================

secao = criar_secao("Informações Gerais da Loja")


def ver_informacoes():
    try:
        loja.ver_informacoes()
        messagebox.showinfo(
            "Informações",
            "Resumo exibido no terminal do VS Code."
        )
    except Exception as erro:
        messagebox.showerror("Erro", str(erro))


criar_botao(
    secao,
    "Ver Informações Gerais",
    ver_informacoes
)


# Rodapé
tk.Label(
    conteudo,
    text="Sistema de Crochê • Gerenciamento da loja",
    bg=COR_FUNDO,
    fg="white",
    pady=15
).pack(fill="x")


# Iniciar interface
janela.mainloop()


