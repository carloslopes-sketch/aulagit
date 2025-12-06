import math
import pandas as pd
import numpy as np

# Conjunto de dados
dados = [2, 4, 6, 8, 10]

# Passo 1: Calcular a média
media = sum(dados) / len(dados)
print(f"Dados: {dados}")
print(f"Média: {media}")

print("-" * 100)
# Passo 2: Calcular as diferenças entre cada valor e a média
diferencas = [x - media for x in dados]
print(f"Diferenças em relação à média: {diferencas}")

# Passo 3: Elevar as diferenças ao quadrado
quadrados_diferencas = [x ** 2 for x in diferencas]
print(f"Quadrados das diferenças: {quadrados_diferencas}")

# Passo 4: Calcular a média dos quadrados das diferenças
variancia = sum(quadrados_diferencas) / len(quadrados_diferencas)
print(f"Variância: {variancia:.2f}")

# Passo 5: Calcular a raiz quadrada da variância
desvio_padrao = math.sqrt(variancia)
print(f"Desvio Padrão: {desvio_padrao:.2f}")

print("-" * 100)

dados_serie = pd.Series([2, 4, 6, 8, 10])

print("--- Usando Pandas e NumPy ---")
print(f"\nMédia (usando Pandas .mean()): {dados_serie.mean():.2f}")

# NumPy por padrão usa N no denominador (população)
print(f"Variância (usando NumPy np.var()): {np.var(dados_serie):.2f}")

# Pandas por padrão usa N-1 (amostra), mas podemos forçar o cálculo da população:
# print(f"- Variância (usando Pandas .var(ddof=0)): {dados_serie.var(ddof=0):.2f}")

# NumPy por padrão usa N no denominador (população)
print(f"Desvio Padrão (usando NumPy np.std()): {np.std(dados_serie):.2f}")

# Pandas por padrão usa N-1 (amostra)
print(f"Desvio Padrão (usando Pandas .std(ddof=0)): {dados_serie.std(ddof=0):.2f}")

print("-" * 100)

# Coeficiente de Variação (CV)
cv = (desvio_padrao / media) * 100
print(f"Coeficiente de Variação (CV): {cv:.2f}%")

# Distância da Variância em relação à Média
distancia = variancia / (media ** 2)
print(f"Distância da Variância em relação à Média: {distancia:.2f}")

# Análise de Dispersão
if distancia <= 0.10:
    analise = "Baixa dispersão dos dados em relação à média."
elif distancia < 0.25:
    analise = "Dispersão moderada dos dados em relação à média."
else:
    analise = "Alta dispersão dos dados em relação à média."
    
print(f"Análise de Dispersão: {analise}")

print("-" * 100)

###################################################################

# Carregar o DataFrame
pedidos_df = pd.read_csv("../aula4/vendas_pedidos.csv")

# Selecionar os dados de interesse
dados_valor_total = pedidos_df['valor_total']

# Cálculo das medidas
media_vendas = dados_valor_total.mean()
# Usando np.var com ddof=0 para calcular a variância populacional
variancia_vendas = np.var(dados_valor_total, ddof=0)
# Usando np.std com ddof=0 para calcular o desvio padrão populacional
desvio_padrao_vendas = np.std(dados_valor_total, ddof=0)

# Coeficiente de Variação (CV)
cv_vendas = (desvio_padrao_vendas / media_vendas) * 100

# Distância da Variância em relação à Média
distancia_vendas = variancia_vendas / (media_vendas ** 2)

print(f"--- Análise dos Valores Totais dos Pedidos ---")
print(f"\nMédia dos Valores Totais: R$ {media_vendas:.2f}")
print(f"Variância dos Valores Totais: {variancia_vendas:.2f}")
print(f"Desvio Padrão dos Valores Totais: R$ {desvio_padrao_vendas:.2f}")
print("-" * 100)
print(f"Coeficiente de Variação (CV): {cv_vendas:.2f}%")
print(f"Distância da Variância / Média²: {distancia_vendas:.2f}")

# Análise de Dispersão
if distancia_vendas <= 0.10:
    analise_vendas = "Baixa dispersão dos dados em relação à média."
elif distancia_vendas < 0.25:
    analise_vendas = "Dispersão moderada dos dados em relação à média."
else:
    analise_vendas = "Alta dispersão dos dados em relação à média."
    
print(f"Conclusão da Dispersão: {analise_vendas}")