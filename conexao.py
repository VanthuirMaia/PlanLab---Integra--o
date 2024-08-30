import os
import sqlite3

DATABASE_DIR = 'database'
DATABASE_FILE = os.path.join(DATABASE_DIR, 'plano_aula.db')

# Conectar ao banco de dados
def get_db_connection():
    if not os.path.exists(DATABASE_DIR):
        os.makedirs(DATABASE_DIR)
    db_exists = os.path.exists(DATABASE_FILE)
    conn = sqlite3.connect(DATABASE_FILE)
    if not db_exists:
        create_tables(conn)
    conn.row_factory = sqlite3.Row
    return conn

# Criação das tabelas
def create_tables(conn):
    # Tabela de usuários
    conn.execute('''
        CREATE TABLE IF NOT EXISTS usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    ''')

    # Tabela de aulas (planos de aula)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS aula (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_aula TEXT NOT NULL,
            turma TEXT NOT NULL,
            semestre TEXT NOT NULL,
            titulo TEXT NOT NULL,
            conteudo_programatico TEXT,
            metodologia TEXT,
            recursos_necessarios TEXT,
            avaliacao_observacoes TEXT,
            observacoes TEXT,
            eventos_extraordinarios TEXT CHECK(eventos_extraordinarios IN ('Sim', 'Não')),
            usuario_id INTEGER,
            FOREIGN KEY(usuario_id) REFERENCES usuario(id)
        )
    ''')

    # Tabela de cadernetas associadas aos planos de aula
    conn.execute('''
        CREATE TABLE IF NOT EXISTS caderneta (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plano_id INTEGER NOT NULL,
            data_criacao TEXT DEFAULT (DATE('now')),
            anotacoes TEXT,
            participacao TEXT,
            conteudo_trabalhado TEXT,
            atividades TEXT,
            FOREIGN KEY (plano_id) REFERENCES aula(id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    inserir_dados_iniciais(conn)

# Inserir dados iniciais
def inserir_dados_iniciais(conn):
    usuarios = conn.execute('SELECT * FROM usuario').fetchall()
    if not usuarios:
        conn.execute('''
            INSERT INTO usuario (nome, email, senha)
            VALUES ("usuario", "usuario@usuario.com.br", "1234")
        ''')
    conn.commit()

if __name__ == '__main__':
    conn = get_db_connection()
    conn.close()
    print("Banco de dados e tabelas configurados com sucesso.")
