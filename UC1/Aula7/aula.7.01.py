lista02_nopets=[
    'lavar louça', 
    'Ir ao mercado',
    'Lavar banheiro',
    'Tirar poeira', 
    'Lavar o quintal']
lista02_nopets.append('Dar banho no cachorro')
lista02_nopets.pop()
#print(lista02_nopets)
#print(lista02_nopets[1])
#print(lista02[1][6:13])
#print(lista02_nopets[1][6:])
#print(lista02_nopets[1][:6],lista02_nopets[4][8:])
lista02_pets=lista02_nopets.copy()
lista02_pets.append('Dar banho no doguinho')
lista02_pets.append('Limpar areia dos gatos')
lista02_pets.insert(5,'Ir ao Veterinario')

lista02_pets.remove('Ir ao Veterinario')
print(lista02_pets)


