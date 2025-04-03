import sqlite3
from datetime import datetime
from cliente import Cliente
from conta import ContaCorrente, ContaPoupanca, ContaSalario

def conectar():
    return sqlite3.connect('banco.db')

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            cpf TEXT PRIMARY KEY,
            nome TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contas (
            numero TEXT PRIMARY KEY,
            cpf_cliente TEXT,
            tipo TEXT,
            saldo REAL,
            limite REAL,
            FOREIGN KEY (cpf_cliente) REFERENCES clientes (cpf)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_conta TEXT,
            data TEXT,
            tipo TEXT,
            valor REAL,
            FOREIGN KEY (numero_conta) REFERENCES contas (numero)
        )
    ''')
    conn.commit()
    conn.close()

def salvar_cliente(cliente):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO clientes (cpf, nome) VALUES (?, ?)', (cliente.cpf, cliente.nome))
    conn.commit()
    conn.close()

def atualizar_cliente(cliente):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('UPDATE clientes SET nome = ? WHERE cpf = ?', (cliente.nome, cliente.cpf))
    conn.commit()
    conn.close()

def deletar_cliente(cpf):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM clientes WHERE cpf = ?', (cpf,))
    cursor.execute('DELETE FROM contas WHERE cpf_cliente = ?', (cpf,))
    cursor.execute('DELETE FROM transacoes WHERE numero_conta IN (SELECT numero FROM contas WHERE cpf_cliente = ?)', (cpf,))
    conn.commit()
    conn.close()

def salvar_conta(conta):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO contas (numero, cpf_cliente, tipo, saldo, limite) VALUES (?, ?, ?, ?, ?)
    ''', (conta.numero, conta.cliente.cpf, conta.tipo, conta.saldo, conta.limite))
    conn.commit()
    conn.close()

def atualizar_saldo_conta(conta):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE contas SET saldo = ? WHERE numero = ?
    ''', (conta.saldo, conta.numero))
    conn.commit()
    conn.close()

def salvar_transacao(numero_conta, tipo, valor):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transacoes (numero_conta, data, tipo, valor) VALUES (?, ?, ?, ?)
    ''', (numero_conta, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), tipo, valor))
    conn.commit()
    conn.close()

def carregar_dados():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM clientes')
    clientes = {}
    for row in cursor.fetchall():
        cpf, nome = row
        clientes[cpf] = Cliente(nome, cpf)

    cursor.execute('SELECT * FROM contas')
    contas = []
    for row in cursor.fetchall():
        numero, cpf_cliente, tipo, saldo, limite = row
        cliente = clientes[cpf_cliente]
        if tipo == 'Corrente':
            conta = ContaCorrente(cliente, numero, saldo)
        elif tipo == 'Poupança':
            conta = ContaPoupanca(cliente, numero, saldo)
        elif tipo == 'Salário':
            conta = ContaSalario(cliente, numero, saldo)
        contas.append(conta)

    cursor.execute('SELECT * FROM transacoes')
    for row in cursor.fetchall():
        numero_conta, data, tipo, valor = row[1], row[2], row[3], row[4]
        conta = next((conta for conta in contas if conta.numero == numero_conta), None)
        if conta:
            conta.transacoes.append((datetime.strptime(data, '%Y-%m-%d %H:%M:%S'), tipo, valor))

    conn.close()
    return clientes, contas
