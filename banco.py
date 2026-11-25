
from database import get_connection
from decimal import Decimal

class Kroche:

    # ==========================================
    # FUNÇÕES AUXILIARES
    # ==========================================

    def executar(self, sql, valores=()):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(sql, valores)
            conn.commit()
            return cursor.rowcount

        except Exception:
            conn.rollback()
            raise

        finally:
            cursor.close()
            conn.close()

    def consultar(self, sql, valores=()):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(sql, valores)
            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()

    # ==========================================
    # CROCHÊ
    # ==========================================

    def cadastrar_kroche(self, nome):

        self.executar(
            "INSERT INTO kroche (nome) VALUES (%s)",
            (nome,)
        )

        print("Crochê cadastrado com sucesso!")
        return True

    def listar_kroche(self):

        dados = self.consultar(
            "SELECT * FROM kroche"
        )

        for item in dados:
            print(item)

        return dados

    # ==========================================
    # CLIENTES
    # ==========================================

    def cadastrar_cliente(self, nome, cpf, telefone):

        if self.consultar(
            "SELECT 1 FROM clientes WHERE CPF = %s",
            (cpf,)
        ):
            print("Já existe um cliente com esse CPF.")
            return False

        self.executar(
            """
            INSERT INTO clientes (nome, CPF, numTelefone)
            VALUES (%s, %s, %s)
            """,
            (nome, cpf, telefone)
        )

        print("Cliente cadastrado com sucesso!")
        return True

    def listar_clientes(self):

        dados = self.consultar(
            "SELECT * FROM clientes"
        )

        for cliente in dados:
            print(cliente)

        return dados

    def buscar_cliente(self, cpf):

        resultado = self.consultar(
            "SELECT * FROM clientes WHERE CPF = %s",
            (cpf,)
        )

        if resultado:
            return resultado[0]

        print("Cliente não encontrado.")
        return None

    def excluir_cliente(self, id_cliente):

        resultado = self.executar(
            "DELETE FROM clientes WHERE id_cliente = %s",
            (id_cliente,)
        )

        if resultado:
            print("Cliente excluído com sucesso!")
            return True

        print("Cliente não encontrado.")
        return False

    # ==========================================
    # VENDEDORES
    # ==========================================

    def cadastrar_vendedor(self, nome, cpf, telefone):

        if self.consultar(
            "SELECT 1 FROM vendedores WHERE CPF = %s",
            (cpf,)
        ):
            print("Já existe um vendedor com esse CPF.")
            return False

        self.executar(
            """
            INSERT INTO vendedores (nome, CPF, numTelefone)
            VALUES (%s, %s, %s)
            """,
            (nome, cpf, telefone)
        )

        print("Vendedor cadastrado com sucesso!")
        return True

    def listar_vendedores(self):

        dados = self.consultar(
            "SELECT * FROM vendedores"
        )

        for vendedor in dados:
            print(vendedor)

        return dados

    def excluir_vendedor(self, id_vendedor):

        resultado = self.executar(
            "DELETE FROM vendedores WHERE id_vendedor = %s",
            (id_vendedor,)
        )

        if resultado:
            print("Vendedor excluído com sucesso!")
            return True

        print("Vendedor não encontrado.")
        return False

    # ==========================================
    # PRODUTOS
    # ==========================================

    def cadastrar_produto(self, nome, preco, quantidade):

        if preco < 0 or quantidade < 0:
            print("Preço ou quantidade inválidos.")
            return False

        self.executar(
            """
            INSERT INTO produto (nome, preco, quantidade)
            VALUES (%s, %s, %s)
            """,
            (nome, preco, quantidade)
        )

        print("Produto cadastrado com sucesso!")
        return True

    def listar_produtos(self):

        dados = self.consultar(
            "SELECT * FROM produto"
        )

        for produto in dados:
            print(produto)

        return dados

    def buscar_produto(self, id_produto):

        resultado = self.consultar(
            "SELECT * FROM produto WHERE id_produto = %s",
            (id_produto,)
        )

        if resultado:
            return resultado[0]

        print("Produto não encontrado.")
        return None

    def atualizar_estoque(self, id_produto, quantidade):

        if quantidade < 0:
            print("Quantidade inválida.")
            return False

        resultado = self.executar(
            """
            UPDATE produto
            SET quantidade = %s
            WHERE id_produto = %s
            """,
            (quantidade, id_produto)
        )

        if resultado:
            print("Estoque atualizado com sucesso!")
            return True

        print("Produto não encontrado ou estoque já possui essa quantidade.")
        return False

    def excluir_produto(self, id_produto):

        resultado = self.executar(
            "DELETE FROM produto WHERE id_produto = %s",
            (id_produto,)
        )

        if resultado:
            print("Produto excluído com sucesso!")
            return True

        print("Produto não encontrado.")
        return False

    # ==========================================
    # MÉTODOS DE PAGAMENTO
    # ==========================================

    def cadastrar_pagamento(
        self, nome, preco, quantidade, historico
    ):

        if preco < 0 or quantidade < 0:
            print("Dados de pagamento inválidos.")
            return False

        self.executar(
            """
            INSERT INTO metodo_pagamento
            (nome, preco, quantidade, historico)
            VALUES (%s, %s, %s, %s)
            """,
            (nome, preco, quantidade, historico)
        )

        print("Método de pagamento cadastrado!")
        return True

    def listar_pagamentos(self):

        dados = self.consultar(
            "SELECT * FROM metodo_pagamento"
        )

        for pagamento in dados:
            print(pagamento)

        return dados

    def excluir_pagamento(self, id_pagamento):

        resultado = self.executar(
            """
            DELETE FROM metodo_pagamento
            WHERE id_pagamento = %s
            """,
            (id_pagamento,)
        )

        if resultado:
            print("Pagamento excluído com sucesso!")
            return True

        print("Pagamento não encontrado.")
        return False

    # ==========================================
    # CONSULTAS GERAIS
    # ==========================================

    def ver_informacoes(self):

        tabelas = [
            ("Clientes", "clientes"),
            ("Vendedores", "vendedores"),
            ("Produtos", "produto"),
            ("Métodos de pagamento", "metodo_pagamento"),
            ("Crochês", "kroche")
        ]

        print("\n===== INFORMAÇÕES DA LOJA =====")

        for nome, tabela in tabelas:

            resultado = self.consultar(
                f"SELECT COUNT(*) FROM {tabela}"
            )

            print(f"{nome}: {resultado[0][0]}")

        print("===============================")

    
    # ==========================================
    # REGISTRAR COMPRA DO CLIENTE
    # ==========================================

    def registrar_compra(self, id_cliente, id_produto, quantidade):

        if not isinstance(quantidade, int) or isinstance(quantidade, bool) or quantidade <= 0:
            raise ValueError("Quantidade inválida.")

        conn = get_connection()
        cursor = conn.cursor()

        try:
            # Localiza o produto e bloqueia sua linha
            # enquanto a compra está sendo processada.

            cursor.execute("""
                SELECT
                    p.nome,
                    p.preco,
                    p.quantidade,
                    p.id_vendedor,
                    v.nome
                FROM produto p
                LEFT JOIN vendedores v
                    ON p.id_vendedor = v.id_vendedor
                WHERE p.id_produto = %s
                FOR UPDATE
            """, (id_produto,))

            produto = cursor.fetchone()

            if not produto:
                raise ValueError("Produto não encontrado.")

            nome_produto, preco, estoque, id_vendedor, nome_vendedor = produto

            # Verifica o estoque disponível.

            if quantidade > estoque:
                raise ValueError(
                    f"Estoque insuficiente! Disponível: {estoque}"
                )

            # Localiza o cliente.

            cursor.execute("""
                SELECT nome
                FROM clientes
                WHERE id_cliente = %s
            """, (id_cliente,))

            cliente = cursor.fetchone()

            if not cliente:
                raise ValueError("Cliente não encontrado.")

            nome_cliente = cliente[0]

            # Calcula o valor total.

            preco_unitario = Decimal(str(preco))
            valor_total = (preco_unitario * quantidade).quantize(
                Decimal("0.01")
            )

            # Registra a venda.

            cursor.execute("""
                INSERT INTO vendas (
                    id_cliente,
                    nome_cliente,
                    id_produto,
                    nome_produto,
                    id_vendedor,
                    nome_vendedor,
                    quantidade,
                    preco_unitario,
                    valor_total
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                id_cliente,
                nome_cliente,
                id_produto,
                nome_produto,
                id_vendedor,
                nome_vendedor,
                quantidade,
                preco_unitario,
                valor_total
            ))

            id_venda = cursor.lastrowid

            # Atualiza o estoque.

            cursor.execute("""
                UPDATE produto
                SET quantidade = quantidade - %s
                WHERE id_produto = %s
            """, (quantidade, id_produto))

            conn.commit()

            return {
                "id_venda": id_venda,
                "cliente": nome_cliente,
                "produto": nome_produto,
                "vendedor": nome_vendedor,
                "quantidade": quantidade,
                "preco_unitario": preco_unitario,
                "valor_total": valor_total
            }

        except Exception:
            conn.rollback()
            raise

        finally:
            cursor.close()
            conn.close()
