import pandas as pd

df = pd.read_csv('vendas_produtos.csv')
print(df.head())




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
query_produtos = "SELECT * FROM pedidos"
dados_filtrados = obter_dados_do_banco(query_produtos)

if dados_filtrados:
    for produto in dados_filtrados:
        print(produto)