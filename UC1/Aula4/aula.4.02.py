potencialampada=int(input('Qual a voltagem das lampadas?'))
largura=int(input('Qual a largura do comodo?'))
comprimento=int(input('Qual comprimento do comodo?'))
metrosquadrados=largura*comprimento
quantidadelampadas=metrosquadrados/potencialampada


if potencialampada ==3:
    print('Serão nessárias',quantidadelampadas)
elif potencialampada >3:
    print('Serão necessárias',  quantidadelampadas)