import math
import pandas as pd
import numpy as np


# Carregar o DataFrame
pedidos_df = pd.read_csv("../aula8/orders.csv")

# Selecionar os dados de interesse
dados_valor_total = pedidos_df['TotalAmount']

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