import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os
import warnings
warnings.filterwarnings('ignore')

# Configurar estilo dos gráficos
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Função para formatar valores em Reais
def formatar_reais(valor):
    return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# Funções de análise interpretativa
def analisar_media_mediana(media, mediana, dados):
    """Analisa a relação entre média e mediana"""
    dif_percent = abs((media - mediana) / mediana) * 100
    
    if dif_percent < 10:
        return {
            'status': '✅ BALANCEADO',
            'descricao': f'Média e mediana próximas (diferença de {dif_percent:.1f}%)',
            'interpretacao': 'Distribuição aproximadamente simétrica. A média representa bem o valor típico.',
            'recomendacao': 'Pode usar a média como referência principal para decisões.',
            'cor': 'green'
        }
    elif dif_percent < 30:
        return {
            'status': '⚠️ MODERADA DIFERENÇA',
            'descricao': f'Média {dif_percent:.1f}% diferente da mediana',
            'interpretacao': 'Moderada assimetria. Valores extremos estão influenciando a média.',
            'recomendacao': 'Considere usar a mediana para decisões mais robustas.',
            'cor': 'orange'
        }
    else:
        direcao = "acima" if media > mediana else "abaixo"
        return {
            'status': '❌ ALTA DIFERENÇA',
            'descricao': f'Média {dif_percent:.1f}% {direcao} da mediana',
            'interpretacao': f'Alta assimetria. Valores muito { "altos" if media > mediana else "baixos" } estão distorcendo a média.',
            'recomendacao': 'Use a mediana como referência. Investigue os valores extremos.',
            'cor': 'red'
        }

def analisar_variabilidade(cv):
    """Analisa o coeficiente de variação"""
    if cv < 15:
        return {
            'status': '✅ BAIXA VARIABILIDADE',
            'descricao': f'CV = {cv:.1f}% (consistente)',
            'interpretacao': 'Valores muito homogêneos. Padrão de vendas estável.',
            'recomendacao': 'Previsões financeiras mais confiáveis.',
            'cor': 'green'
        }
    elif cv < 30:
        return {
            'status': '⚠️ VARIABILIDADE MODERADA',
            'descricao': f'CV = {cv:.1f}% (moderado)',
            'interpretacao': 'Variabilidade aceitável. Alguma dispersão nos valores.',
            'recomendacao': 'Monitorar periodicamente para detectar mudanças.',
            'cor': 'orange'
        }
    elif cv < 50:
        return {
            'status': '⚠️ ALTA VARIABILIDADE',
            'descricao': f'CV = {cv:.1f}% (alto)',
            'interpretacao': 'Valores bastante dispersos. Diferentes perfis de compra.',
            'recomendacao': 'Segmentar análise por faixa de valor.',
            'cor': 'red'
        }
    else:
        return {
            'status': '❌ VARIABILIDADE MUITO ALTA',
            'descricao': f'CV = {cv:.1f}% (muito alto)',
            'interpretacao': 'Extrema dispersão. Difícil estabelecer padrão típico.',
            'recomendacao': 'Analisar separadamente diferentes grupos de clientes.',
            'cor': 'darkred'
        }

def analisar_assimetria(assimetria):
    """Analisa o coeficiente de assimetria"""
    if -0.5 <= assimetria <= 0.5:
        return {
            'status': '✅ SIMÉTRICA',
            'descricao': f'Assimetria = {assimetria:.3f} (balanceada)',
            'interpretacao': 'Distribuição equilibrada. Valores igualmente distribuídos.',
            'recomendacao': 'Análise simplificada, comporta-se como normal.',
            'cor': 'green'
        }
    elif 0.5 < assimetria <= 1:
        return {
            'status': '⚠️ ASSIMETRIA POSITIVA MODERADA',
            'descricao': f'Assimetria = {assimetria:.3f} (positiva moderada)',
            'interpretacao': 'Cauda à direita. Alguns valores altos puxam a distribuição.',
            'recomendacao': 'Focar em vendas de alto valor como oportunidade.',
            'cor': 'orange'
        }
    elif assimetria > 1:
        return {
            'status': '❌ ASSIMETRIA POSITIVA FORTE',
            'descricao': f'Assimetria = {assimetria:.3f} (positiva forte)',
            'interpretacao': 'Cauda longa à direita. Muitos valores muito altos.',
            'recomendacao': 'Analisar separadamente os grandes pedidos.',
            'cor': 'red'
        }
    elif -1 <= assimetria < -0.5:
        return {
            'status': '⚠️ ASSIMETRIA NEGATIVA MODERADA',
            'descricao': f'Assimetria = {assimetria:.3f} (negativa moderada)',
            'interpretacao': 'Cauda à esquerda. Prevalência de valores baixos.',
            'recomendacao': 'Rever estratégia para aumentar ticket médio.',
            'cor': 'orange'
        }
    else:
        return {
            'status': '❌ ASSIMETRIA NEGATIVA FORTE',
            'descricao': f'Assimetria = {assimetria:.3f} (negativa forte)',
            'interpretacao': 'Cauda longa à esquerda. Muitos valores muito baixos.',
            'recomendacao': 'Investigar causas dos valores baixos recorrentes.',
            'cor': 'red'
        }

def analisar_curtose(curtose):
    """Analisa o coeficiente de curtose"""
    if -0.5 <= curtose <= 0.5:
        return {
            'status': '✅ MESOCÚRTICA',
            'descricao': f'Curtose = {curtose:.3f} (similar à normal)',
            'interpretacao': 'Distribuição com altura similar à normal.',
            'recomendacao': 'Métodos estatísticos paramétricos são apropriados.',
            'cor': 'green'
        }
    elif curtose > 0.5:
        return {
            'status': '⚠️ LEPTOCÚRTICA',
            'descricao': f'Curtose = {curtose:.3f} (pico alto)',
            'interpretacao': 'Valores concentrados perto da média, caudas pesadas.',
            'recomendacao': 'Maior probabilidade de outliers extremos.',
            'cor': 'orange'
        }
    else:
        return {
            'status': '⚠️ PLATICÚRTICA',
            'descricao': f'Curtose = {curtose:.3f} (pico baixo)',
            'interpretacao': 'Valores mais espalhados, menor concentração na média.',
            'recomendacao': 'Maior variabilidade, menor previsibilidade.',
            'cor': 'orange'
        }

def analisar_outliers(n_outliers, total):
    """Analisa a presença de outliers"""
    percent = (n_outliers / total) * 100
    
    if n_outliers == 0:
        return {
            'status': '✅ SEM OUTLIERS',
            'descricao': 'Nenhum outlier detectado',
            'interpretacao': 'Dados consistentes, sem valores atípicos.',
            'recomendacao': 'Análise simplificada, todos os valores são típicos.',
            'cor': 'green'
        }
    elif percent < 5:
        return {
            'status': '⚠️ POUCOS OUTLIERS',
            'descricao': f'{n_outliers} outliers ({percent:.1f}%)',
            'interpretacao': 'Poucos valores atípicos, impacto limitado.',
            'recomendacao': 'Verificar individualmente, mas provavelmente OK.',
            'cor': 'orange'
        }
    elif percent < 10:
        return {
            'status': '⚠️ OUTLIERS MODERADOS',
            'descricao': f'{n_outliers} outliers ({percent:.1f}%)',
            'interpretacao': 'Quantidade significativa de valores atípicos.',
            'recomendacao': 'Analisar separadamente estes casos.',
            'cor': 'red'
        }
    else:
        return {
            'status': '❌ MUITOS OUTLIERS',
            'descricao': f'{n_outliers} outliers ({percent:.1f}%)',
            'interpretacao': 'Alta proporção de valores atípicos.',
            'recomendacao': 'Revisar processo de coleta/validação de dados.',
            'cor': 'darkred'
        }

def analisar_faixa_valores(minimo, maximo, media):
    """Analisa a faixa de valores"""
    amplitude = maximo - minimo
    relacao_max_media = maximo / media if media > 0 else 0
    
    if relacao_max_media < 3:
        return {
            'status': '✅ FAIXA ADEQUADA',
            'descricao': f'Amplitude: {formatar_reais(amplitude)}',
            'interpretacao': 'Faixa de valores proporcional à média.',
            'recomendacao': 'Valores dentro de expectativas razoáveis.',
            'cor': 'green'
        }
    elif relacao_max_media < 5:
        return {
            'status': '⚠️ FAIXA AMPLA',
            'descricao': f'Amplitude: {formatar_reais(amplitude)}',
            'interpretacao': 'Diferença considerável entre mínimo e máximo.',
            'recomendacao': 'Considerar segmentação por valor.',
            'cor': 'orange'
        }
    else:
        return {
            'status': '❌ FAIXA MUITO AMPLA',
            'descricao': f'Amplitude: {formatar_reais(amplitude)}',
            'interpretacao': 'Extrema diferença entre valores extremos.',
            'recomendacao': 'Investigar valores extremos individualmente.',
            'cor': 'red'
        }

# Obter diretório atual para salvar as imagens
diretorio_atual = os.getcwd()
print(f"📁 Diretório atual: {diretorio_atual}")
print(f"💾 As imagens serão salvas neste diretório")

# Carregar o DataFrame
try:
    pedidos_df = pd.read_csv("../aula9/orders.csv")
    
    if 'TotalAmount' not in pedidos_df.columns:
        print("Erro: Coluna 'TotalAmount' não encontrada")
        print(f"Colunas disponíveis: {list(pedidos_df.columns)}")
    else:
        dados_valor_total = pedidos_df['TotalAmount'].dropna()
        
        if dados_valor_total.empty:
            print("Erro: Nenhum dado disponível")
        else:
            # Cálculo das medidas estatísticas
            media_vendas = dados_valor_total.mean()
            mediana_vendas = dados_valor_total.median()
            moda_valor = dados_valor_total.mode()[0] if not dados_valor_total.mode().empty else 0
            desvio_padrao_vendas = np.std(dados_valor_total, ddof=0)
            cv_vendas = (desvio_padrao_vendas / media_vendas) * 100
            assimetria = dados_valor_total.skew()
            curtose = dados_valor_total.kurtosis()
            
            # Calcular quartis e outliers
            Q1 = dados_valor_total.quantile(0.25)
            Q3 = dados_valor_total.quantile(0.75)
            IQR = Q3 - Q1
            limite_inferior = Q1 - 1.5 * IQR
            limite_superior = Q3 + 1.5 * IQR
            outliers = dados_valor_total[(dados_valor_total < limite_inferior) | 
                                        (dados_valor_total > limite_superior)]
            n_outliers = len(outliers)
            
            # Executar todas as análises
            analise_media_mediana = analisar_media_mediana(media_vendas, mediana_vendas, dados_valor_total)
            analise_variabilidade = analisar_variabilidade(cv_vendas)
            analise_assimetria = analisar_assimetria(assimetria)
            analise_curtose = analisar_curtose(curtose)
            analise_outliers = analisar_outliers(n_outliers, len(dados_valor_total))
            analise_faixa = analisar_faixa_valores(dados_valor_total.min(), dados_valor_total.max(), media_vendas)
            
            # Criar lista para armazenar nomes dos arquivos salvos
            arquivos_salvos = []
            
            # ============================================================================
            # 1. PRIMEIRA FIGURA: HISTOGRAMA COM ANÁLISE
            # ============================================================================
            fig1, ((ax1_graph, ax1_desc), (ax1_analise, _)) = plt.subplots(2, 2, figsize=(16, 10))
            fig1.suptitle('VISUALIZAÇÃO 1: DISTRIBUIÇÃO DOS VALORES - HISTOGRAMA', 
                         fontsize=16, fontweight='bold', y=0.98)
            
            # Gráfico Histograma
            n, bins, patches = ax1_graph.hist(dados_valor_total, bins=30, edgecolor='black', 
                                            alpha=0.7, density=True, color='skyblue')
            
            ax1_graph.axvline(media_vendas, color='red', linestyle='--', linewidth=2, 
                            label=f'Média: {formatar_reais(media_vendas)}')
            
            ax1_graph.axvline(mediana_vendas, color='green', linestyle='--', linewidth=2,
                            label=f'Mediana: {formatar_reais(mediana_vendas)}')
            
            dados_valor_total.plot(kind='kde', ax=ax1_graph, color='darkblue', linewidth=2)
            
            ax1_graph.set_title('📊 HISTOGRAMA - DISTRIBUIÇÃO', fontsize=14, fontweight='bold', pad=10)
            ax1_graph.set_xlabel('Valor do Pedido (R$)', fontsize=11)
            ax1_graph.set_ylabel('Densidade', fontsize=11)
            ax1_graph.legend(fontsize=9)
            ax1_graph.grid(True, alpha=0.3)
            
            # Descrição do Histograma
            ax1_desc.axis('off')
            desc_text1 = """
            📋 GRÁFICO 1: HISTOGRAMA
            
            🎯 O QUE ESTE GRÁFICO MOSTRA:
            • Distribuição de frequência dos valores
            • Concentração dos pedidos por faixa de valor
            • Formato geral da distribuição
            
            🔍 ELEMENTOS VISUAIS:
            • Barras azuis: Quantidade em cada faixa
            • Linha vermelha: Média dos valores
            • Linha verde: Mediana (valor central)
            • Curva azul escura: Suavização da distribuição
            
            💡 COMO INTERPRETAR:
            1. Formato de sino = Distribuição normal
            2. Pico à esquerda = Maioria com valores baixos
            3. Pico à direita = Maioria com valores altos
            4. Múltiplos picos = Vários padrões de compra
            """
            
            ax1_desc.text(0, 1, desc_text1, transform=ax1_desc.transAxes, fontsize=10,
                         verticalalignment='top', fontfamily='monospace',
                         bbox=dict(boxstyle='round', facecolor='#E8F4FD', alpha=0.9, edgecolor='blue'))
            
            # ANÁLISE DETALHADA DA RELAÇÃO MÉDIA-MEDIANA
            ax1_analise.axis('off')
            
            # Calcular diferença percentual
            dif_percent = abs((media_vendas - mediana_vendas) / mediana_vendas) * 100
            direcao = "acima" if media_vendas > mediana_vendas else "abaixo"
            
            analise_text1 = f"""
            🔍 ANÁLISE: RELAÇÃO MÉDIA vs MEDIANA
            
            📊 VALORES CALCULADOS:
            • Média: {formatar_reais(media_vendas)}
            • Mediana: {formatar_reais(mediana_vendas)}
            • Diferença: {formatar_reais(abs(media_vendas - mediana_vendas))}
            • Diferença percentual: {dif_percent:.1f}%
            
            📈 {analise_media_mediana['status']}
            {analise_media_mediana['descricao']}
            
            💡 INTERPRETAÇÃO:
            {analise_media_mediana['interpretacao']}
            
            ⚠️ RECOMENDAÇÃO:
            {analise_media_mediana['recomendacao']}
            
            {"🚨 ATENÇÃO: A média está muito distante da mediana! Use a mediana como referência mais confiável." 
             if dif_percent > 30 else "✅ A média representa bem o valor típico dos pedidos."}
            """
            
            # Usar cor baseada na análise
            cor_fundo = {
                'green': '#E8F6F3',
                'orange': '#FFF3E0',
                'red': '#FFEBEE',
                'darkred': '#FCE4EC'
            }.get(analise_media_mediana['cor'], '#F5F5F5')
            
            ax1_analise.text(0, 1, analise_text1, transform=ax1_analise.transAxes, fontsize=9.5,
                           verticalalignment='top', fontfamily='monospace',
                           bbox=dict(boxstyle='round', facecolor=cor_fundo, alpha=0.9, 
                                   edgecolor=analise_media_mediana['cor']))
            
            # Remover o quarto subplot não usado
            fig1.delaxes(_)
            
            plt.tight_layout()
            
            # Salvar a figura 1
            nome_arquivo1 = '01_histograma_com_analise.png'
            caminho_completo1 = os.path.join(diretorio_atual, nome_arquivo1)
            fig1.savefig(caminho_completo1, dpi=300, bbox_inches='tight', facecolor='white')
            arquivos_salvos.append(nome_arquivo1)
            print(f"✅ Figura 1 salva como: {nome_arquivo1}")
            plt.show()
            plt.close(fig1)
            
            # ============================================================================
            # 2. SEGUNDA FIGURA: BOXPLOT COM ANÁLISE DE DISPERSÃO
            # ============================================================================
            fig2, ((ax2_graph, ax2_desc), (ax2_analise, _)) = plt.subplots(2, 2, figsize=(16, 10))
            fig2.suptitle('VISUALIZAÇÃO 2: DISPERSÃO DOS VALORES - BOXPLOT', 
                         fontsize=16, fontweight='bold', y=0.98)
            
            # Gráfico Boxplot
            box = ax2_graph.boxplot([dados_valor_total], patch_artist=True,
                                   boxprops=dict(facecolor='lightcoral', alpha=0.7),
                                   medianprops=dict(color='black', linewidth=2),
                                   whiskerprops=dict(color='gray', linewidth=1.5),
                                   capprops=dict(color='gray', linewidth=1.5),
                                   flierprops=dict(marker='o', markersize=8, 
                                                   markerfacecolor='red', alpha=0.6))
            
            ax2_graph.set_title('📦 BOXPLOT - DISPERSÃO', fontsize=14, fontweight='bold', pad=10)
            ax2_graph.set_ylabel('Valor (R$)', fontsize=11)
            ax2_graph.set_xticklabels(['Valores dos Pedidos'])
            ax2_graph.grid(True, alpha=0.3)
            
            # Adicionar estatísticas no boxplot
            ax2_graph.text(0.05, 0.95, f'Q1: {formatar_reais(Q1)}',
                          transform=ax2_graph.transAxes, fontsize=9, fontweight='bold',
                          bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            ax2_graph.text(0.05, 0.88, f'Q3: {formatar_reais(Q3)}',
                          transform=ax2_graph.transAxes, fontsize=9, fontweight='bold',
                          bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            
            # Descrição do Boxplot
            ax2_desc.axis('off')
            desc_text2 = """
            📋 GRÁFICO 2: BOXPLOT
            
            🎯 O QUE ESTE GRÁFICO MOSTRA:
            • Dispersão dos valores
            • Identificação de outliers (valores atípicos)
            • Quartis da distribuição
            
            🔍 ELEMENTOS VISUAIS:
            • Caixa laranja: Intervalo interquartil (25%-75%)
            • Linha preta: Mediana (valor central)
            • "Bigodes": Extensão dos dados normais
            • Pontos vermelhos: Outliers
            
            📊 QUARTIS:
            • Q1: 25% dos valores são menores
            • Q3: 75% dos valores são menores
            • IQR = Q3 - Q1 (dispersão central)
            """
            
            ax2_desc.text(0, 1, desc_text2, transform=ax2_desc.transAxes, fontsize=10,
                         verticalalignment='top', fontfamily='monospace',
                         bbox=dict(boxstyle='round', facecolor='#FFF0F0', alpha=0.9, edgecolor='red'))
            
            # ANÁLISE DETALHADA DE DISPERSÃO E OUTLIERS
            ax2_analise.axis('off')
            
            analise_text2 = f"""
            🔍 ANÁLISE: DISPERSÃO E OUTLIERS
            
            📊 MEDIDAS DE DISPERSÃO:
            • Desvio Padrão: {formatar_reais(desvio_padrao_vendas)}
            • Coef. Variação (CV): {cv_vendas:.1f}%
            • Intervalo Interquartil (IQR): {formatar_reais(IQR)}
            
            📈 {analise_variabilidade['status']}
            {analise_variabilidade['descricao']}
            
            💡 INTERPRETAÇÃO DA VARIABILIDADE:
            {analise_variabilidade['interpretacao']}
            
            ⚠️ {analise_outliers['status']}
            {analise_outliers['descricao']}
            
            🔍 INTERPRETAÇÃO DOS OUTLIERS:
            {analise_outliers['interpretacao']}
            
            📌 RECOMENDAÇÕES:
            1. {analise_variabilidade['recomendacao']}
            2. {analise_outliers['recomendacao']}
            
            {"🚨 ALERTA: Alta variabilidade pode indicar múltiplos perfis de cliente!" 
             if cv_vendas > 50 else "✅ Variabilidade dentro dos limites esperados."}
            """
            
            # Cor para análise de variabilidade (a mais crítica)
            cor_critica = analise_variabilidade['cor'] if cv_vendas > 30 else analise_outliers['cor']
            cor_fundo2 = {
                'green': '#E8F6F3',
                'orange': '#FFF3E0',
                'red': '#FFEBEE',
                'darkred': '#FCE4EC'
            }.get(cor_critica, '#F5F5F5')
            
            ax2_analise.text(0, 1, analise_text2, transform=ax2_analise.transAxes, fontsize=9.5,
                           verticalalignment='top', fontfamily='monospace',
                           bbox=dict(boxstyle='round', facecolor=cor_fundo2, alpha=0.9, 
                                   edgecolor=cor_critica))
            
            # Remover o quarto subplot não usado
            fig2.delaxes(_)
            
            plt.tight_layout()
            
            # Salvar a figura 2
            nome_arquivo2 = '02_boxplot_com_analise.png'
            caminho_completo2 = os.path.join(diretorio_atual, nome_arquivo2)
            fig2.savefig(caminho_completo2, dpi=300, bbox_inches='tight', facecolor='white')
            arquivos_salvos.append(nome_arquivo2)
            print(f"✅ Figura 2 salva como: {nome_arquivo2}")
            plt.show()
            plt.close(fig2)
            
            # ============================================================================
            # 3. TERCEIRA FIGURA: TENDÊNCIA CENTRAL COMPARATIVA
            # ============================================================================
            fig3, ((ax3_graph, ax3_desc), (ax3_analise, _)) = plt.subplots(2, 2, figsize=(16, 10))
            fig3.suptitle('VISUALIZAÇÃO 3: TENDÊNCIA CENTRAL - COMPARAÇÃO DETALHADA', 
                         fontsize=16, fontweight='bold', y=0.98)
            
            # Gráfico de Barras
            medidas = ['MÉDIA', 'MEDIANA', 'MODA']
            valores = [media_vendas, mediana_vendas, moda_valor]
            cores = ['#FF6B6B', '#4ECDC4', '#45B7D1']
            
            bars = ax3_graph.bar(medidas, valores, color=cores, edgecolor='black', 
                               linewidth=1.5, alpha=0.8)
            
            ax3_graph.set_title('📈 MEDIDAS DE TENDÊNCIA CENTRAL', 
                              fontsize=14, fontweight='bold', pad=10)
            ax3_graph.set_ylabel('Valor (R$)', fontsize=11)
            
            # Adicionar valores nas barras
            for bar, valor, medida in zip(bars, valores, medidas):
                height = bar.get_height()
                ax3_graph.text(bar.get_x() + bar.get_width()/2., height + 0.01*max(valores),
                             f'{formatar_reais(valor)}',
                             ha='center', va='bottom', fontsize=11, fontweight='bold')
            
            ax3_graph.grid(True, alpha=0.3, axis='y')
            
            # Descrição das Medidas
            ax3_desc.axis('off')
            desc_text3 = """
            📋 GRÁFICO 3: TENDÊNCIA CENTRAL
            
            🎯 O QUE ESTE GRÁFICO MOSTRA:
            • Comparação dos valores centrais
            • Diferenças entre as medidas
            • Possíveis distorções nos dados
            
            🔍 SIGNIFICADO DE CADA MEDIDA:
            
            📊 MÉDIA (Vermelha):
            • Soma total ÷ número de pedidos
            • Sensível a valores extremos
            
            📊 MEDIANA (Verde-água):
            • Valor do meio quando ordenados
            • NÃO é afetada por outliers
            
            📊 MODA (Azul):
            • Valor que mais se repete
            • Mostra padrão mais frequente
            """
            
            ax3_desc.text(0, 1, desc_text3, transform=ax3_desc.transAxes, fontsize=10,
                         verticalalignment='top', fontfamily='monospace',
                         bbox=dict(boxstyle='round', facecolor='#F0FFF4', alpha=0.9, edgecolor='green'))
            
            # ANÁLISE COMPARATIVA DETALHADA
            ax3_analise.axis('off')
            
            # Calcular relações entre as medidas
            dif_media_mediana = ((media_vendas - mediana_vendas) / mediana_vendas) * 100
            dif_media_moda = ((media_vendas - moda_valor) / moda_valor) * 100 if moda_valor > 0 else 0
            
            analise_text3 = f"""
            🔍 ANÁLISE COMPARATIVA DETALHADA
            
            📊 RELAÇÕES ENTRE AS MEDIDAS:
            • Média vs Mediana: {dif_media_mediana:+.1f}%
            • Média vs Moda: {dif_media_moda:+.1f}%
            • Mediana vs Moda: {((mediana_vendas - moda_valor)/moda_valor*100):+.1f}%
            
            📈 SIGNIFICADO DAS DIFERENÇAS:
            
            {analise_media_mediana['status']}
            • {analise_media_mediana['interpretacao']}
            
            💡 IMPLICAÇÕES PARA DECISÕES:
            
            1. PARA PREÇOS E PROMOÇÕES:
            • {'Focar no valor médio' if dif_media_mediana < 10 else 'Usar mediana como referência'}
            
            2. PARA ESTOQUE E PRODUÇÃO:
            • {'Planejar baseado na moda' if dif_media_moda < 20 else 'Planejar baseado na mediana'}
            
            3. PARA META DE VENDAS:
            • {'Meta realista próxima à média' if dif_media_mediana < 15 else 'Meta baseada na mediana'}
            
            🎯 CONCLUSÃO PRINCIPAL:
            {"✅ Use a MÉDIA como principal referência" if dif_media_mediana < 10 
             else "⚠️ Use a MEDIANA como referência mais confiável" 
             if dif_media_mediana < 30 else "🚨 Use a MEDIANA, a média está muito distorcida!"}
            """
            
            # Determinar cor baseada na maior diferença
            maior_dif = max(abs(dif_media_mediana), abs(dif_media_moda))
            if maior_dif < 15:
                cor_analise = 'green'
                cor_fundo3 = '#E8F6F3'
            elif maior_dif < 30:
                cor_analise = 'orange'
                cor_fundo3 = '#FFF3E0'
            else:
                cor_analise = 'red'
                cor_fundo3 = '#FFEBEE'
            
            ax3_analise.text(0, 1, analise_text3, transform=ax3_analise.transAxes, fontsize=9.5,
                           verticalalignment='top', fontfamily='monospace',
                           bbox=dict(boxstyle='round', facecolor=cor_fundo3, alpha=0.9, 
                                   edgecolor=cor_analise))
            
            # Remover o quarto subplot não usado
            fig3.delaxes(_)
            
            plt.tight_layout()
            
            # Salvar a figura 3
            nome_arquivo3 = '03_tendencia_central_com_analise.png'
            caminho_completo3 = os.path.join(diretorio_atual, nome_arquivo3)
            fig3.savefig(caminho_completo3, dpi=300, bbox_inches='tight', facecolor='white')
            arquivos_salvos.append(nome_arquivo3)
            print(f"✅ Figura 3 salva como: {nome_arquivo3}")
            plt.show()
            plt.close(fig3)
            
            # ============================================================================
            # 4. QUARTA FIGURA: FORMA DA DISTRIBUIÇÃO
            # ============================================================================
            fig4, ((ax4_graph, ax4_desc), (ax4_analise, _)) = plt.subplots(2, 2, figsize=(16, 10))
            fig4.suptitle('VISUALIZAÇÃO 4: FORMA DA DISTRIBUIÇÃO - ASSIMETRIA E CURTOSE', 
                         fontsize=16, fontweight='bold', y=0.98)
            
            # Gráfico de Pizza
            if -0.5 <= assimetria <= 0.5:
                simetria_class = 'SIMÉTRICA'
                simetria_cor = '#2ECC71'
                simetria_icon = '⚖️'
            elif assimetria > 0.5:
                simetria_class = 'POSITIVA'
                simetria_cor = '#E74C3C'
                simetria_icon = '↗️'
            else:
                simetria_class = 'NEGATIVA'
                simetria_cor = '#3498DB'
                simetria_icon = '↙️'
            
            if curtose > 0:
                curtose_class = 'LEPTOCÚRTICA'
                curtose_cor = '#F39C12'
                curtose_icon = '📈'
            elif curtose < 0:
                curtose_class = 'PLATICÚRTICA'
                curtose_cor = '#9B59B6'
                curtose_icon = '📉'
            else:
                curtose_class = 'MESOCÚRTICA'
                curtose_cor = '#1ABC9C'
                curtose_icon = '📊'
            
            labels = [f'ASSIMETRIA\n{simetria_icon}', f'CURTOSE\n{curtose_icon}']
            sizes = [abs(assimetria) + 1, abs(curtose) + 1]
            colors = [simetria_cor, curtose_cor]
            
            wedges, texts, autotexts = ax4_graph.pie(sizes, labels=labels, colors=colors,
                                                    autopct='%1.1f%%', startangle=90,
                                                    textprops=dict(fontsize=10, fontweight='bold'))
            
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            
            ax4_graph.set_title('🥧 FORMA DA DISTRIBUIÇÃO', 
                              fontsize=14, fontweight='bold', pad=10)
            
            # Descrição da Forma
            ax4_desc.axis('off')
            desc_text4 = """
            📋 GRÁFICO 4: FORMA DA DISTRIBUIÇÃO
            
            🎯 O QUE ESTE GRÁFICO MOSTRA:
            • Tipo de assimetria dos dados
            • Grau de achatamento (curtose)
            • Formato geral da distribuição
            
            🔍 ASSIMETRIA:
            • Mede o equilíbrio da distribuição
            • Positiva: cauda à direita
            • Negativa: cauda à esquerda
            
            🔍 CURTOSE:
            • Mede o "achatamento"
            • Leptocúrtica: pico alto
            • Platicúrtica: pico baixo
            • Mesocúrtica: normal
            """
            
            ax4_desc.text(0, 1, desc_text4, transform=ax4_desc.transAxes, fontsize=10,
                         verticalalignment='top', fontfamily='monospace',
                         bbox=dict(boxstyle='round', facecolor='#FDF0FF', alpha=0.9, edgecolor='purple'))
            
            # ANÁLISE DETALHADA DA FORMA
            ax4_analise.axis('off')
            
            # Determinar impacto combinado
            impacto_assimetria = "significativo" if abs(assimetria) > 0.5 else "moderado"
            impacto_curtose = "importante" if abs(curtose) > 0.5 else "limitado"
            
            analise_text4 = f"""
            🔍 ANÁLISE DETALHADA DA FORMA
            
            📊 VALORES CALCULADOS:
            • Assimetria: {assimetria:.3f}
            • Curtose: {curtose:.3f}
            
            📈 {analise_assimetria['status']}
            {analise_assimetria['descricao']}
            
            💡 INTERPRETAÇÃO DA ASSIMETRIA:
            {analise_assimetria['interpretacao']}
            
            📈 {analise_curtose['status']}
            {analise_curtose['descricao']}
            
            💡 INTERPRETAÇÃO DA CURTOSE:
            {analise_curtose['interpretacao']}
            
            ⚠️ IMPLICAÇÕES COMBINADAS:
            
            1. PARA ANÁLISE ESTATÍSTICA:
            • {'Métodos paramétricos apropriados' if abs(assimetria) < 0.5 and abs(curtose) < 0.5 
               else 'Considerar métodos não-paramétricos'}
            
            2. PARA GESTÃO DE RISCO:
            • {'Risco moderado de valores extremos' if curtose > 0 
               else 'Risco distribuído mais uniformemente'}
            
            3. PARA PREVISÕES:
            • {'Previsões mais confiáveis' if abs(assimetria) < 0.5 
               else 'Maior incerteza nas previsões'}
            
            🎯 IMPACTO GERAL:
            • Assimetria: {impacto_assimetria}
            • Curtose: {impacto_curtose}
            {"✅ Forma adequada para análise estatística padrão" 
             if abs(assimetria) < 0.5 and abs(curtose) < 0.5 else "⚠️ Forma requer cuidados na análise"}
            """
            
            # Cor baseada na assimetria (geralmente mais impactante)
            cor_analise4 = analise_assimetria['cor']
            cor_fundo4 = {
                'green': '#E8F6F3',
                'orange': '#FFF3E0',
                'red': '#FFEBEE'
            }.get(cor_analise4, '#F5F5F5')
            
            ax4_analise.text(0, 1, analise_text4, transform=ax4_analise.transAxes, fontsize=9.5,
                           verticalalignment='top', fontfamily='monospace',
                           bbox=dict(boxstyle='round', facecolor=cor_fundo4, alpha=0.9, 
                                   edgecolor=cor_analise4))
            
            # Remover o quarto subplot não usado
            fig4.delaxes(_)
            
            plt.tight_layout()
            
            # Salvar a figura 4
            nome_arquivo4 = '04_forma_distribuicao_com_analise.png'
            caminho_completo4 = os.path.join(diretorio_atual, nome_arquivo4)
            fig4.savefig(caminho_completo4, dpi=300, bbox_inches='tight', facecolor='white')
            arquivos_salvos.append(nome_arquivo4)
            print(f"✅ Figura 4 salva como: {nome_arquivo4}")
            plt.show()
            plt.close(fig4)
            
            # ============================================================================
            # 5. QUINTA FIGURA: RESUMO ESTATÍSTICO COMPLETO
            # ============================================================================
            fig5, (ax5_table, ax5_analise) = plt.subplots(1, 2, figsize=(18, 10))
            fig5.suptitle('VISUALIZAÇÃO 5: RESUMO ESTATÍSTICO COMPLETO COM ANÁLISE', 
                         fontsize=16, fontweight='bold', y=0.98)
            
            # Tabela de Resumo
            ax5_table.axis('tight')
            ax5_table.axis('off')
            
            # Criar dados para a tabela com status coloridos
            estatisticas = [
                ["📊 DADOS GERAIS", "", ""],
                ["Nº de Pedidos", f"{len(dados_valor_total):,}".replace(',', '.'), "📋"],
                ["", "", ""],
                ["🎯 TENDÊNCIA CENTRAL", "", ""],
                ["Média", formatar_reais(media_vendas), analise_media_mediana['status'][:1]],
                ["Mediana", formatar_reais(mediana_vendas), analise_media_mediana['status'][:1]],
                ["Moda", formatar_reais(moda_valor), "📊"],
                ["", "", ""],
                ["📈 DISPERSÃO", "", ""],
                ["Desvio Padrão", formatar_reais(desvio_padrao_vendas), "📏"],
                ["Coef. Variação", f"{cv_vendas:.1f}%", analise_variabilidade['status'][:1]],
                ["", "", ""],
                ["🔍 FORMA", "", ""],
                ["Assimetria", f"{assimetria:.3f}", analise_assimetria['status'][:1]],
                ["Curtose", f"{curtose:.3f}", analise_curtose['status'][:1]],
                ["", "", ""],
                ["💰 VALORES EXTREMOS", "", ""],
                ["Mínimo", formatar_reais(dados_valor_total.min()), "📉"],
                ["Máximo", formatar_reais(dados_valor_total.max()), "📈"],
                ["Amplitude", formatar_reais(dados_valor_total.max()-dados_valor_total.min()), analise_faixa['status'][:1]],
                ["", "", ""],
                ["⚠️ OUTLIERS", "", ""],
                ["Detectados", f"{n_outliers}", analise_outliers['status'][:1]],
                ["Percentual", f"{(n_outliers/len(dados_valor_total)*100):.1f}%", analise_outliers['status'][:1]]
            ]
            
            # Criar tabela
            tabela = ax5_table.table(cellText=estatisticas, 
                                    cellLoc='left', 
                                    colWidths=[0.25, 0.20, 0.05],
                                    loc='center',
                                    cellColours=[['#F8F9F9', '#FFFFFF', '#F0F0F0']] * len(estatisticas))
            
            tabela.auto_set_font_size(False)
            tabela.set_fontsize(10)
            tabela.scale(1, 1.8)
            
            # Colorir células baseado nas análises
            for i, (label, valor, status) in enumerate(estatisticas):
                if "Média" in label or "Mediana" in label:
                    tabela[(i, 2)].set_facecolor(analise_media_mediana['cor'])
                elif "Coef. Variação" in label:
                    tabela[(i, 2)].set_facecolor(analise_variabilidade['cor'])
                elif "Assimetria" in label:
                    tabela[(i, 2)].set_facecolor(analise_assimetria['cor'])
                elif "Curtose" in label:
                    tabela[(i, 2)].set_facecolor(analise_curtose['cor'])
                elif "Amplitude" in label:
                    tabela[(i, 2)].set_facecolor(analise_faixa['cor'])
                elif "Detectados" in label or "Percentual" in label:
                    tabela[(i, 2)].set_facecolor(analise_outliers['cor'])
                elif any(x in label for x in ["DADOS", "TENDÊNCIA", "DISPERSÃO", "FORMA", "VALORES", "OUTLIERS"]):
                    tabela[(i, 0)].set_facecolor('#34495E')
                    tabela[(i, 0)].set_text_props(color='white', weight='bold', fontsize=11)
                    tabela[(i, 1)].set_facecolor('#34495E')
                    tabela[(i, 2)].set_facecolor('#34495E')
            
            ax5_table.set_title('📋 RESUMO ESTATÍSTICO NUMÉRICO', 
                              fontsize=14, fontweight='bold', pad=20, y=1.02)
            
            # ANÁLISE FINAL CONSOLIDADA
            ax5_analise.axis('off')
            
            # Determinar avaliação geral
            problemas = []
            if analise_media_mediana['cor'] in ['orange', 'red', 'darkred']:
                problemas.append("Relação média-mediana")
            if analise_variabilidade['cor'] in ['orange', 'red', 'darkred']:
                problemas.append("Variabilidade")
            if analise_assimetria['cor'] in ['orange', 'red', 'darkred']:
                problemas.append("Assimetria")
            if analise_outliers['cor'] in ['orange', 'red', 'darkred']:
                problemas.append("Outliers")
            
            avaliacao_geral = "EXCELENTE" if len(problemas) == 0 else "BOA" if len(problemas) <= 1 else "REGULAR" if len(problemas) <= 2 else "CRÍTICA"
            
            analise_text5 = f"""
            🔍 ANÁLISE FINAL CONSOLIDADA
            
            📊 AVALIAÇÃO GERAL: {avaliacao_geral}
            {"✅ Todos os indicadores dentro do esperado" if len(problemas) == 0 
             else f"⚠️ Atenção necessária em: {', '.join(problemas)}"}
            
            🎯 PRINCIPAIS CONCLUSÕES:
            
            1. VALOR TÍPICO DOS PEDIDOS:
            • {formatar_reais(media_vendas)} (média)
            • {analise_media_mediana['interpretacao'].split('.')[0]}.
            
            2. CONSISTÊNCIA DOS DADOS:
            • {analise_variabilidade['descricao']}
            • {analise_variabilidade['interpretacao'].split('.')[0]}.
            
            3. FORMA DA DISTRIBUIÇÃO:
            • {analise_assimetria['descricao']}
            • {analise_curtose['descricao']}
            
            4. QUALIDADE DOS DADOS:
            • {analise_outliers['descricao']}
            • {analise_outliers['interpretacao'].split('.')[0]}.
            
            💡 RECOMENDAÇÕES PRIORITÁRIAS:
            
            1. PARA TOMADA DE DECISÃO:
            • {analise_media_mediana['recomendacao']}
            
            2. PARA CONTROLE DE QUALIDADE:
            • {analise_outliers['recomendacao']}
            
            3. PARA PLANEJAMENTO:
            • {analise_variabilidade['recomendacao']}
            
            🚨 ALERTAS IMPORTANTES:
            {f"• Média muito diferente da mediana: use mediana como referência!" 
             if analise_media_mediana['cor'] in ['red', 'darkred'] else ""}
            {f"• Alta variabilidade: segmentar análise!" 
             if analise_variabilidade['cor'] in ['red', 'darkred'] else ""}
            {f"• Muitos outliers: investigar causas!" 
             if analise_outliers['cor'] in ['red', 'darkred'] else ""}
            
            📈 STATUS: {avaliacao_geral}
            {"✅ Dados adequados para análise e decisão" if avaliacao_geral in ["EXCELENTE", "BOA"] 
             else "⚠️ Dados requerem atenção especial"}
            """
            
            # Cor baseada na avaliação geral
            if avaliacao_geral == "EXCELENTE":
                cor_geral = 'green'
                cor_fundo5 = '#E8F6F3'
            elif avaliacao_geral == "BOA":
                cor_geral = 'lightgreen'
                cor_fundo5 = '#F1F8E9'
            elif avaliacao_geral == "REGULAR":
                cor_geral = 'orange'
                cor_fundo5 = '#FFF3E0'
            else:
                cor_geral = 'red'
                cor_fundo5 = '#FFEBEE'
            
            ax5_analise.text(0, 1, analise_text5, transform=ax5_analise.transAxes, fontsize=10,
                           verticalalignment='top', fontfamily='monospace',
                           bbox=dict(boxstyle='round', facecolor=cor_fundo5, alpha=0.9, 
                                   edgecolor=cor_geral, linewidth=2))
            
            plt.tight_layout()
            
            # Salvar a figura 5
            nome_arquivo5 = '05_resumo_completo_com_analise.png'
            caminho_completo5 = os.path.join(diretorio_atual, nome_arquivo5)
            fig5.savefig(caminho_completo5, dpi=300, bbox_inches='tight', facecolor='white')
            arquivos_salvos.append(nome_arquivo5)
            print(f"✅ Figura 5 salva como: {nome_arquivo5}")
            plt.show()
            plt.close(fig5)
            
            # ============================================================================
            # RESUMO FINAL NO CONSOLE COM ANÁLISE DETALHADA
            # ============================================================================
            print("\n" + "="*100)
            print(" " * 35 + "📊 RELATÓRIO ANALÍTICO DETALHADO")
            print("="*100)
            
            print(f"\n📁 ARQUIVOS GERADOS:")
            for i, arquivo in enumerate(arquivos_salvos, 1):
                print(f"   {i:2d}. {arquivo}")
            
            print(f"\n🔍 ANÁLISE DETALHADA DOS RESULTADOS:")
            print("-" * 50)
            
            print(f"\n1. RELAÇÃO MÉDIA-MEDIANA:")
            print(f"   • Média: {formatar_reais(media_vendas)}")
            print(f"   • Mediana: {formatar_reais(mediana_vendas)}")
            dif_percent = abs((media_vendas - mediana_vendas) / mediana_vendas) * 100
            print(f"   • Diferença: {dif_percent:.1f}%")
            print(f"   • STATUS: {analise_media_mediana['status']}")
            print(f"   • {analise_media_mediana['interpretacao']}")
            if dif_percent > 30:
                print(f"   🚨 ALERTA: A mediana dos valores é muito diferente da média!")
                print(f"      Isso indica que valores extremos estão distorcendo a média.")
                print(f"      Use a mediana ({formatar_reais(mediana_vendas)}) como referência mais confiável.")
            
            print(f"\n2. VARIABILIDADE DOS DADOS:")
            print(f"   • Coeficiente de Variação: {cv_vendas:.1f}%")
            print(f"   • STATUS: {analise_variabilidade['status']}")
            print(f"   • {analise_variabilidade['interpretacao']}")
            if cv_vendas > 50:
                print(f"   ⚠️  ATENÇÃO: Variabilidade muito alta!")
                print(f"      Considere segmentar a análise por faixa de valor.")
            
            print(f"\n3. FORMA DA DISTRIBUIÇÃO:")
            print(f"   • Assimetria: {assimetria:.3f} ({analise_assimetria['status']})")
            print(f"   • Curtose: {curtose:.3f} ({analise_curtose['status']})")
            print(f"   • {analise_assimetria['interpretacao']}")
            if abs(assimetria) > 1:
                print(f"   🔍 OBSERVAÇÃO: Assimetria forte detectada.")
                print(f"      Distribuição inclinada para valores {'altos' if assimetria > 0 else 'baixos'}.")
            
            print(f"\n4. OUTLIERS E VALORES ATÍPICOS:")
            print(f"   • Outliers detectados: {n_outliers}")
            print(f"   • Percentual: {(n_outliers/len(dados_valor_total)*100):.1f}%")
            print(f"   • STATUS: {analise_outliers['status']}")
            print(f"   • {analise_outliers['interpretacao']}")
            if n_outliers > 0:
                print(f"   📊 SUGESTÃO: Analisar separadamente os {n_outliers} valores atípicos.")
            
            print(f"\n5. FAIXA DE VALORES:")
            print(f"   • Mínimo: {formatar_reais(dados_valor_total.min())}")
            print(f"   • Máximo: {formatar_reais(dados_valor_total.max())}")
            print(f"   • Amplitude: {formatar_reais(dados_valor_total.max()-dados_valor_total.min())}")
            print(f"   • STATUS: {analise_faixa['status']}")
            
            print(f"\n🎯 AVALIAÇÃO FINAL: {avaliacao_geral}")
            if len(problemas) > 0:
                print(f"   • Pontos de atenção: {', '.join(problemas)}")
            else:
                print(f"   ✅ Todos os indicadores dentro do esperado")
            
            print(f"\n💡 RECOMENDAÇÕES PRINCIPAIS:")
            print(f"   1. {analise_media_mediana['recomendacao']}")
            print(f"   2. {analise_variabilidade['recomendacao']}")
            if n_outliers > 0:
                print(f"   3. {analise_outliers['recomendacao']}")
            
            print("\n" + "="*100)
            print(f"✅ ANÁLISE COMPLETA - {len(arquivos_salvos)} IMAGENS SALVAS")
            print(f"   📁 Diretório: {diretorio_atual}")
            print("="*100)

except FileNotFoundError:
    print("❌ Erro: Arquivo 'orders.csv' não encontrado")
    print("   Caminho especificado: ../aula9/orders.csv")
    print("   Verifique se o arquivo existe no diretório correto")
except Exception as e:
    print(f"❌ Erro inesperado: {str(e)}")
    import traceback
    traceback.print_exc()