import random
from cliente import Cliente
from conta import ContaCorrente, ContaPoupanca, ContaSalario, gerar_numero_conta
from database import salvar_cliente, atualizar_cliente, deletar_cliente, salvar_conta, atualizar_saldo_conta, salvar_transacao, carregar_dados


global clientes, contas
clientes = {}
contas = []


def listar_clientes():
    if not clientes:
        print("Nenhum cliente registrado.\n")
        return
    for cpf, cliente in clientes.items():
        print(f"CPF: {cpf} - Nome: {cliente.nome}")
    print()


def editar_cliente():
    cpf = input("Digite o CPF do cliente a ser editado: ")
    if cpf not in clientes:
        print("CPF não encontrado.\n")
        return
    cliente = clientes[cpf]
    novo_nome = input(f'Digite o novo nome para o cliente (atual: {cliente.nome}): ')
    cliente.nome = novo_nome
    atualizar_cliente(cliente)
    print(f'Cliente {cliente.nome} atualizado com sucesso.\n')


def excluir_cliente():
    cpf = input("Digite o CPF do cliente a ser excluído: ")
    if cpf not in clientes:
        print("CPF não encontrado.\n")
        return
    cliente = clientes.pop(cpf)
    deletar_cliente(cpf)
    print(f'Cliente {cliente.nome} excluído com sucesso.\n')


def criar_cliente():
    nome = input('Digite o nome do cliente: ')
    cpf = input('Digite o CPF do cliente: ')
    if cpf in clientes:
        print('Cliente já cadastrado com este CPF.\n')
        return
    cliente = Cliente(nome, cpf)
    clientes[cpf] = cliente
    salvar_cliente(cliente)
    print(f'Cliente {nome} criado com sucesso.\n')


def criar_conta():
    if not clientes:
        print("Nenhum cliente registrado. Por favor, crie um cliente primeiro.\n")
        return
    print("\nEscolha um cliente pelo CPF para criar uma conta:")
    for cpf, cliente in clientes.items():
        print(f"CPF: {cpf} - Nome: {cliente.nome}")
    cpf_escolhido = input("Digite o CPF do cliente: ")
    if cpf_escolhido not in clientes:
        print("CPF não encontrado. Por favor, verifique o CPF ou crie um cliente.\n")
        return
    cliente_selecionado = clientes[cpf_escolhido]

    print("\nEscolha o tipo de conta:")
    print("1 - Corrente")
    print("2 - Poupança")
    print("3 - Salário")
    tipo_conta = input("Digite o número do tipo de conta: ")

    if tipo_conta == '1':
        conta = ContaCorrente(cliente_selecionado, gerar_numero_conta())
    elif tipo_conta == '2':
        conta = ContaPoupanca(cliente_selecionado, gerar_numero_conta())
    elif tipo_conta == '3':
        conta = ContaSalario(cliente_selecionado, gerar_numero_conta())
    else:
        print("Tipo de conta inválido.\n")
        return

    contas.append(conta)
    salvar_conta(conta)
    print(f'Conta {conta.numero} criada para {cliente_selecionado.nome} com sucesso.\n')


def modificar_conta():
    cpf = input("Digite o CPF do cliente para modificar a conta: ")
    contas_cliente = [conta for conta in contas if conta.cliente.cpf == cpf]
    if not contas_cliente:
        print("Nenhuma conta encontrada para este CPF.\n")
        return
    for conta in contas_cliente:
        print(f"Conta: {conta.numero} - Tipo: {conta.tipo} - Saldo: {conta.saldo}")
    numero_conta = input("Digite o número da conta a ser modificada: ")
    conta_selecionada = next((conta for conta in contas_cliente if conta.numero == numero_conta), None)
    if not conta_selecionada:
        print("Conta não encontrada.\n")
        return

    print("\nEscolha a modificação:")
    print("1 - Mudar tipo de conta")
    print("2 - Gerar novo número de conta")
    opcao = input("Digite a opção: ")

    if opcao == '1':
        print("\nEscolha o novo tipo de conta:")
        print("1 - Corrente")
        print("2 - Poupança")
        print("3 - Salário")
        novo_tipo = input("Digite o número do novo tipo de conta: ")
        if novo_tipo == '1':
            nova_conta = ContaCorrente(conta_selecionada.cliente, conta_selecionada.numero, conta_selecionada.saldo)
        elif novo_tipo == '2':
            nova_conta = ContaPoupanca(conta_selecionada.cliente, conta_selecionada.numero, conta_selecionada.saldo)
        elif novo_tipo == '3':
            nova_conta = ContaSalario(conta_selecionada.cliente, conta_selecionada.numero, conta_selecionada.saldo)
        else:
            print("Tipo de conta inválido.\n")
            return
        contas.remove(conta_selecionada)
        contas.append(nova_conta)
        salvar_conta(nova_conta)
        print(f'Tipo de conta mudado para {nova_conta.tipo} com sucesso.\n')

    elif opcao == '2':
        novo_numero = gerar_numero_conta()
        conta_selecionada.numero = novo_numero
        salvar_conta(conta_selecionada)
        print(f'Número da conta alterado para {novo_numero} com sucesso.\n')


def operacoes_bancarias():
    if not contas:
        print("Nenhuma conta registrada. Por favor, crie uma conta primeiro.\n")
        return
    cpf = input("Digite o CPF do cliente para acessar a conta: ")
    contas_cliente = [conta for conta in contas if conta.cliente.cpf == cpf]
    if not contas_cliente:
        print("Nenhuma conta encontrada para este CPF.\n")
        return
    conta_selecionada = contas_cliente[0]  # Supondo apenas uma conta por CPF para simplificar

    while True:
        operacao = input('''
Escolha uma operação:
1 - Depositar
2 - Sacar
3 - Extrato
4 - Transferir
5 - Retornar ao menu anterior
''')
        if operacao == '1':
            valor = float(input('Digite o valor: '))
            print(conta_selecionada.depositar(valor))
            salvar_transacao(conta_selecionada.numero, "Depósito", valor)
            atualizar_saldo_conta(conta_selecionada)

        elif operacao == '2':
            valor = float(input('Digite o valor: '))
            print(conta_selecionada.sacar(valor))
            salvar_transacao(conta_selecionada.numero, "Saque", valor)
            atualizar_saldo_conta(conta_selecionada)

        elif operacao == '3':
            print(conta_selecionada.extrato())

        elif operacao == '4':
            cpf_destino = input("Digite o CPF do destinatário: ")
            contas_destino = [conta for conta in contas if conta.cliente.cpf == cpf_destino]
            if not contas_destino:
                print("Nenhuma conta encontrada para este CPF.\n")
                continue
            conta_destino = contas_destino[0]  # Supondo apenas uma conta por CPF para simplificar
            valor = float(input("Digite o valor: "))
            print(conta_selecionada.transferir(conta_destino, valor))
            salvar_transacao(conta_selecionada.numero, f"Transferência Enviada para {conta_destino.cliente.nome}",
                             valor)
            salvar_transacao(conta_destino.numero, f"Transferência Recebida de {conta_selecionada.cliente.nome}", valor)
            atualizar_saldo_conta(conta_selecionada)
            atualizar_saldo_conta(conta_destino)

        elif operacao == '5':
            break


if __name__ == '__main__':
    clientes, contas = carregar_dados()

    while True:
        opcao = input('''
1 - Criar Cliente
2 - Criar Conta
3 - Operações Bancárias
4 - Listar Clientes
5 - Editar Cliente
6 - Excluir Cliente
7 - Modificar Conta
8 - Sair
Escolha uma opção: ''')

        if opcao == '1':
            criar_cliente()

        elif opcao == '2':
            criar_conta()

        elif opcao == '3':
            operacoes_bancarias()

        elif opcao == '4':
            listar_clientes()

        elif opcao == '5':
            editar_cliente()

        elif opcao == '6':
            excluir_cliente()

        elif opcao == '7':
            modificar_conta()

        elif opcao == '8':
            print('Obrigado por usar nosso sistema bancário.')
            break
