listagem_candidatos=[]
contador_candidatos=3
for i in range(1, 13):  # 12 candidatos
    try:
        print(f"\nCandidato {i}:")
        ano_nasc = int(input("Digite o ano de nascimento: "))
        idade = ano_atual - ano_nasc

        if idade < 18:
            print("Não pode participar (menor de 18 anos).")
            continue  # pula para o próximo candidato
        elif idade >=18:
            nome= input("Digite seu nome")
            telefone = input("Digite o telefone: ")
            email = input("Digite o e-mail: ")
            contador_candidatos-=1
            print('-'*40)
            print(f"Cadastro concluído para candidato {i}.")
            print('-'*40)
            candidato={
                'nome': nome,
                'telefone': telefone,
                'Email': email
                }
        else:
            print("favor informe um ano de nascimento valido")
        listagem_candidatos.append(candidato)
            
    except ValueError:
        print("Ano inválido! Digite apenas números para o ano de nascimento.")
print(listagem_candidatos)