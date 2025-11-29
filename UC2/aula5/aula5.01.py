import numpy as np
import pandas as pd

# lista_numeros = [10, 20, 30, 40, 50]
# meu_array = np.array(lista_numeros)

# print(meu_array)
# # Saída: [10 20 30 40 50]
# print(type(meu_array))
# # Saída: <class 'numpy.ndarray'>

# # Comparando com uma série do Pandas
# minha_serie = pd.Series(lista_numeros)
# print(minha_serie)
# print(type(minha_serie))

####################################################

# Extraindo a coluna 'preco' do arquivo vendas_produtos.csv com Numpy
precos_array = np.genfromtxt('../aula4/vendas_pedidos.csv', delimiter=',', skip_header=1, dtype=None, encoding='utf-8', usecols=3)
print(precos_array)
print(type(precos_array))

# Calcule a média:
media = np.mean(precos_array)
print(f"Média dos preços: R$ {media:.2f}")


# Obtenha a mediana:
mediana = np.median(precos_array)
print(f"Mediana dos preços: R$ {mediana:.2f}")


# Calcule a distância entre a média e a mediana:
distancia = (media - mediana) / mediana
print(f"Distância entre a média e a mediana: {distancia * 100:.2f}%")

if abs(distancia) <= 0.10:
    print("A média tende a ser uma medida de tendência central confiável.")
elif abs(distancia) < 0.25:
    print("A média pode estar sofrendo uma influência moderada de valores extremos.")
else:
    print("A média tende a não ser uma medida de tendência central confiável.")

# Verificando a direção da influência
if media > mediana:
    print("A influência é dos valores mais altos da distribuição.")
elif media < mediana:
    print("A influência é dos valores mais baixos da distribuição.")

# Visualizando a distribuição dos preços
import matplotlib.pyplot as plt  # Importando a biblioteca Matplotlib
import seaborn as sns  # Importando a biblioteca Seaborn    

sns.histplot(precos_array, kde=True) # kde=True adiciona a curva de densidade, traduzindo seria "Kernel Density Estimate"
plt.title('Distribuição dos Preços dos Produtos')
plt.show()  