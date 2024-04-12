class Conta():
    def __init__(self, cliente, agencia, numero,limite, saldo=0):
        self.cliente = cliente
        self.agencia = agencia
        self.numero = numero
        self.limite = 0
        self.saldo = saldo

    def depositar(self, valor):
        self.saldo += valor
        return f' O saldo atual é {self.saldo}'

    def sacar(self, valor):
        if valor > self.saldo or valor <= 0:
            print('Você não pode realizar essa transação')
        else:
            self.saldo -= valor
            print(f' O saldo atual é {self.saldo}')

    def extrato(self):
        print( f' O saldo atual é {self.saldo}')