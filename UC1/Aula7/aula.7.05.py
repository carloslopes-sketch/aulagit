def origens_produtos ():
    print("--- 4. CÓDIGO DE ORIGEM (MATCH/CASE) ---")
    try:
        codigo = int(input("Digite o código de origem (inteiro, ex: 7, 15 ou 90): "))
        
        # ESTRUTURA MATCH/CASE
        match codigo:
            case 1:
                procedencia = "Sul"
            case 2:
                procedencia = "Norte"
            case 3:
                procedencia = "Leste"
            case 4:
                procedencia = "Oeste"
            case 5 | 6:
                procedencia = "Nordeste"
            # Faixa com Condição (Guard: 'if')
            case n if 7 <= n <= 9:
                procedencia = "Sudeste"
            case 10:
                procedencia = "Centro-Oeste"
            case 11:
                procedencia = "Nordeste"
            # Caso Padrão (Default)
            case _:
                procedencia = "Importado"

        print(f"Resultado:\n  Código {codigo} -> Procedência: {procedencia}\n")
        
    except ValueError:
        print("ERRO: Digite um número inteiro válido.")

origens_produtos()
