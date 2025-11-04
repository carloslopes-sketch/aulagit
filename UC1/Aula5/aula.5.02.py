print("--- Usando While (Repetição Condicional)---")
contador=0 #incializamos o contador
limite=5 # Difinimos o Limite
while contador < limite: #A condição de parada
    try:
        print(f"Número {contador+1} de {limite}: ")
        num = float(input('Digite um número: '))

        dobro= num*2
        triplo=num*3
        quadruplo=num*4
        print(f" Resultado: Dobro={dobro}, Triplo={triplo}, Quádruplo={quadruplo}\n")

        contador = contador +1 # Importantissimo! Incremetar o contador 
    except ValueError:
        print("Entrada inválida. Tente novamente.")