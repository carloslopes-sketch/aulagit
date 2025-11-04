Login = 'mestre'
senha = 'mestre'
contador=0
tentativa=3
totaltentativa=3

while contador < tentativa: # Loop infinito garantido para executar pelo menos uma vez
    try:
        print(F'Tentativas: {contador+1} de {totaltentativa}')
        InputLogin= input('Insira login: ')
        Inputsenha=input('Insira sua senha: ')
        if Login == InputLogin and senha== Inputsenha:
            print('Login realizado com sucesso')
            print('------------------------------------------------------')
            break
        else:
            print('Usuario ou senha invalidos, favor tente novamente!')
            #print(F'Tentativas: {contador+1} de {tentativa}')

            #break  # Ponto de DECISÃO: Se o limite for atingido, usamos 'break' para sair
            tentativa -=1
            contador += 1 
    except ValueError:
        print("Entrada inválida. Tente novamente.")
if tentativa== 0:
    print('BLOQUEADO: Número máximo de tentativas permitidas foram realizadas.')