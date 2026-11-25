
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from decimal import Decimal
from banco import Kroche
import hashlib
import secrets

import mysql.connector

from database import get_connection, criar_tabelas, preparar_acessos


# ==================================================
# CONFIGURAÇÕES
# ==================================================

COR_FUNDO = "#586D4A"
COR_TITULO = "#22211F"
COR_BOTAO = "#48453D"
COR_TEXTO = "#FFFFFF"

# Preparação inicial do banco
criar_tabelas()
preparar_acessos()


# ==================================================
# FUNÇÕES DE SEGURANÇA
# ==================================================

def gerar_senha(senha):

    salt = secrets.token_hex(16)

    resultado = hashlib.pbkdf2_hmac(
        "sha256",
        senha.encode(),
        salt.encode(),
        200000
    )

    return salt + "$" + resultado.hex()


def verificar_senha(senha, senha_armazenada):

    try:
        salt, hash_original = senha_armazenada.split("$")

        resultado = hashlib.pbkdf2_hmac(
            "sha256",
            senha.encode(),
            salt.encode(),
            200000
        )

        return resultado.hex() == hash_original

    except (ValueError, AttributeError):
        return False


# ==================================================
# APLICAÇÃO
# ==================================================

class LojaKroche:

    def __init__(self, janela):

        self.janela = janela

        self.janela.title("Loja Krochê - Área do Usuário")
        self.janela.geometry("850x650")
        self.janela.minsize(700, 550)
        self.janela.configure(bg=COR_FUNDO)

        self.tipo_usuario = None
        self.id_usuario = None
        self.nome_usuario = None

        # Conexão com a classe de operações do banco
        self.loja = Kroche()

        self.mostrar_inicio()

    # ==================================================
    # FUNÇÕES GERAIS
    # ==================================================

    def limpar_tela(self):

        for widget in self.janela.winfo_children():
            widget.destroy()

    def conectar(self):
        return get_connection()

    def criar_titulo(self, texto):

        tk.Label(
            self.janela,
            text=texto,
            font=("Arial", 23, "bold"),
            bg=COR_FUNDO,
            fg=COR_TEXTO
        ).pack(pady=20)

    def criar_botao(self, texto, comando):

        return tk.Button(
            self.janela,
            text=texto,
            command=comando,
            font=("Arial", 11, "bold"),
            bg=COR_BOTAO,
            fg="white",
            activebackground="#686257",
            activeforeground="white",
            width=25,
            pady=8,
            cursor="hand2"
        )

    def criar_campo(self, texto, ocultar=False):

        tk.Label(
            self.janela,
            text=texto,
            font=("Arial", 11),
            bg=COR_FUNDO,
            fg="white"
        ).pack(pady=(8, 2))

        campo = tk.Entry(
            self.janela,
            font=("Arial", 12),
            width=32,
            show="*" if ocultar else ""
        )

        campo.pack()
        return campo

    # ==================================================
    # TELA INICIAL
    # ==================================================

    def mostrar_inicio(self):

        self.limpar_tela()

        self.tipo_usuario = None
        self.id_usuario = None
        self.nome_usuario = None

        self.criar_titulo("BEM-VINDO À LOJA KROCHÊ")

        tk.Label(
            self.janela,
            text="Escolha como deseja acessar:",
            font=("Arial", 14),
            bg=COR_FUNDO,
            fg="white"
        ).pack(pady=25)

        self.criar_botao(
            "ENTRAR COMO CLIENTE",
            lambda: self.tela_login("cliente")
        ).pack(pady=12)

        self.criar_botao(
            "ENTRAR COMO VENDEDOR",
            lambda: self.tela_login("vendedor")
        ).pack(pady=12)

        self.criar_botao(
            "SAIR",
            self.janela.destroy
        ).pack(pady=30)

    # ==================================================
    # LOGIN
    # ==================================================

    def tela_login(self, tipo):

        self.limpar_tela()

        self.tipo_usuario = tipo

        self.criar_titulo("LOGIN - " + tipo.upper())

        self.campo_nome = self.criar_campo("Nome")
        self.campo_senha = self.criar_campo(
            "Senha",
            ocultar=True
        )

        self.criar_botao(
            "ENTRAR",
            self.login
        ).pack(pady=20)

        self.criar_botao(
            "CRIAR CONTA",
            lambda: self.tela_cadastro(tipo)
        ).pack(pady=5)

        self.criar_botao(
            "VOLTAR",
            self.mostrar_inicio
        ).pack(pady=5)

    def login(self):

        nome = self.campo_nome.get().strip()
        senha = self.campo_senha.get()

        if not nome or not senha:

            messagebox.showwarning(
                "Atenção",
                "Preencha todos os campos."
            )
            return

        tabela = (
            "clientes"
            if self.tipo_usuario == "cliente"
            else "vendedores"
        )

        campo_id = (
            "id_cliente"
            if self.tipo_usuario == "cliente"
            else "id_vendedor"
        )

        conn = None
        cursor = None

        try:

            conn = self.conectar()
            cursor = conn.cursor()

            cursor.execute(
                f"""
                SELECT {campo_id}, nome, senha_hash
                FROM {tabela}
                WHERE nome = %s
                """,
                (nome,)
            )

            resultados = cursor.fetchall()

            if len(resultados) == 0:

                messagebox.showerror(
                    "Erro",
                    "Usuário não encontrado."
                )
                return

            if len(resultados) > 1:

                messagebox.showwarning(
                    "Atenção",
                    "Existem usuários com esse nome. "
                    "Entre em contato com o administrador."
                )
                return

            usuario_id, nome, senha_hash = resultados[0]

            if not verificar_senha(senha, senha_hash):

                messagebox.showerror(
                    "Erro",
                    "Senha incorreta."
                )
                return

            self.id_usuario = usuario_id
            self.nome_usuario = nome

            if self.tipo_usuario == "cliente":
                self.tela_cliente()
            else:
                self.tela_vendedor()

        except mysql.connector.Error as erro:

            messagebox.showerror(
                "Erro no banco de dados",
                str(erro)
            )

        finally:

            if cursor:
                cursor.close()

            if conn and conn.is_connected():
                conn.close()

    # ==================================================
    # CADASTRO
    # ==================================================

    def tela_cadastro(self, tipo):

        self.limpar_tela()

        self.criar_titulo("CRIAR CONTA - " + tipo.upper())

        self.campo_nome = self.criar_campo("Nome completo")
        self.campo_cpf = self.criar_campo("CPF (somente números)")
        self.campo_telefone = self.criar_campo("Telefone")
        self.campo_senha = self.criar_campo(
            "Criar senha",
            ocultar=True
        )

        self.criar_botao(
            "CADASTRAR",
            self.cadastrar
        ).pack(pady=20)

        self.criar_botao(
            "VOLTAR",
            lambda: self.tela_login(tipo)
        ).pack()

    def cadastrar(self):

        nome = self.campo_nome.get().strip()
        cpf = self.campo_cpf.get().strip()
        telefone = self.campo_telefone.get().strip()
        senha = self.campo_senha.get()

        if not all([nome, cpf, telefone, senha]):

            messagebox.showwarning(
                "Atenção",
                "Preencha todos os campos."
            )
            return

        if not cpf.isdigit() or len(cpf) != 11:

            messagebox.showwarning(
                "CPF inválido",
                "Digite um CPF com 11 números."
            )
            return

        if len(senha) < 6:

            messagebox.showwarning(
                "Senha inválida",
                "A senha precisa ter pelo menos 6 caracteres."
            )
            return

        tabela = (
            "clientes"
            if self.tipo_usuario == "cliente"
            else "vendedores"
        )

        senha_hash = gerar_senha(senha)

        conn = None
        cursor = None

        try:

            conn = self.conectar()
            cursor = conn.cursor()

            cursor.execute(
                f"""
                INSERT INTO {tabela}
                (nome, CPF, numTelefone, senha_hash)
                VALUES (%s, %s, %s, %s)
                """,
                (nome, cpf, telefone, senha_hash)
            )

            conn.commit()

            messagebox.showinfo(
                "Sucesso",
                "Conta criada com sucesso!"
            )

            self.tela_login(self.tipo_usuario)

        except mysql.connector.IntegrityError:

            messagebox.showerror(
                "Erro",
                "Esse CPF já está cadastrado."
            )

        except mysql.connector.Error as erro:

            if conn:
                conn.rollback()

            messagebox.showerror(
                "Erro",
                str(erro)
            )

        finally:

            if cursor:
                cursor.close()

            if conn and conn.is_connected():
                conn.close()

    # ==================================================
    # INTERFACE DO CLIENTE
    # ==================================================

    def tela_cliente(self):

        self.limpar_tela()

        self.criar_titulo("ÁREA DO CLIENTE")

        tk.Label(
            self.janela,
            text=f"Bem-vindo(a), {self.nome_usuario}!",
            font=("Arial", 13),
            bg=COR_FUNDO,
            fg="white"
        ).pack(pady=5)

        tk.Label(
            self.janela,
            text="Produtos disponíveis na loja:",
            font=("Arial", 12, "bold"),
            bg=COR_FUNDO,
            fg="white"
        ).pack(pady=10)

        self.tabela = ttk.Treeview(
            self.janela,
            columns=("produto", "preco", "vendedor", "quantidade"),
            show="headings",
            height=13
        )

        self.tabela.heading("produto", text="Produto")
        self.tabela.heading("preco", text="Preço")
        self.tabela.heading("vendedor", text="Vendedor")
        self.tabela.heading("quantidade", text="Quantidade")

        self.tabela.column("produto", width=210)
        self.tabela.column("preco", width=120)
        self.tabela.column("vendedor", width=200)
        self.tabela.column("quantidade", width=120)

        self.tabela.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=10
        )

        self.atualizar_produtos_cliente()

        self.criar_botao(
            "COMPRAR PRODUTO",
            self.comprar_produto
        ).pack(pady=5)

        self.criar_botao(
            "ATUALIZAR PRODUTOS",
            self.atualizar_produtos_cliente
        ).pack(pady=5)

        self.criar_botao(
            "EXCLUIR MINHA CONTA",
            self.excluir_conta
        ).pack(pady=5)

        self.criar_botao(
            "SAIR DA CONTA",
            self.mostrar_inicio
        ).pack(pady=5)

    # ==================================================
    # ATUALIZAR PRODUTOS DO CLIENTE
    # ==================================================

    def atualizar_produtos_cliente(self):

        for item in self.tabela.get_children():
            self.tabela.delete(item)

        conn = None
        cursor = None

        try:

            conn = self.conectar()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    p.id_produto,
                    p.nome,
                    p.preco,
                    COALESCE(v.nome, 'Loja'),
                    p.quantidade
                FROM produto p
                LEFT JOIN vendedores v
                    ON p.id_vendedor = v.id_vendedor
                ORDER BY p.nome
            """)

            for produto in cursor.fetchall():

                id_produto, nome, preco, vendedor, quantidade = produto

                self.tabela.insert(
                    "",
                    "end",
                    iid=str(id_produto),
                    values=(
                        nome,
                        f"R$ {float(preco):.2f}",
                        vendedor,
                        quantidade
                    )
                )

        except mysql.connector.Error as erro:

            messagebox.showerror(
                "Erro",
                str(erro)
            )

        finally:

            if cursor:
                cursor.close()

            if conn and conn.is_connected():
                conn.close()

    # ==================================================
    # COMPRAR PRODUTO
    # ==================================================

    def comprar_produto(self):

        selecionado = self.tabela.selection()

        if not selecionado:

            messagebox.showwarning(
                "Atenção",
                "Selecione um produto para comprar."
            )
            return

        # O ID do produto fica oculto no identificador da linha
        id_produto = int(selecionado[0])

        conn = None
        cursor = None

        try:

            conn = self.conectar()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT nome, preco, quantidade
                FROM produto
                WHERE id_produto = %s
            """, (id_produto,))

            dados = cursor.fetchone()

        except mysql.connector.Error as erro:

            messagebox.showerror(
                "Erro no banco de dados",
                str(erro)
            )
            return

        finally:

            if cursor:
                cursor.close()

            if conn and conn.is_connected():
                conn.close()

        if not dados:

            messagebox.showerror(
                "Erro",
                "Produto não encontrado."
            )

            self.atualizar_produtos_cliente()
            return

        nome_produto, preco, estoque = dados

        if estoque <= 0:

            messagebox.showwarning(
                "Estoque esgotado",
                "Esse produto não possui unidades disponíveis."
            )

            self.atualizar_produtos_cliente()
            return

        # Pergunta a quantidade desejada
        quantidade = simpledialog.askinteger(
            "Comprar produto",
            f"Produto: {nome_produto}\n"
            f"Estoque disponível: {estoque}\n\n"
            "Quantas unidades deseja comprar?",
            parent=self.janela,
            minvalue=1,
            maxvalue=estoque
        )

        if quantidade is None:
            return

        # Calcula o valor total
        preco_decimal = Decimal(str(preco))
        valor_total = preco_decimal * quantidade

        # Confirma a compra
        confirmar = messagebox.askyesno(
            "Confirmar compra",
            f"Produto: {nome_produto}\n"
            f"Quantidade: {quantidade}\n"
            f"Preço unitário: R$ {preco_decimal:.2f}\n"
            f"Valor total: R$ {valor_total:.2f}\n\n"
            "Deseja confirmar a compra?"
        )

        if not confirmar:
            return

        # Registra a compra no banco de dados
        try:

            resultado = self.loja.registrar_compra(
                self.id_usuario,
                id_produto,
                quantidade
            )

            # Atualiza o estoque na tela
            self.atualizar_produtos_cliente()

            # Exibe o comprovante da compra
            messagebox.showinfo(
                "Compra realizada!",
                f"Compra registrada com sucesso!\n\n"
                f"Número da venda: {resultado['id_venda']}\n"
                f"Cliente: {resultado['cliente']}\n"
                f"Produto: {resultado['produto']}\n"
                f"Vendedor: {resultado['vendedor'] or 'Loja'}\n"
                f"Quantidade: {resultado['quantidade']}\n"
                f"Preço unitário: R$ {resultado['preco_unitario']:.2f}\n"
                f"Valor total: R$ {resultado['valor_total']:.2f}"
            )

        except ValueError as erro:

            messagebox.showwarning(
                "Não foi possível comprar",
                str(erro)
            )

            self.atualizar_produtos_cliente()

        except mysql.connector.Error as erro:

            messagebox.showerror(
                "Erro no banco de dados",
                str(erro)
            )

            self.atualizar_produtos_cliente()

    # ==================================================
    # INTERFACE DO VENDEDOR
    # ==================================================

    def tela_vendedor(self):

        self.limpar_tela()

        self.criar_titulo("ÁREA DO VENDEDOR")

        tk.Label(
            self.janela,
            text=f"Bem-vindo(a), {self.nome_usuario}!",
            font=("Arial", 13),
            bg=COR_FUNDO,
            fg="white"
        ).pack(pady=5)

        self.tabela = ttk.Treeview(
            self.janela,
            columns=("id", "produto", "preco", "quantidade"),
            show="headings",
            height=12
        )

        self.tabela.heading("id", text="ID")
        self.tabela.heading("produto", text="Produto")
        self.tabela.heading("preco", text="Preço")
        self.tabela.heading("quantidade", text="Quantidade")

        self.tabela.column("id", width=60)
        self.tabela.column("produto", width=250)
        self.tabela.column("preco", width=120)
        self.tabela.column("quantidade", width=120)

        self.tabela.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=10
        )

        self.atualizar_produtos_vendedor()

        self.criar_botao(
            "CADASTRAR PRODUTO",
            self.cadastrar_produto
        ).pack(pady=4)

        self.criar_botao(
            "ALTERAR PREÇO",
            self.alterar_preco
        ).pack(pady=4)

        self.criar_botao(
            "EXCLUIR PRODUTO",
            self.excluir_produto
        ).pack(pady=4)

        self.criar_botao(
            "EXCLUIR MINHA CONTA",
            self.excluir_conta
        ).pack(pady=4)

        self.criar_botao(
            "SAIR DA CONTA",
            self.mostrar_inicio
        ).pack(pady=4)

    # ==================================================
    # ATUALIZAR PRODUTOS DO VENDEDOR
    # ==================================================

    def atualizar_produtos_vendedor(self):

        for item in self.tabela.get_children():
            self.tabela.delete(item)

        conn = None
        cursor = None

        try:

            conn = self.conectar()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id_produto, nome, preco, quantidade
                FROM produto
                WHERE id_vendedor = %s
                ORDER BY nome
            """, (self.id_usuario,))

            for produto in cursor.fetchall():

                self.tabela.insert(
                    "",
                    "end",
                    values=(
                        produto[0],
                        produto[1],
                        f"R$ {float(produto[2]):.2f}",
                        produto[3]
                    )
                )

        except mysql.connector.Error as erro:

            messagebox.showerror(
                "Erro",
                str(erro)
            )

        finally:

            if cursor:
                cursor.close()

            if conn and conn.is_connected():
                conn.close()

    # ==================================================
    # CADASTRAR PRODUTO
    # ==================================================

    def cadastrar_produto(self):

        janela = tk.Toplevel(self.janela)
        janela.title("Cadastrar produto")
        janela.geometry("350x350")
        janela.configure(bg=COR_FUNDO)
        janela.transient(self.janela)
        janela.grab_set()

        def campo(texto):

            tk.Label(
                janela,
                text=texto,
                bg=COR_FUNDO,
                fg="white"
            ).pack(pady=(10, 2))

            entrada = tk.Entry(
                janela,
                font=("Arial", 11)
            )

            entrada.pack()
            return entrada

        nome = campo("Nome do produto")
        preco = campo("Preço")
        quantidade = campo("Quantidade")

        def salvar():

            nome_produto = nome.get().strip()

            try:

                valor = float(preco.get().replace(",", "."))
                estoque = int(quantidade.get())

                if not nome_produto or valor <= 0 or estoque < 0:
                    raise ValueError

            except ValueError:

                messagebox.showwarning(
                    "Atenção",
                    "Informe um nome, preço positivo e quantidade válida."
                )
                return

            conn = None
            cursor = None

            try:

                conn = self.conectar()
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO produto
                    (nome, preco, quantidade, id_vendedor)
                    VALUES (%s, %s, %s, %s)
                """, (
                    nome_produto,
                    valor,
                    estoque,
                    self.id_usuario
                ))

                conn.commit()

                janela.destroy()

                self.atualizar_produtos_vendedor()

                messagebox.showinfo(
                    "Sucesso",
                    "Produto cadastrado!"
                )

            except mysql.connector.Error as erro:

                if conn:
                    conn.rollback()

                messagebox.showerror(
                    "Erro",
                    str(erro)
                )

            finally:

                if cursor:
                    cursor.close()

                if conn and conn.is_connected():
                    conn.close()

        tk.Button(
            janela,
            text="SALVAR PRODUTO",
            command=salvar,
            bg=COR_BOTAO,
            fg="white",
            width=22,
            pady=8
        ).pack(pady=20)

    # ==================================================
    # ALTERAR PREÇO
    # ==================================================

    def alterar_preco(self):

        selecionado = self.tabela.selection()

        if not selecionado:

            messagebox.showwarning(
                "Atenção",
                "Selecione um produto."
            )
            return

        dados = self.tabela.item(
            selecionado[0],
            "values"
        )

        id_produto = dados[0]

        janela = tk.Toplevel(self.janela)
        janela.title("Alterar preço")
        janela.geometry("300x200")
        janela.configure(bg=COR_FUNDO)
        janela.transient(self.janela)
        janela.grab_set()

        tk.Label(
            janela,
            text=f"Produto: {dados[1]}",
            bg=COR_FUNDO,
            fg="white"
        ).pack(pady=15)

        tk.Label(
            janela,
            text="Novo preço:",
            bg=COR_FUNDO,
            fg="white"
        ).pack()

        entrada = tk.Entry(janela)
        entrada.pack(pady=5)

        def salvar():

            try:

                valor = float(
                    entrada.get().replace(",", ".")
                )

                if valor <= 0:
                    raise ValueError

            except ValueError:

                messagebox.showwarning(
                    "Atenção",
                    "Digite um preço válido."
                )
                return

            conn = None
            cursor = None

            try:

                conn = self.conectar()
                cursor = conn.cursor()

                cursor.execute("""
                    UPDATE produto
                    SET preco = %s
                    WHERE id_produto = %s
                    AND id_vendedor = %s
                """, (
                    valor,
                    id_produto,
                    self.id_usuario
                ))

                conn.commit()

                janela.destroy()

                self.atualizar_produtos_vendedor()

                messagebox.showinfo(
                    "Sucesso",
                    "Preço atualizado!"
                )

            except mysql.connector.Error as erro:

                if conn:
                    conn.rollback()

                messagebox.showerror(
                    "Erro",
                    str(erro)
                )

            finally:

                if cursor:
                    cursor.close()

                if conn and conn.is_connected():
                    conn.close()

        tk.Button(
            janela,
            text="SALVAR",
            command=salvar,
            bg=COR_BOTAO,
            fg="white",
            width=22,
            pady=8
        ).pack(pady=15)

    # ==================================================
    # EXCLUIR PRODUTO
    # ==================================================

    def excluir_produto(self):

        selecionado = self.tabela.selection()

        if not selecionado:

            messagebox.showwarning(
                "Atenção",
                "Selecione um produto."
            )
            return

        dados = self.tabela.item(
            selecionado[0],
            "values"
        )

        id_produto = dados[0]

        confirmar = messagebox.askyesno(
            "Confirmar",
            f"Deseja excluir o produto {dados[1]}?"
        )

        if not confirmar:
            return

        conn = None
        cursor = None

        try:

            conn = self.conectar()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM produto
                WHERE id_produto = %s
                AND id_vendedor = %s
            """, (
                id_produto,
                self.id_usuario
            ))

            conn.commit()

            self.atualizar_produtos_vendedor()

            messagebox.showinfo(
                "Sucesso",
                "Produto excluído!"
            )

        except mysql.connector.Error as erro:

            if conn:
                conn.rollback()

            messagebox.showerror(
                "Erro",
                str(erro)
            )

        finally:

            if cursor:
                cursor.close()

            if conn and conn.is_connected():
                conn.close()

    # ==================================================
    # EXCLUIR CONTA
    # ==================================================

    def excluir_conta(self):

        confirmar = messagebox.askyesno(
            "Excluir conta",
            "Tem certeza que deseja excluir sua conta?"
        )

        if not confirmar:
            return

        tabela = (
            "clientes"
            if self.tipo_usuario == "cliente"
            else "vendedores"
        )

        campo_id = (
            "id_cliente"
            if self.tipo_usuario == "cliente"
            else "id_vendedor"
        )

        conn = None
        cursor = None

        try:

            conn = self.conectar()
            cursor = conn.cursor()

            if self.tipo_usuario == "vendedor":

                # Os produtos permanecem na loja,
                # mas deixam de pertencer ao vendedor.
                cursor.execute("""
                    UPDATE produto
                    SET id_vendedor = NULL
                    WHERE id_vendedor = %s
                """, (self.id_usuario,))

            cursor.execute(
                f"DELETE FROM {tabela} WHERE {campo_id} = %s",
                (self.id_usuario,)
            )

            conn.commit()

            self.id_usuario = None
            self.nome_usuario = None

            messagebox.showinfo(
                "Sucesso",
                "Sua conta foi excluída."
            )

            self.mostrar_inicio()

        except mysql.connector.Error as erro:

            if conn:
                conn.rollback()

            messagebox.showerror(
                "Erro",
                str(erro)
            )

        finally:

            if cursor:
                cursor.close()

            if conn and conn.is_connected():
                conn.close()


# ==================================================
# INICIAR PROGRAMA
# ==================================================

if __name__ == "__main__":

    janela = tk.Tk()

    app = LojaKroche(janela)

    janela.mainloop()
