try:
    codigoorigem=int(input('Insira o codigo de origem do produto:'))
    match codigoorigem:
        case 1:
            print('A origem do produto é Sul')
        case 2:
            print('A origem do produto é Norte')
        case 3:
            print('A origem do produto é Leste')
        case 4:
            print('A origem do produto é Oeste')
        case 5 | 6:
            print('A origem do produto é Nordeste')
        case 7 | 8 | 9:
            print('A origem do produto é Sudeste')
        case 10:
            print('A origem do produto é Centro-Oeste')
        case 11:
            print('A origem do produto é Noroeste')
except ValueError:
    print('Importado')