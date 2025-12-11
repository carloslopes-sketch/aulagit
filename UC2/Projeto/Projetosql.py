import mysql.connector

def obter_dados_do_banco(query):
    try:
        conexao = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="amazon"
        )
        cursor = conexao.cursor()
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        # Obtém os nomes das colunas
        colunas = [desc[0] for desc in cursor.description]
        return resultados, colunas
    except mysql.connector.Error as erro:
        print(f"Erro ao conectar ao MySQL: {erro}")
        return None, None
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()

def mostrar_menu():
    print("\n" + "="*60)
    print("SISTEMA DE CONSULTAS AO BANCO DE DADOS")
    print("="*60)
    print("\nEscolha uma consulta para executar:")
    print("1. Pedidos com valor superior a 100")
    print("2. Clientes de Nova York")
    print("3. Pedidos com valor superior a 1000")
    print("4. Total de pedidos por cliente (a partir de 2000)")
    print("5. Total de pedidos por cliente com detalhes (a partir de 2000)")
    print("6. Sair")
    print("-"*60)

def obter_query_escolhida(opcao):
    queries = {
        1: """select orders.OrderID,
orders.OrderDate,
products.ProductName,
orders.TotalAmount
from orders
join products on
products.ProductID = orders.ProductID
where orders.TotalAmount > 100
order by TotalAmount""",
        
        2: """select customers.CustomerName,
orders.OrderDate,
products.Category,
products.ProductName,
customers.city
from products
join orders on
products.ProductID = orders.ProductID
join customers on
orders.CustomerID = customers.CustomerID
where customers.city = 'New York'""",
        
        3: """select customers.CustomerName,
orders.OrderDate,
products.ProductName,
orders.PaymentMethod,
orders.TotalAmount
from products
join orders on
products.ProductID = orders.ProductID
join customers on
orders.CustomerID = customers.CustomerID
where orders.TotalAmount > 1000""",
        
        4: """SELECT 
    customers.CustomerName,
    customers.City,
    customers.State,
    customers.Country,
    Sum(orders.TotalAmount) AS TotalPedidos
FROM customers
JOIN orders ON orders.CustomerID = customers.CustomerID
WHERE YEAR(orders.OrderDate) >= 2000
GROUP BY 
    customers.CustomerID,
    customers.CustomerName,
    customers.City,
    customers.State,
    customers.Country
ORDER BY TotalPedidos DESC""",
        
        5: """SELECT 
    customers.CustomerName,
    customers.City,
    customers.State,
    customers.Country,
    Sum(orders.TotalAmount) AS TotalPedidos
FROM customers
JOIN orders ON orders.CustomerID = customers.CustomerID
WHERE YEAR(orders.OrderDate) >= 2000
GROUP BY 
    customers.CustomerID,
    customers.CustomerName,
    customers.City,
    customers.State,
    customers.Country
ORDER BY TotalPedidos DESC"""
    }
    
    return queries.get(opcao)

def mostrar_resultados(resultados, colunas):
    if resultados and colunas:
        print(f"\n{'='*80}")
        print(f"RESULTADOS DA CONSULTA ({len(resultados)} registros encontrados)")
        print('='*80)
        
        # Mostra os nomes das colunas
        print(" | ".join(colunas))
        print("-"*80)
        
        # Mostra os dados
        for linha in resultados:
            # Formata cada valor para melhor visualização
            linha_formatada = []
            for valor in linha:
                if valor is None:
                    linha_formatada.append("NULL")
                else:
                    linha_formatada.append(str(valor))
            print(" | ".join(linha_formatada))
    elif resultados is None:
        print("\nNão foi possível executar a consulta.")
    else:
        print("\nNenhum resultado encontrado.")

def main():
    while True:
        mostrar_menu()
        
        try:
            escolha = int(input("\nDigite sua opção (1-6): "))
            
            if escolha == 6:
                print("\nSaindo do sistema...")
                break
                
            if escolha < 1 or escolha > 5:
                print("\nOpção inválida! Por favor, escolha uma opção entre 1 e 6.")
                continue
                
            # Obtém a query escolhida
            query = obter_query_escolhida(escolha)
            
            if query:
                print(f"\nExecutando consulta {escolha}...")
                
                # Executa a consulta
                resultados, colunas = obter_dados_do_banco(query)
                
                # Mostra os resultados
                mostrar_resultados(resultados, colunas)
            else:
                print("\nErro: Query não encontrada para a opção selecionada.")
                
        except ValueError:
            print("\nErro: Por favor, digite um número válido.")
        except Exception as e:
            print(f"\nOcorreu um erro: {e}")

if __name__ == "__main__":
    main()