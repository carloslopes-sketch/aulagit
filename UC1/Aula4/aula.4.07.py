Nota1=float(input('Insira o valor da Nota da Primeira Prova:'))
Nota2=float(input('Insira o valor da Nota da segunda Prova:'))
Optativa=float(input('Insira o valor da nota da prova Optativa:'))
Media1=(Optativa+Nota1)/2
Media2=(Optativa+Nota2)/2
media3=(Nota1+Nota2)/2
if Optativa > Nota1 or Nota2 and Nota2 > Nota1 and Media2>=6:
    print('Aluno Aprovado')
elif Optativa > Nota1 or Nota2 and Nota2 < Nota1 and Media1>=6:
    print('Aluno Aprovado')
elif Optativa > Nota1 or Nota2 and Nota2 > Nota1 and Media2 <6 and Media2>3:
    print('Aluno em Recuperação')
elif Optativa > Nota1 or Nota2 and Nota2 < Nota1 and Media2 <6 and Media1>3:
    print('Aluno em Recuperação')
elif Optativa > Nota1 or Nota2 and Nota2 > Nota1 and Media2<3:
    print('Aluno Reprovado')
elif Optativa > Nota1 or Nota2 and Nota2 < Nota1 and Media1<3:
    print('Aluno Reprovado')
elif Optativa > Nota1 or Nota2 and Nota1 > Nota2 and Media1>=6:
    print('Aluno Aprovado')
elif Optativa > Nota1 or Nota2 and Nota1 < Nota2 and Media2>=6:
    print('Aluno Aprovado')
elif Optativa > Nota1 or Nota2 and Nota2 > Nota1 and Media1 <6 and Media1>3:
    print('Aluno em Recuperação')
elif Optativa > Nota1 or Nota2 and Nota2 > Nota1 and Media1<3:
    print('Aluno Reprovado')
elif media3>=6:
    print('Aluno Aprovado')
elif media3 <6 and Media1>3:
    print('Aluno em Recuperação')
elif media3<3:
    print('Aluno Reprovado')
else:
    print('Erro nos lançamentos')