diadasemana=int(input('Qual dia da semana você quer saber?'))

match diadasemana:
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
        

# if diadasemana==1:
#     print ('Domingo')
# elif diadasemana==2:
#     print('Segunda-feira')
# elif diadasemana==3:
#     print('Terça-feira')
# elif diadasemana==4:
#     print('Quarta-feira')
# elif diadasemana==5:
#     print('Quinta-feira')
# elif diadasemana==6:
#     print('Sexta-feira')
# elif diadasemana==7:
#     print('Sabado')
# else:
#     print ('Número Invalida')