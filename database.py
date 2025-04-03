from datetime import datetime
from cliente import Cliente
from conta import ContaCorrente, ContaPoupanca, ContaSalario

def salvar_cliente(cliente):
    with open('clientes.txt', 'a') as file:
        file.write(f"{cliente.cpf},{cliente.nome}\n")

def atualizar_cliente(cliente):
    with open('clientes.txt', 'r') as file:
        linhas = file.readlines()
    with open('clientes.txt', 'w') as file:
        for linha in linhas:
            cpf, nome = linha.strip().split(',')
            if cpf == cliente.cpf:
                linha = f"{cliente.cpf},{cliente.nome}\n"
            file.write(linha)

def deletar_cliente(cpf):
    with open('clientes.txt', 'r') as file:
        linhas = file.readlines()
    with open('clientes.txt', 'w') as file:
        for linha in linhas:
            if cpf not in linha:
                file.write(linha)
    with open('contas.txt', 'r') as file:
        contas = file.readlines()
    with open('contas.txt', 'w') as file:
        for conta in contas:
            if cpf not in conta:
                file.write(conta)
    with open('transacoes.txt', 'r') as file:
        transacoes = file.readlines()
    with open('transacoes.txt', 'w') as file:
        for transacao in transacoes:
            numero_conta = transacao.split(',')[0]
            if not any(cpf in conta for conta in contas if conta.startswith(numero_conta)):
                file.write(transacao)

def salvar_conta(conta):
    with open('contas.txt', 'a') as file:
        file.write(f"{conta.numero},{conta.cliente.cpf},{conta.tipo},{conta.saldo},{conta.limite}\n")

def atualizar_saldo_conta(conta):
    with open('contas.txt', 'r') as file:
        linhas = file.readlines()
    with open('contas.txt', 'w') as file:
        for linha in linhas:
            numero, cpf_cliente, tipo, saldo, limite = linha.strip().split(',')
            if numero == conta.numero:
                linha = f"{numero},{cpf_cliente},{tipo},{conta.saldo},{limite}\n"
            file.write(linha)

def salvar_transacao(numero_conta, tipo, valor):
    data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('transacoes.txt', 'a') as file:
        file.write(f"{numero_conta},{data},{tipo},{valor}\n")

def carregar_dados():
    clientes = {}
    with open('clientes.txt', 'r') as file:
        for linha in file:
            cpf, nome = linha.strip().split(',')
            clientes[cpf] = Cliente(nome, cpf)

    contas = []
    with open('contas.txt', 'r') as file:
        for linha in file:
            numero, cpf_cliente, tipo, saldo, limite = linha.strip().split(',')
            cliente = clientes[cpf_cliente]
            if tipo == 'Corrente':
                conta = ContaCorrente(cliente, numero, saldo)
            elif tipo == 'Poupança':
                conta = ContaPoupanca(cliente, numero, saldo)
            elif tipo == 'Salário':
                conta = ContaSalario(cliente, numero, saldo)
            contas.append(conta)

    with open('transacoes.txt', 'r') as file:
        for linha in file:
            numero_conta, data, tipo, valor = linha.strip().split(',')
            conta = next((c for c in contas if c.numero == numero_conta), None)
            if conta:
                conta.transacoes.append((datetime.strptime(data, '%Y-%m-%d %H:%M:%S'), tipo, valor))

    return clientes, contas
