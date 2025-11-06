### TUPLA ###

pares=(30,20,50,48,80,49,60,7,90)
print(pares[3])
print(pares[3:])
print(pares[3:5])
print(pares[:3])
print(len(pares))
pares=pares+(44,)
print(pares)
listas_pares=list(pares)
print('*'*90)
listas_pares.remove(90)
print(listas_pares)