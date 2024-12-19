import sqlite3
from datetime import datetime

# Função para criar o banco de dados e as tabelas
def criar_banco():
    conn = sqlite3.connect('motofrete.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        endereco TEXT NOT NULL,
        telefone TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS entregadores (
        id INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        placa TEXT NOT NULL,
        disponibilidade BOOLEAN NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY,
        cliente_id INTEGER,
        entregador_id INTEGER,
        origem TEXT NOT NULL,
        destino TEXT NOT NULL,
        status TEXT NOT NULL,
        data_criacao TEXT,
        FOREIGN KEY (cliente_id) REFERENCES clientes(id),
        FOREIGN KEY (entregador_id) REFERENCES entregadores(id)
    )
    ''')

    conn.commit()
    conn.close()

# Função para cadastrar um cliente
def cadastrar_cliente():
    nome = input("Digite o nome do cliente: ")
    endereco = input("Digite o endereço do cliente: ")
    telefone = input("Digite o telefone do cliente: ")

    conn = sqlite3.connect('motofrete.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO clientes (nome, endereco, telefone)
    VALUES (?, ?, ?)
    ''', (nome, endereco, telefone))

    conn.commit()
    conn.close()
    print("Cliente cadastrado com sucesso!")

# Função para cadastrar um entregador
def cadastrar_entregador():
    nome = input("Digite o nome do entregador: ")
    placa = input("Digite a placa da moto: ")
    disponibilidade = input("O entregador está disponível? (sim/não): ").lower() == 'sim'

    conn = sqlite3.connect('motofrete.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO entregadores (nome, placa, disponibilidade)
    VALUES (?, ?, ?)
    ''', (nome, placa, disponibilidade))

    conn.commit()
    conn.close()
    print("Entregador cadastrado com sucesso!")

# Função para cadastrar um pedido
def cadastrar_pedido():
    cliente_id = int(input("Digite o ID do cliente: "))
    entregador_id = int(input("Digite o ID do entregador: "))
    origem = input("Digite o local de origem: ")
    destino = input("Digite o local de destino: ")

    # Verificar se o entregador está disponível
    conn = sqlite3.connect('motofrete.db')
    cursor = conn.cursor()
    cursor.execute('SELECT disponibilidade FROM entregadores WHERE id = ?', (entregador_id,))
    disponibilidade = cursor.fetchone()

    if disponibilidade and disponibilidade[0]:
        status = "Em andamento"
        data_criacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
        INSERT INTO pedidos (cliente_id, entregador_id, origem, destino, status, data_criacao)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (cliente_id, entregador_id, origem, destino, status, data_criacao))
        
        # Atualizar a disponibilidade do entregador
        cursor.execute('UPDATE entregadores SET disponibilidade = ? WHERE id = ?', (False, entregador_id))

        conn.commit()
        conn.close()
        print("Pedido cadastrado com sucesso!")
    else:
        conn.close()
        print("Entregador não disponível.")

# Função para atualizar o status do pedido
def atualizar_status_pedido():
    pedido_id = int(input("Digite o ID do pedido: "))
    novo_status = input("Digite o novo status do pedido (Em andamento/Concluído/Cancelado): ")

    conn = sqlite3.connect('motofrete.db')
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE pedidos SET status = ? WHERE id = ?
    ''', (novo_status, pedido_id))

    if novo_status == 'Concluído':
        # Atualizar a disponibilidade do entregador após a conclusão do pedido
        cursor.execute('SELECT entregador_id FROM pedidos WHERE id = ?', (pedido_id,))
        entregador_id = cursor.fetchone()[0]
        cursor.execute('UPDATE entregadores SET disponibilidade = ? WHERE id = ?', (True, entregador_id))

    conn.commit()
    conn.close()
    print("Status do pedido atualizado!")

# Função para visualizar os pedidos
def visualizar_pedidos():
    conn = sqlite3.connect('motofrete.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pedidos')
    pedidos = cursor.fetchall()

    if pedidos:
        for pedido in pedidos:
            print(f"ID Pedido: {pedido[0]}, Cliente ID: {pedido[1]}, Entregad
