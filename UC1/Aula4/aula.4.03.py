largura=int(input('Qual a largura do comodo?'))
altura=int(input('Qual a altura do comodo?'))
comprimento=int(input('Qual a comprimento do comodo?'))
parede1=largura*altura
parede2=largura*altura
parede3=comprimento*altura
parede4=comprimento*altura
totalmetros=parede1+parede2+parede3+parede4

print('O total de caixas de azuleijos será de', (totalmetros/1.5))
