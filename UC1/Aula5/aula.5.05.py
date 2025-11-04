Idade = int(input('Insira a sua Idade: ')) # Inicializamos o contador
Limite = 18
contador=1
while True: # Loop infinito garantido para executar pelo menos uma vez
    try:
        Nome= input('Insira seu nome: ')
        formacao=input('Insira sua formação: ')

        print(F'O cadidato {Nome} e com a formação de {formacao} está apto a participar do processo!! ')
        contador = contador +1
    except ValueError:
        print("Entrada inválida. Tente novamente.")






            if Idade < Limite:
        print('Menores de 18 não podem participar do processo!')
        break  # Ponto de DECISÃO: Se o limite for atingido, usamos 'break' para sair
    if contador> 12:
        break