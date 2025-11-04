print("--- Simulação DO-WHILE (Executa 1ª vez, depois checa) ---")
contador = 0
limite = 5
while True: # Loop infinito garantido para executar pelo menos uma vez
    if contador >= limite:
        break # Ponto de DECISÃO: Se o limite for atingido, usamos 'break' para sair

    try:
        print(f"Número {contador + 1} de {limite}:")
        num = float(input("Digite um número: "))
        dobro = num * 2
        triplo = num * 3
        quadruplo = num * 4
        print(f" Resultado: Dobro={dobro}, Triplo={triplo}, Quádruplo={quadruplo}\n")

        contador = contador + 1 # Incremento
        
    except ValueError:
        print("Entrada inválida. Tente novamente.")