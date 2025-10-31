numero1=80
numero2=30
numero3=50

if numero1< numero2 and numero3 and numero3 < numero2:
    print(numero1,numero3,numero2)
elif numero1< numero2 and numero3 and numero3 > numero2:
    print(numero1,numero2,numero3)
elif numero1< numero2 and numero3 and numero3 > numero2:
    print(numero1,numero2,numero3)
elif numero1> numero2 and numero3 and numero3 > numero2:
    print(numero2,numero3,numero1)
else:
    print(numero3,numero2,numero1)
