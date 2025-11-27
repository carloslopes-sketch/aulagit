import pandas as pd

df = pd.read_csv('vendas_produtos.csv')
print(df.head())


import mysql.connector
# 1. Conectar ao banco de dados
conexao = mysql.connector.connect(
 host="127.0.0.1",
 user="root",
 password="",
 database="vendas_online"
)

# 2. Criar um objeto cursor para executar as queries
cursor = conexao.cursor()
# 3. Definir a query
query = "SELECT * FROM produtos"
# 4. Executar a query
cursor.execute(query)
# 5. Obter os resultados
resultados = cursor.fetchall()
# 6. Exibir os resultados
for linha in resultados:
 print(linha)
# 7. Fechar a conexão
cursor.close()
conexao.close()

import mysql.connector

def obter_dados_do_banco(query):
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="vendas_online"
        )
        cursor = conexao.cursor()
        cursor.execute(query)
        resultados = cursor.fetchall()
        return resultados
    except mysql.connector.Error as erro:
        print(f"Erro ao conectar ao MySQL: {erro}")
        return None
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()

# Usando a função
query_produtos = "SELECT * FROM produtos WHERE preco > 100"
dados_filtrados = obter_dados_do_banco(query_produtos)

if dados_filtrados:
    for produto in dados_filtrados:
        print(produto)