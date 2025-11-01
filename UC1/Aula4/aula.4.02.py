potencialampada=float(input('Qual a voltagem das lampadas?'))
largura=float(input('Qual a largura do comodo?'))
comprimento=float(input('Qual comprimento do comodo?'))
metrosquadrados=largura*comprimento
potencianecessaria= metrosquadrados*3

quantidadelampadas= int (potencianecessaria/potencialampada)
num_lampadas_float=quantidadelampadas / potencianecessaria


if num_lampadas_float > quantidadelampadas:
    num_lampadas_final = quantidadelampadas+1

else:
    num_lampadas_final = quantidadelampadas


print(f"Resultado:\n Área: {metrosquadrados:.2f} m²")
print(f"Lâmpadas necessárias: {num_lampadas_final}")


