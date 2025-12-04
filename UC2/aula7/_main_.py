# Importe o seu módulo.
# Assumimos aqui que 'statistic.py' está no mesmo diretório.
import pandas as pd
from statistic import calcular_medidas_descritivas, gerar_painel_boxplot

# 1. Definir o caminho do arquivo
# Ajuste o caminho para onde o seu arquivo está
caminho_csv = "../aula7/orders.csv" 

# 2. Carregar os dados
try:
    df = pd.read_csv(caminho_csv)
    
    # Converter a coluna TotalAmount de string para float
    # Primeiro remover possíveis caracteres não numéricos e converter ponto para separador decimal
    df['TotalAmount'] = df['TotalAmount'].astype(str).str.replace(',', '.')  # Garantir que . é separador decimal
    df['TotalAmount'] = pd.to_numeric(df['TotalAmount'], errors='coerce')  # Converter para float
    
    # Remover valores NaN (se houver conversões falhas)
    df = df.dropna(subset=['TotalAmount'])
    
    # 3. Preparar o array para a análise
    precos_array = df['TotalAmount'].values.astype(float)
    
    # 4. Chamar a função de cálculo do seu módulo
    medidas_calculadas = calcular_medidas_descritivas(precos_array)
    
    # 5. Chamar a função de visualização do seu módulo
    if medidas_calculadas:
        gerar_painel_boxplot(
            precos_array, 
            medidas_calculadas, 
            titulo_boxplot='Boxplot de Preços (vendas_produtos.csv)', 
            caminho_salvar='Relatorio_Precos.png'
        )

except FileNotFoundError:
    print(f"Erro: O arquivo {caminho_csv} não foi encontrado.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")
# try:
#     df = pd.read_csv(caminho_csv)
    
#     # 3. Preparar o array para a análise
#     precos_array = df['TotalAmount'].values
    
#     # 4. Chamar a função de cálculo do seu módulo
#     medidas_calculadas = calcular_medidas_descritivas(precos_array)
    
#     # 5. Chamar a função de visualização do seu módulo
#     if medidas_calculadas:
#         gerar_painel_boxplot(
#             precos_array, 
#             medidas_calculadas, 
#             titulo_boxplot='Boxplot de Preços (vendas_produtos.csv)', 
#             caminho_salvar='Relatorio_Precos.png'
#         )

# except FileNotFoundError:
#     print(f"Erro: O arquivo {caminho_csv} não foi encontrado.")
# except Exception as e:
#     print(f"Ocorreu um erro: {e}")