from sistemaBancario.conta import Conta
from sistemaBancario.cliente import Cliente

clientes = {}
contas = []

def criar_cliente():
    nome = input('Digite o nome do cliente: ')
    cpf = input('Digite o CPF do cliente: ')
    if cpf in clientes:
        print('Cliente já cadastrado com este CPF.\n')
        return
    cliente = Cliente(nome, cpf)
    clientes[cpf] = cliente
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
    agencia = input('Digite a agência: ')
    numero = input('Digite o número da conta: ')
    conta = Conta(cliente_selecionado, agencia, numero, limite=3000)
    contas.append(conta)
    print(f'Conta {numero} criada para {cliente_selecionado.nome} com sucesso.\n')


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
4 - Retornar ao menu anterior
''')
        if operacao == '1':
            depositar = float(input('Digite o valor: '))
            conta_selecionada.depositar(depositar)

        elif operacao == '2':
            saque = float(input('Digite o valor: '))
            conta_selecionada.sacar(saque)

        elif operacao == '3':
            conta_selecionada.extrato()

        elif operacao == '4':
            break

while True:
    opcao = input('''
1 - Criar Cliente
2 - Criar Conta
3 - Operações Bancárias
4 - Sair
Escolha uma opção: ''')

    if opcao == '1':
        criar_cliente()

    elif opcao == '2':
        criar_conta()

    elif opcao == '3':
        operacoes_bancarias()

    elif opcao == '4':
        print('Obrigado por usar nosso sistema bancário.')
        break
