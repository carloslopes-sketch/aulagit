import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar o arquivo completo:
df_produtos = pd.read_csv('./aula6/vendas_produtos.csv')

# Extrair a coluna de preços:
precos_array = df_produtos['preco'].values

# Exibir os primeiros dados carregados para confirmação:
print("DataFrame Carregado (Primeiros 5):")
print(df_produtos.head())
print("\nArray de Preços Carregado (Primeiros 5):")
print(precos_array[:5])

# Calcular Q1 e Q3
Q1 = np.percentile(precos_array, 25)
Q3 = np.percentile(precos_array, 75)

# Calcular IQR
IQR = Q3 - Q1

# Calcular Limites
limite_superior = Q3 + (1.5 * IQR)
limite_inferior = Q1 - (1.5 * IQR)

print(f"\n--- Limites de Outliers (Preços dos Produtos) ---")
print(f"Q1 (25%): R$ {Q1:.2f}")
print(f"Q3 (75%): R$ {Q3:.2f}")
print(f"IQR: R$ {IQR:.2f}")
print(f"Limite Superior (LS): R$ {limite_superior:.2f}")
print(f"Limite Inferior (LI): R$ {limite_inferior:.2f}")

# Identificação de Outliers Superiores e Inferiores
outliers_superiores = df_produtos[df_produtos['preco'] > limite_superior]
outliers_inferiores = df_produtos[df_produtos['preco'] < abs(limite_inferior)]

# Exibir Outliers Superiores Ordenados (Decrescente)
print(f"\n--- Outliers Superiores ({len(outliers_superiores)} produtos) ---")
print(outliers_superiores[['nome', 'preco']].sort_values(by='preco', ascending=False))

# Exibir Outliers Inferiores Ordenados (Crescente)
print(f"\n--- Outliers Inferiores ({len(outliers_inferiores)} produtos) ---")
print(outliers_inferiores[['nome', 'preco']].sort_values(by='preco', ascending=True))

# Garante que os DataFrames de outliers não estão vazios antes de plotar
if not outliers_inferiores.empty or not outliers_superiores.empty:
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6)) # 1 linha, 2 colunas
    
    # 1ª Posição: Outliers Inferiores (Crescente)
    axes[0].bar(outliers_inferiores['nome'], outliers_inferiores['preco'])
    axes[0].set_title('Outliers Inferiores (Preços Mais Baixos)')
    axes[0].set_ylabel('Preço (R$)')
    axes[0].tick_params(axis='x', rotation=45, labelsize=8)
    axes[0].grid(axis='y', linestyle='--')
    
    # 2ª Posição: Outliers Superiores (Decrescente)
    # Ordenamos novamente para garantir a visualização correta
    outliers_superiores_plot = outliers_superiores.sort_values(by='preco', ascending=False)
    axes[1].bar(outliers_superiores_plot['nome'], outliers_superiores_plot['preco'])
    axes[1].set_title('Outliers Superiores (Preços Mais Altos)')
    axes[1].set_ylabel('Preço (R$)')
    axes[1].tick_params(axis='x', rotation=45, labelsize=8)
    axes[1].grid(axis='y', linestyle='--')
    
    plt.tight_layout() # Ajusta automaticamente os parâmetros de subplot para dar preenchimento
    plt.show()

else:
    print("\nNão houve outliers superiores ou inferiores para plotar.")