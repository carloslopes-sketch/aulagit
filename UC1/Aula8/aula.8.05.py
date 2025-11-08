import random # Sempre no topo do arquivo!

def gerar_dados(qtd, min_val, max_val):
    """
    Gera uma LISTA de números aleatórios.
    - qtd: quantos números queremos na lista
    - min_val: o valor mínimo (inclusivo)
    - max_val: o valor máximo (inclusivo)
    """
 
    # A estrutura a seguir se chama "List Comprehension".
    # É um jeito rápido de criar uma lista usando um loop.
    lista_de_dados = [random.randint(min_val, max_val) for _ in range(qtd)]
 
    return lista_de_dados
    # Testando a função
dados_aleatorios = gerar_dados(5, 1, 100) # Gera 5 números entre 1 e 100
print(f"Dados gerados: {dados_aleatorios}")