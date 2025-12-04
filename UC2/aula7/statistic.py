import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==============================================================================
# 1. FUNÇÃO DE CÁLCULO
# ==============================================================================

def calcular_medidas_descritivas(dados_array):
    """
    Calcula e retorna um dicionário com as principais medidas estatísticas
    de tendência central, posição e dispersão para um array NumPy.
    """
    if dados_array is None or len(dados_array) == 0:
        return None

    # Medidas de Tendência Central
    media = np.mean(dados_array)
    mediana = np.median(dados_array)

    # Medidas de Posição (Quartis e IQR)
    Q1 = np.percentile(dados_array, 25)
    Q3 = np.percentile(dados_array, 75)
    IQR = Q3 - Q1

    # Limites de Outliers
    limite_superior = Q3 + (1.5 * IQR)
    limite_inferior = Q1 - (1.5 * IQR)

    # Valores Extremos
    min_valor = np.min(dados_array)
    max_valor = np.max(dados_array)

    return {
        'media': media,
        'mediana': mediana,
        'Q1': Q1,
        'Q3': Q3,
        'IQR': IQR,
        'limite_superior': limite_superior,
        'limite_inferior': limite_inferior,
        'min_valor': min_valor,
        'max_valor': max_valor,
    }

# ==============================================================================
# 2. FUNÇÃO DE VISUALIZAÇÃO
# ==============================================================================

def gerar_painel_boxplot(dados_array, medidas, titulo_boxplot='Boxplot da Distribuição de Dados', caminho_salvar=None):
    """
    Gera e exibe um painel com um Boxplot e um resumo das medidas estatísticas.
    
    Args:
        dados_array (np.ndarray): O array NumPy com os dados.
        medidas (dict): O dicionário retornado por calcular_medidas_descritivas().
        titulo_boxplot (str): Título para o boxplot.
        caminho_salvar (str, optional): Caminho para salvar a imagem.
    """
    if medidas is None:
        print("Erro: Medidas estatísticas não fornecidas ou inválidas.")
        return

    fig, axes = plt.subplots(1, 2, figsize=(16, 8))

    # --- POSIÇÃO 1: BOXPLOT ---
    sns.boxplot(y=dados_array, ax=axes[0])
    axes[0].set_title(titulo_boxplot)
    axes[0].set_ylabel(dados_array.name if hasattr(dados_array, 'name') else 'Valores')

    # --- POSIÇÃO 2: CENÁRIO DE MEDIDAS (plt.text) ---
    axes[1].axis('off')
    axes[1].set_title('Medidas Estatísticas Calculadas')

    # Preparando o texto formatado (usando as chaves do dicionário 'medidas')
    resumo = (
        f"Medidas de Tendência Central:\n"
        f"  Média: R$ {medidas['media']:.2f}\n"
        f"  Mediana (Q2): R$ {medidas['mediana']:.2f}\n"
        f"\n"
        f"Medidas de Posição/Dispersão:\n"
        f"  Q1: R$ {medidas['Q1']:.2f}\n"
        f"  Q3: R$ {medidas['Q3']:.2f}\n"
        f"  IQR: R$ {medidas['IQR']:.2f}\n"
        f"\n"
        f"Limites e Extremos:\n"
        f"  Limite Superior (LS): R$ {medidas['limite_superior']:.2f}\n"
        f"  Limite Inferior (LI): R$ {medidas['limite_inferior']:.2f}\n"
        f"  Valor Máximo: R$ {medidas['max_valor']:.2f}\n"
        f"  Valor Mínimo: R$ {medidas['min_valor']:.2f}\n"
    )

    # Adicionando o texto
    axes[1].text(0.1, 0.95, resumo,
                 transform=axes[1].transAxes,
                 fontsize=12,
                 verticalalignment='top',
                 bbox=dict(boxstyle="round,pad=0.5", alpha=0.1, color='lightgray'))

    plt.tight_layout()
    
    if caminho_salvar:
        plt.savefig(caminho_salvar)
        print(f"Painel salvo em: {caminho_salvar}")
    
    plt.show()