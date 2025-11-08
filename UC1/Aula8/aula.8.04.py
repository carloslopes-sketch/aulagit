# import time

# def dar_boas_vindas():
#  print("-"*40)
#  print(" Bem-vindo ao nosso aplicativo! 😀")
#  print("-"*40)

# # 2. CHAMADA da função
# # O código abaixo só será executado se você "chamar" a função pelo nome:

# print("Início do programa.")
# dar_boas_vindas() # <-- Isso executa o código dentro da função
# print("Meio do programa.")
# dar_boas_vindas() # <-- Podemos chamar de novo!
# print("Fim do programa.")
# time.sleep(2)
# nome=input('Isira seu nome: ')

# def boas_vindas_personalizado(nome_da_pessoa):

#  print("-"*40)
#  print(f"Olá, {boas_vindas_personalizado}! Seja bem-vindo(a)! 😀")
#  print("-"*40)
# Ao chamar a função, passamos o ARGUMENTO (o valor)
# boas_vindas_personalizado("Maria")
# boas_vindas_personalizado("João")


# def somar(a, b):
#     resultado = a + b
#     return resultado

# # Para usar o valor, precisamos guardá-lo em uma variável

# soma1 = somar(5, 10)
# soma2 = somar(100, 50)

# print(f"O primeiro resultado é: {soma1}")
# print(f"O segundo resultado é: {soma2}")
# print(f"Você pode usar direto no print: {somar(3, 3)}")


def somar(a, b):
    """
    
    Esta função recebe dois números (a e b) e retorna a soma deles.
    (Isso é uma 'docstring', uma boa prática para documentar o que a função faz)
    
    """
    resultado = a + b
    return resultado
# 2. Parte principal do nosso programa
print("Calculadora de Somas")
# 3. Vamos usar um loop 'for' para tratar dos 3 pares

for i in range(3):
    print(f"\n--- Calculando {i+1}º par ---")
 
    # Pedimos os números ao usuário
    num1 = int(input("Digite o primeiro número: "))
    num2 = int(input("Digite o segundo número: "))
    
    # Chamamos a função com os números que o usuário digitou
    # e guardamos o valor que ela 'retornou'
    resultado_da_soma = somar(num1, num2)
    
    # Imprimimos o resultado
    print(f"A soma de {num1} + {num2} é = {resultado_da_soma}")

print("\nPrograma finalizado!")
