menu = """
### DIGITE A OPÇÃO DESEJADA ###

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

OPÇÃO: 

"""
saldo = 0
limite = 500
extrato = ''
numero_saque = 0
LIMITE_SAQUES = 3


while True:
    opcao = input(menu).lower().strip()

    if opcao == "d":
        deposito = float(input('Qual valor do deposito: '))
        saldo += deposito
        print(f'Deposito de R${deposito} realizado com sucesso')

    elif opcao == "s":
        if numero_saque < LIMITE_SAQUES:
            saque = float(input("Qual valor deseja sacar? "))
            if saque <= saldo and saque <= limite:
                print(f'Saque de R${saque} realizado com sucesso')
                numero_saque += 1
                saldo -= saque
            elif saque > limite:
                print(f'Você atingiu o limite de valor diário, valor diário máximo de {limite}')
            elif saque > saldo:
                print(f'Saldo insuficiente para saque, seu saldo atual é de R${saldo}')
        else:
            print(f'Limite de saque diário excedido, você já realizou {numero_saque} saques hoje')

    elif opcao == 'e':
        print(f"Seu saldo atual é de R$ {saldo}")

    elif opcao == "q":
        break

