import pandas as pd
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

######################

def obter_dados_do_banco(query):
    try:
        conexao = mysql.connector.connect(
            host="127.0.0.1",
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

######################


query_clientes = "SELECT * FROM clientes"
df_clientes = pd.DataFrame(obter_dados_do_banco(query_clientes), columns=['id_cliente', 'nome', 'email'])
print(df_clientes)

df_pedidos = pd.read_csv('vendas_pedidos.csv')
print(df_pedidos)

# Relacionando os DataFrames pela coluna 'id_cliente'
df_relacionado = pd.merge(df_clientes, df_pedidos, on='id_cliente', how='inner')

print(df_relacionado)