codigodoproduto=int(input('Qual o codigo do produto?'))
match codigodoproduto:
        case 1:
            print('Domingo')
        case 2:
            print('Segunda-Feira')
        case 3:
            print('Terça-Feira')
        case 4:
            print('Quarta-Feira')
        case 5:
            print('Quinta-Feira')
        case 6:
            print('Sexta-Feira')
        case 7:
            print('Sabado-Feira')
        case _:
            print('Dia Invalido')