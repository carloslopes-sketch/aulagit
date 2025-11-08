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

print("\n" + "="*70)

# def origens_produtos ():
#     print("--- 4. CÓDIGO DE ORIGEM (MATCH/CASE) ---")
#     try:
#         codigo = int(input("Digite o código de origem (inteiro, ex: 7, 15 ou 90): "))
        
#         ESTRUTURA MATCH/CASE
#         match codigo:
#             case 1:
#                 procedencia = "Sul"
#             case 2:
#                 procedencia = "Norte"
#             case 3:
#                 procedencia = "Leste"
#             case 4:
#                 procedencia = "Oeste"
#             case 5 | 6:
#                 procedencia = "Nordeste"
#             Faixa com Condição (Guard: 'if')
#             case n if 7 <= n <= 9:
#                 procedencia = "Sudeste"
#             case 10:
#                 procedencia = "Centro-Oeste"
#             case 11:
#                 procedencia = "Nordeste"
#             Caso Padrão (Default)
#             case _:
#                 procedencia = "Importado"

#         print(f"Resultado:\n  Código {codigo} -> Procedência: {procedencia}\n")
        
#     except ValueError:
#         print("ERRO: Digite um número inteiro válido.")

# origens_produtos()
