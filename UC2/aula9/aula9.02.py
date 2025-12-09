import math
import pandas as pd
import numpy as np

# Carregar o DataFrame
pedidos_df = pd.read_csv("../aula8/orders.csv")

# Verificar se a coluna existe
if 'TotalAmount' not in pedidos_df.columns:
    print("Erro: Coluna 'TotalAmount' não encontrada no DataFrame")
    print(f"Colunas disponíveis: {list(pedidos_df.columns)}")
else:
    # Selecionar os dados de interesse
    dados_valor_total = pedidos_df['TotalAmount']
    
    # Verificar se há dados
    if dados_valor_total.empty:
        print("Erro: Nenhum dado disponível na coluna 'TotalAmount'")
    else:
        # Cálculo das medidas
        media_vendas = dados_valor_total.mean()
        mediana_vendas = dados_valor_total.median()
        
        # Usando np.var com ddof=0 para calcular a variância populacional
        variancia_vendas = np.var(dados_valor_total, ddof=0)
        
        # Usando np.std com ddof=0 para calcular o desvio padrão populacional
        desvio_padrao_vendas = np.std(dados_valor_total, ddof=0)
        
        # Coeficiente de Variação (CV)
        cv_vendas = (desvio_padrao_vendas / media_vendas) * 100
        
        # Distância da Variância em relação à Média (medida de dispersão relativa)
        distancia_vendas = variancia_vendas / (media_vendas ** 2)
        
        # Cálculo de assimetria - CORREÇÃO: deve ser .skew() (método, não atributo)
        assimetria = dados_valor_total.skew()
        
        # Cálculo de curtose para análise mais completa
        curtose = dados_valor_total.kurtosis()
        
        print("=" * 80)
        print("ANÁLISE ESTATÍSTICA DOS VALORES TOTAIS DOS PEDIDOS")
        print("=" * 80)
        
        print(f"\nMEDIDAS DE TENDÊNCIA CENTRAL:")
        print(f"• Média: R$ {media_vendas:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        print(f"• Mediana: R$ {mediana_vendas:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        # print(f"• Moda: R$ {dados_valor_total.mode()[0]:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.') if not dados_valor_total.mode().empty else "• Moda: Não definida")
        
        print(f"\nMEDIDAS DE DISPERSÃO:")
        print(f"• Variância: {variancia_vendas:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        print(f"• Desvio Padrão: R$ {desvio_padrao_vendas:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        print(f"• Amplitude: R$ {dados_valor_total.max() - dados_valor_total.min():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        
        print(f"\nMEDIDAS DE DISPERSÃO RELATIVA:")
        print(f"• Coeficiente de Variação (CV): {cv_vendas:.2f}%")
        print(f"• Distância Variância/Média²: {distancia_vendas:.4f}")
        
        print(f"\nMEDIDAS DE FORMA:")
        print(f"• Assimetria (Skewness): {assimetria:.4f}")
        print(f"• Curtose: {curtose:.4f}")
        
        print("\n" + "-" * 80)
        print("INTERPRETAÇÃO DOS RESULTADOS")
        print("-" * 80)
        
        # Análise de Dispersão aprimorada
        if cv_vendas < 30:
            analise_cv = "Baixa variabilidade relativa (dados homogêneos)"
        elif cv_vendas < 50:
            analise_cv = "Média variabilidade relativa"
        else:
            analise_cv = "Alta variabilidade relativa (dados heterogêneos)"
        
        if distancia_vendas <= 0.10:
            analise_vendas = "Baixa dispersão dos dados em relação à média."
        elif distancia_vendas < 0.25:
            analise_vendas = "Dispersão moderada dos dados em relação à média."
        else:
            analise_vendas = "Alta dispersão dos dados em relação à média."
        
        print(f"\nANÁLISE DE DISPERSÃO:")
        print(f"• CV: {analise_cv}")
        print(f"• Distância Variância/Média²: {analise_vendas}")
        
        print(f"\nANÁLISE DE SIMETRIA:")
        # Critérios mais flexíveis e comuns para análise de simetria
        if -0.5 <= assimetria <= 0.5:
            Analise_Simetria = "Distribuição aproximadamente simétrica"
        elif assimetria > 0.5:
            Analise_Simetria = "Distribuição assimétrica positiva (viés à direita)"
        else:
            Analise_Simetria = "Distribuição assimétrica negativa (viés à esquerda)"
        
        print(f"• {Analise_Simetria}")
        
        print(f"\nANÁLISE DE CURTOSE:")
        if curtose > 0:
            analise_curtose = "Distribuição leptocúrtica (mais pontiaguda que a normal)"
        elif curtose < 0:
            analise_curtose = "Distribuição platicúrtica (mais achatada que a normal)"
        else:
            analise_curtose = "Distribuição mesocúrtica (curtose similar à normal)"
        print(f"• {analise_curtose}")
        
        print("\n" + "=" * 80)
        print("RESUMO ESTATÍSTICO:")
        print("=" * 80)
        print(f"• Total de pedidos analisados: {len(dados_valor_total):,}".replace(',', '.'))
        print(f"• Valor mínimo: R$ {dados_valor_total.min():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        print(f"• Valor máximo: R$ {dados_valor_total.max():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        print(f"• Soma total: R$ {dados_valor_total.sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))