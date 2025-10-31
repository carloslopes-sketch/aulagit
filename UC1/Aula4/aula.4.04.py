Iniciodia=float(input('Qual a quantidade de KM no incio do dia?'))
fimdia=float(input('Qual a quantidade de KM no final do dia?'))
#combustivelgasto=float(input('Qual a quantidade de litros gastos no final do dia?'))
Valorrecebido=float(input('Qual o valor total recebido no total do dia? '))
quantidadelitrosporkm=float(input('Qual a quantidade de km por litros ?'))
mediaconsumo=((fimdia-Iniciodia)/ quantidadelitrosporkm)
valorcombustivel=mediaconsumo*6.15
total=Valorrecebido-valorcombustivel

if total >0:
    print('O Taxista teve um lucro de', total)
else:
    print('O Taxista teve um prejuizo de, ', total)

