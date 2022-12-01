import mysql.connector
from mysql.connector import errorcode

# Cria a Conexão e Pega os Parâmetros do MySQL
connection = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '12345'
)

cursor = connection.cursor()

# Descarta o Banco se já for Existente
cursor.execute("DROP DATABASE IF EXISTS `bancofilmes`")

# Cria o Banco de Dados (Schema) e Deixa-o Ativo para Uso
cursor.execute("CREATE DATABASE `bancofilmes`;")
cursor.execute("USE `bancofilmes`;")

# Cria as Tabelas do Banco "bancofilmes"
TABLES = {}

TABLES['Filmes'] = ('''
CREATE TABLE `filmes` (
    `id_filme` INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `nome_filme` VARCHAR(100),
    `data_lancamento` DATE NOT NULL,
    `nome_diretor` VARCHAR(100),
    `nome_ator` VARCHAR(100)
)
''')

TABLES['Plataformas'] = ('''
CREATE TABLE `plataformas` (
    `id_plataforma` INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `nome_plataforma` VARCHAR(100)
);
''')

TABLES['Comentarios'] = ('''
CREATE TABLE `comentarios` (
    `id_comentario` INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `comentario` VARCHAR(500)
)
''')

TABLES['Usuarios'] = ('''
CREATE TABLE `usuarios` (
    `id_usuario` INTEGER NOT NULL AUTO_INCREMENT,
    `nome_usuario`  VARCHAR(100),
    `email` VARCHAR(50),
    `senha` VARCHAR(30)
)
''')

# Cria a Tabela e Retorna Sucesso ou Erro
for nome_tabela in TABLES:
    tabela = TABLES[nome_tabela]
    
    try:
        print('A Tabela {}:'.format(tabela), end = ' ')
        cursor.execute(tabela)
    except mysql.connector.Error as erro:
        if erro.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print('A Tabela já Existe!')
        else:
            print(erro.msg)
    else:
        print('Tudo OK!')

# Operação de Commit no Banco
connection.commit()

# Fecha o Banco e as Operações
cursor.close()
connection.close()