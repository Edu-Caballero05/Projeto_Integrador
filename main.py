
from database import criar_tabelas
from banco import Kroche


# ==========================================
# MENU PRINCIPAL
# ==========================================

def menu():

    print("""
========================================
       SISTEMA DE GERENCIAMENTO
              DE CROCHÊ
========================================

1 - Cadastrar crochê
2 - Listar crochês

3 - Cadastrar cliente
4 - Listar clientes
5 - Buscar cliente
6 - Excluir cliente

7 - Cadastrar vendedor
8 - Listar vendedores
9 - Excluir vendedor

10 - Cadastrar produto
11 - Listar produtos
12 - Buscar produto
13 - Atualizar estoque
14 - Excluir produto

15 - Cadastrar método de pagamento
16 - Listar métodos de pagamento
17 - Excluir método de pagamento

18 - Informações gerais da loja

0 - Finalizar programa

========================================
""")

    try:
        return int(input("Digite uma opção: "))

    except ValueError:
        print("Digite apenas números!")
        return -1


# ==========================================
# INICIALIZAÇÃO DO SISTEMA
# ==========================================

criar_tabelas()

loja = Kroche()


# ==========================================
# LOOP PRINCIPAL
# ==========================================

while True:

    opcao = menu()

    # ==========================================
    # FINALIZAR PROGRAMA
    # ==========================================

    if opcao == 0:

        print("Programa finalizado. Até mais!")
        break

    # ==========================================
    # CROCHÊ
    # ==========================================

    elif opcao == 1:

        nome = input("Digite o nome do crochê: ")

        loja.cadastrar_kroche(nome)

    elif opcao == 2:

        loja.listar_kroche()

    # ==========================================
    # CLIENTES
    # ==========================================

    elif opcao == 3:

        nome = input("Digite o nome do cliente: ")
        cpf = input("Digite o CPF do cliente: ")
        telefone = input("Digite o telefone do cliente: ")

        loja.cadastrar_cliente(nome, cpf, telefone)

    elif opcao == 4:

        loja.listar_clientes()

    elif opcao == 5:

        cpf = input("Digite o CPF do cliente: ")

        cliente = loja.buscar_cliente(cpf)

        if cliente:
            print("Cliente encontrado:")
            print(cliente)

    elif opcao == 6:

        id_cliente = int(input("Digite o ID do cliente: "))

        loja.excluir_cliente(id_cliente)

    # ==========================================
    # VENDEDORES
    # ==========================================

    elif opcao == 7:

        nome = input("Digite o nome do vendedor: ")
        cpf = input("Digite o CPF do vendedor: ")
        telefone = input("Digite o telefone do vendedor: ")

        loja.cadastrar_vendedor(nome, cpf, telefone)

    elif opcao == 8:

        loja.listar_vendedores()

    elif opcao == 9:

        id_vendedor = int(input("Digite o ID do vendedor: "))

        loja.excluir_vendedor(id_vendedor)

    # ==========================================
    # PRODUTOS
    # ==========================================

    elif opcao == 10:

        nome = input("Digite o nome do produto: ")
        preco = float(input("Digite o preço do produto: "))
        quantidade = int(input("Digite a quantidade em estoque: "))

        loja.cadastrar_produto(nome, preco, quantidade)

    elif opcao == 11:

        loja.listar_produtos()

    elif opcao == 12:

        id_produto = int(input("Digite o ID do produto: "))

        produto = loja.buscar_produto(id_produto)

        if produto:
            print("Produto encontrado:")
            print(produto)

    elif opcao == 13:

        id_produto = int(input("Digite o ID do produto: "))
        quantidade = int(input("Digite a nova quantidade em estoque: "))

        loja.atualizar_estoque(id_produto, quantidade)

    elif opcao == 14:

        id_produto = int(input("Digite o ID do produto: "))

        loja.excluir_produto(id_produto)

    # ==========================================
    # MÉTODOS DE PAGAMENTO
    # ==========================================

    elif opcao == 15:

        nome = input("Digite o método de pagamento: ")
        preco = float(input("Digite o valor do pagamento: "))
        quantidade = int(input("Digite a quantidade: "))
        historico = input("Digite o histórico do pagamento: ")

        loja.cadastrar_pagamento(
            nome,
            preco,
            quantidade,
            historico
        )

    elif opcao == 16:

        loja.listar_pagamentos()

    elif opcao == 17:

        id_pagamento = int(input("Digite o ID do pagamento: "))

        loja.excluir_pagamento(id_pagamento)

    # ==========================================
    # INFORMAÇÕES GERAIS
    # ==========================================

    elif opcao == 18:

        loja.ver_informacoes()

    else:

        print("Opção inválida! Tente novamente.")
