
import mysql.connector


DB_CONFIG = {
    "host": "localhost",
    "port": 3307,
    "user": "root",
    "password": "senacrs",
    "database": "loja_kroche"
}


# ==========================================
# CONEXÃO COM O BANCO
# ==========================================

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


# ==========================================
# CRIAÇÃO DO BANCO E DAS TABELAS
# ==========================================

def criar_tabelas():

    # Cria o banco caso ainda não exista.
    config_sem_banco = DB_CONFIG.copy()
    config_sem_banco.pop("database")

    conn = mysql.connector.connect(**config_sem_banco)

    try:
        cursor = conn.cursor()

        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS loja_kroche"
        )

        cursor.close()

    finally:
        conn.close()

    # Conecta ao banco criado.
    conn = get_connection()

    try:
        cursor = conn.cursor()

        # ==========================================
        # TABELA KROCHE
        # ==========================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS kroche (
                id_kroche INT PRIMARY KEY AUTO_INCREMENT,
                nome VARCHAR(50) NOT NULL
            )
        """)

        # ==========================================
        # TABELA CLIENTES
        # ==========================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id_cliente INT PRIMARY KEY AUTO_INCREMENT,
                nome VARCHAR(100) NOT NULL,
                CPF VARCHAR(11) UNIQUE NOT NULL,
                numTelefone VARCHAR(15) NOT NULL
            )
        """)

        # ==========================================
        # TABELA VENDEDORES
        # ==========================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vendedores (
                id_vendedor INT PRIMARY KEY AUTO_INCREMENT,
                nome VARCHAR(100) NOT NULL,
                CPF VARCHAR(11) UNIQUE NOT NULL,
                numTelefone VARCHAR(15) NOT NULL
            )
        """)

        # ==========================================
        # TABELA PRODUTO
        # ==========================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produto (
                id_produto INT PRIMARY KEY AUTO_INCREMENT,
                nome VARCHAR(50) NOT NULL,
                preco DECIMAL(10,2) NOT NULL,
                quantidade INT NOT NULL,
                id_vendedor INT NULL
            )
        """)

        # ==========================================
        # TABELA METODO DE PAGAMENTO
        # ==========================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metodo_pagamento (
                id_pagamento INT PRIMARY KEY AUTO_INCREMENT,
                nome VARCHAR(50) NOT NULL,
                preco DECIMAL(10,2) NOT NULL,
                quantidade INT NOT NULL,
                historico VARCHAR(100) NOT NULL
            )
        """)

        # ==========================================
        # NOVA TABELA DE VENDAS
        # ==========================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vendas (

                id_venda INT PRIMARY KEY AUTO_INCREMENT,

                id_cliente INT NULL,
                nome_cliente VARCHAR(100) NOT NULL,

                id_produto INT NULL,
                nome_produto VARCHAR(100) NOT NULL,

                id_vendedor INT NULL,
                nome_vendedor VARCHAR(100),

                quantidade INT NOT NULL,

                preco_unitario DECIMAL(10,2) NOT NULL,

                valor_total DECIMAL(10,2) NOT NULL,

                data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            )
        """)

        conn.commit()

        print("Banco de dados e tabelas criados com sucesso!")

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()


# ==========================================
# PREPARAÇÃO DOS ACESSOS
# ==========================================

def preparar_acessos():

    conn = get_connection()

    try:
        cursor = conn.cursor()

        # Senha dos clientes
        cursor.execute(
            "SHOW COLUMNS FROM clientes LIKE 'senha_hash'"
        )

        if not cursor.fetchone():
            cursor.execute("""
                ALTER TABLE clientes
                ADD COLUMN senha_hash VARCHAR(255)
            """)

        # Senha dos vendedores
        cursor.execute(
            "SHOW COLUMNS FROM vendedores LIKE 'senha_hash'"
        )

        if not cursor.fetchone():
            cursor.execute("""
                ALTER TABLE vendedores
                ADD COLUMN senha_hash VARCHAR(255)
            """)

        # Identifica o vendedor responsável pelo produto
        cursor.execute(
            "SHOW COLUMNS FROM produto LIKE 'id_vendedor'"
        )

        if not cursor.fetchone():
            cursor.execute("""
                ALTER TABLE produto
                ADD COLUMN id_vendedor INT NULL
            """)

        conn.commit()

        print("Estrutura de acesso preparada!")

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()
