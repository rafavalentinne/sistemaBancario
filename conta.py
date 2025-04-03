from datetime import datetime
import random

class Conta:
    def __init__(self, cliente, numero, tipo, limite, saldo=0):
        self.cliente = cliente
        self.agencia = "0001"
        self.numero = numero
        self.tipo = tipo
        self.limite = limite
        self.saldo = saldo
        self.transacoes = []
        self.limite_diario_saque = 1000
        self.limite_diario_deposito = 5000
        self.saque_diario = 0
        self.deposito_diario = 0
        self.ultima_atualizacao = datetime.now().date()

    def _atualizar_limites_diarios(self):
        hoje = datetime.now().date()
        if self.ultima_atualizacao != hoje:
            self.saque_diario = 0
            self.deposito_diario = 0
            self.ultima_atualizacao = hoje

    def depositar(self, valor):
        self._atualizar_limites_diarios()
        if self.deposito_diario + valor > self.limite_diario_deposito:
            return 'Você excedeu o limite diário de depósito'
        self.saldo += valor
        self.deposito_diario += valor
        self.transacoes.append((datetime.now(), "Depósito", valor))
        return f'O saldo atual é {self.saldo}'

    def sacar(self, valor):
        self._atualizar_limites_diarios()
        if valor > self.saldo or valor <= 0:
            return 'Você não pode realizar essa transação'
        if self.saque_diario + valor > self.limite_diario_saque:
            return 'Você excedeu o limite diário de saque'
        self.saldo -= valor
        self.saque_diario += valor
        self.transacoes.append((datetime.now(), "Saque", valor))
        return f'O saldo atual é {self.saldo}'

    def extrato(self):
        extrato = f'Extrato da Conta {self.numero}:\n'
        for transacao in self.transacoes:
            data = transacao[0].strftime('%d/%m/%Y %H:%M:%S')
            extrato += f'{data} - {transacao[1]}: {transacao[2]}\n'
        extrato += f'Saldo atual: {self.saldo}'
        return extrato

    def transferir(self, conta_destino, valor):
        self._atualizar_limites_diarios()
        if valor > self.saldo or valor <= 0:
            return 'Você não pode realizar essa transação'
        self.saldo -= valor
        conta_destino.saldo += valor
        self.transacoes.append((datetime.now(), f"Transferência Enviada para {conta_destino.cliente.nome}", valor))
        conta_destino.transacoes.append((datetime.now(), f"Transferência Recebida de {self.cliente.nome}", valor))
        return f'Transferência de {valor} para a conta {conta_destino.numero} realizada com sucesso'

class ContaCorrente(Conta):
    def __init__(self, cliente, numero, saldo=0):
        super().__init__(cliente, numero, "Corrente", limite=3000, saldo=saldo)

class ContaPoupanca(Conta):
    def __init__(self, cliente, numero, saldo=0):
        super().__init__(cliente, numero, "Poupança", limite=1000, saldo=saldo)

class ContaSalario(Conta):
    def __init__(self, cliente, numero, saldo=0):
        super().__init__(cliente, numero, "Salário", limite=0, saldo=saldo)

def gerar_numero_conta():
    conta = random.randint(10000, 99999)
    digito = random.randint(0, 9)
    return '{}-{}'.format(conta, digito)
