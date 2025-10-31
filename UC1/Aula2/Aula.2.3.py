NotaUc1=int(input('Digite a primeira nota: '))
NotaUc2=int(input('Digite a segunda nota: '))
NotaUc3=int(input('Digite a terceira nota: '))
NotaUc4=int(input('Digite a quarta nota: '))
media=((NotaUc1+NotaUc2+NotaUc3+NotaUc4)/4)

if media>= 7:
    print('Aprovado')
elif media>= 5 and media<7:
    print('Recuperação')
elif media<5:
    print('Reprovação')
else:
    print('erro de calculo')
    