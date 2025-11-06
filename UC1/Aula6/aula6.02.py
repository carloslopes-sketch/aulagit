# Lista vazia para armazenar os resultados
resultados = []


for i in range(1, 6):
    print(f"\n--- Aluno {i} ---")
    

    nota1 = float(input("Digite a primeira nota: "))
    nota2 = float(input("Digite a segunda nota: "))
    nota_optativa = float(input("Digite a nota optativa (-1 se não fez): "))
    

    notas_finais = [nota1, nota2]
    usado_optativa = False
    

    if nota_optativa != -1:

        menor_nota = min(nota1, nota2)
        

        if nota1 == menor_nota:
            notas_finais[0] = nota_optativa
        else:
            notas_finais[1] = nota_optativa
        
        usado_optativa = True
        print(f"Nota optativa ({nota_optativa}) substituiu a menor nota ({menor_nota})")
    

    media = sum(notas_finais) / 2
    

    if media >= 7.0:
        situacao = "Aprovado"
    elif media >= 5.0:
        situacao = "Recuperação"
    else:
        situacao = "Reprovado"
    

    info_optativa = " (com optativa)" if usado_optativa else ""
    resultados.append(f"Aluno {i} - Notas: {notas_finais[0]:.1f}, {notas_finais[1]:.1f} - Média: {media:.1f}{info_optativa} - {situacao}")
    
    print(f"Notas finais: {notas_finais[0]:.1f}, {notas_finais[1]:.1f}")
    print(f"Média: {media:.1f} - {situacao}")


print("\n" + "="*70)
print("RESULTADOS FINAIS:")
print("="*70)
for resultado in resultados:
    print(resultado)