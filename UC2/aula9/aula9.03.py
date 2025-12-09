import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Configurar estilo dos gráficos
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

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
            variancia_vendas = np.var(dados_valor_total, ddof=0)
            desvio_padrao_vendas = np.std(dados_valor_total, ddof=0)
            cv_vendas = (desvio_padrao_vendas / media_vendas) * 100
            distancia_vendas = variancia_vendas / (media_vendas ** 2)
            assimetria = dados_valor_total.skew()
            curtose = dados_valor_total.kurtosis()
            
            # Criar figura principal com subplots
            fig = plt.figure(figsize=(18, 12))
            
            # 1. GRÁFICO 1: Histograma com distribuição e medidas
            ax1 = plt.subplot(3, 3, 1)
            n, bins, patches = ax1.hist(dados_valor_total, bins=30, edgecolor='black', alpha=0.7, 
                                       density=True, color='skyblue')
            
            # Adicionar linha da média
            ax1.axvline(media_vendas, color='red', linestyle='--', linewidth=2, 
                       label=f'Média: R$ {media_vendas:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'))
            
            # Adicionar linha da mediana
            ax1.axvline(mediana_vendas, color='green', linestyle='--', linewidth=2,
                       label=f'Mediana: R$ {mediana_vendas:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'))
            
            # Adicionar curva de densidade KDE
            dados_valor_total.plot(kind='kde', ax=ax1, color='darkblue', linewidth=2)
            
            ax1.set_title('Distribuição dos Valores Totais', fontsize=14, fontweight='bold')
            ax1.set_xlabel('Valor (R$)', fontsize=12)
            ax1.set_ylabel('Densidade', fontsize=12)
            ax1.legend(fontsize=10)
            ax1.grid(True, alpha=0.3)
            
            # 2. GRÁFICO 2: Boxplot para análise de dispersão
            ax2 = plt.subplot(3, 3, 2)
            boxplot_data = [dados_valor_total]
            box = ax2.boxplot(boxplot_data, patch_artist=True, 
                             boxprops=dict(facecolor='lightcoral'),
                             medianprops=dict(color='black', linewidth=2),
                             whiskerprops=dict(color='gray', linewidth=1.5),
                             capprops=dict(color='gray', linewidth=1.5))
            
            # Adicionar pontos outliers
            outliers = dados_valor_total[dados_valor_total > dados_valor_total.quantile(0.75) + 
                                        1.5*(dados_valor_total.quantile(0.75)-dados_valor_total.quantile(0.25))]
            if len(outliers) > 0:
                ax2.scatter([1]*len(outliers), outliers, color='red', alpha=0.6, 
                          s=50, label=f'Outliers: {len(outliers)}')
            
            ax2.set_title('Boxplot - Análise de Dispersão', fontsize=14, fontweight='bold')
            ax2.set_ylabel('Valor (R$)', fontsize=12)
            ax2.set_xticklabels(['Valores Totais'])
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            
            # 3. GRÁFICO 3: Gráfico de barras para medidas de tendência central
            ax3 = plt.subplot(3, 3, 3)
            medidas = ['Média', 'Mediana', 'Moda']
            valores = [media_vendas, mediana_vendas, dados_valor_total.mode()[0]]
            cores = ['#FF6B6B', '#4ECDC4', '#45B7D1']
            
            bars = ax3.bar(medidas, valores, color=cores, edgecolor='black', linewidth=1.5)
            ax3.set_title('Medidas de Tendência Central', fontsize=14, fontweight='bold')
            ax3.set_ylabel('Valor (R$)', fontsize=12)
            
            # Adicionar valores nas barras
            for bar, valor in zip(bars, valores):
                height = bar.get_height()
                ax3.text(bar.get_x() + bar.get_width()/2., height + 0.01*max(valores),
                        f'R$ {valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'),
                        ha='center', va='bottom', fontsize=10)
            
            ax3.grid(True, alpha=0.3, axis='y')
            
            # 4. GRÁFICO 4: Medidas de dispersão (gráfico de radar)
            ax4 = plt.subplot(3, 3, 4, projection='polar')
            
            categorias = ['Variância', 'Desvio Padrão', 'CV (%)', 'Amplitude']
            valores_disp = [variancia_vendas, desvio_padrao_vendas, cv_vendas, 
                          dados_valor_total.max() - dados_valor_total.min()]
            
            # Normalizar valores para o gráfico radar
            valores_norm = [v/max(valores_disp)*100 for v in valores_disp]
            valores_norm += valores_norm[:1]  # Fechar o polígono
            
            angles = np.linspace(0, 2*np.pi, len(categorias), endpoint=False).tolist()
            angles += angles[:1]
            
            ax4.plot(angles, valores_norm, 'o-', linewidth=2, color='purple')
            ax4.fill(angles, valores_norm, alpha=0.25, color='purple')
            ax4.set_xticks(angles[:-1])
            ax4.set_xticklabels(categorias, fontsize=10)
            ax4.set_title('Medidas de Dispersão (Normalizadas)', fontsize=12, fontweight='bold')
            ax4.grid(True)
            
            # 5. GRÁFICO 5: Gráfico de pizza para análise de simetria e curtose
            ax5 = plt.subplot(3, 3, 5)
            
            # Determinar classificação
            if -0.5 <= assimetria <= 0.5:
                simetria_class = 'Simétrica'
                simetria_cor = '#2ECC71'
            elif assimetria > 0.5:
                simetria_class = 'Positiva'
                simetria_cor = '#E74C3C'
            else:
                simetria_class = 'Negativa'
                simetria_cor = '#3498DB'
            
            if curtose > 0:
                curtose_class = 'Leptocúrtica'
                curtose_cor = '#F39C12'
            elif curtose < 0:
                curtose_class = 'Platicúrtica'
                curtose_cor = '#9B59B6'
            else:
                curtose_class = 'Mesocúrtica'
                curtose_cor = '#1ABC9C'
            
            labels = [f'Assimetria: {simetria_class}', f'Curtose: {curtose_class}']
            sizes = [abs(assimetria), abs(curtose)]
            colors = [simetria_cor, curtose_cor]
            
            wedges, texts, autotexts = ax5.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                                              startangle=90, textprops=dict(fontsize=10))
            
            ax5.set_title('Assimetria e Curtose', fontsize=14, fontweight='bold')
            
            # 6. GRÁFICO 6: QQ-Plot para análise de normalidade
            ax6 = plt.subplot(3, 3, 6)
            stats.probplot(dados_valor_total, dist="norm", plot=ax6)
            ax6.get_lines()[0].set_marker('o')
            ax6.get_lines()[0].set_markersize(4)
            ax6.get_lines()[0].set_alpha(0.6)
            ax6.get_lines()[1].set_linewidth(2)
            ax6.get_lines()[1].set_color('red')
            ax6.set_title('QQ-Plot - Teste de Normalidade', fontsize=14, fontweight='bold')
            ax6.grid(True, alpha=0.3)
            
            # 7. GRÁFICO 7: Gráfico de violino para distribuição
            ax7 = plt.subplot(3, 3, 7)
            violin_parts = ax7.violinplot([dados_valor_total], showmeans=True, showmedians=True)
            
            # Colorir o violino
            for pc in violin_parts['bodies']:
                pc.set_facecolor('#FFD700')
                pc.set_alpha(0.7)
            
            ax7.set_title('Gráfico de Violino', fontsize=14, fontweight='bold')
            ax7.set_ylabel('Valor (R$)', fontsize=12)
            ax7.set_xticklabels([''])
            ax7.grid(True, alpha=0.3)
            
            # 8. GRÁFICO 8: Resumo estatístico em tabela
            ax8 = plt.subplot(3, 3, 8)
            ax8.axis('tight')
            ax8.axis('off')
            
            # Criar tabela com resumo
            resumo_data = [
                ["Estatística", "Valor", "Interpretação"],
                ["Nº de Pedidos", f"{len(dados_valor_total):,}".replace(',', '.'), "Total analisado"],
                ["Média", f"R$ {media_vendas:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'), "Valor médio"],
                ["Mediana", f"R$ {mediana_vendas:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'), "Valor central"],
                ["Desvio Padrão", f"R$ {desvio_padrao_vendas:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'), "Dispersão absoluta"],
                ["CV", f"{cv_vendas:.1f}%", "Dispersão relativa"],
                ["Assimetria", f"{assimetria:.3f}", simetria_class],
                ["Curtose", f"{curtose:.3f}", curtose_class],
                ["Mínimo", f"R$ {dados_valor_total.min():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'), "Valor mínimo"],
                ["Máximo", f"R$ {dados_valor_total.max():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'), "Valor máximo"]
            ]
            
            tabela = ax8.table(cellText=resumo_data, cellLoc='left', 
                              colWidths=[0.25, 0.25, 0.4],
                              loc='center', fontsize=10)
            tabela.auto_set_font_size(False)
            tabela.set_fontsize(9)
            tabela.scale(1, 1.5)
            
            # Colorir cabeçalho
            for i in range(3):
                tabela[(0, i)].set_facecolor('#34495E')
                tabela[(0, i)].set_text_props(weight='bold', color='white')
            
            ax8.set_title('Resumo Estatístico Completo', fontsize=14, fontweight='bold', pad=20)
            
            # 9. GRÁFICO 9: Histograma cumulativo
            ax9 = plt.subplot(3, 3, 9)
            
            # Histograma normal
            n, bins, patches = ax9.hist(dados_valor_total, bins=30, edgecolor='black', 
                                       alpha=0.5, color='lightblue', density=True, 
                                       label='Frequência')
            
            # Linha cumulativa
            hist, bin_edges = np.histogram(dados_valor_total, bins=30, density=True)
            cumsum = np.cumsum(hist) * np.diff(bin_edges)
            ax9.plot(bin_edges[1:], cumsum, 'r-', linewidth=2, label='Distribuição Acumulada')
            
            ax9.set_title('Histograma com Distribuição Acumulada', fontsize=14, fontweight='bold')
            ax9.set_xlabel('Valor (R$)', fontsize=12)
            ax9.set_ylabel('Densidade / Cumulativa', fontsize=12)
            ax9.legend(loc='upper left')
            ax9.grid(True, alpha=0.3)
            
            # Ajustar layout
            plt.suptitle('ANÁLISE ESTATÍSTICA COMPLETA - VALORES TOTAIS DOS PEDIDOS', 
                        fontsize=16, fontweight='bold', y=0.98)
            plt.tight_layout()
            plt.show()
            
            # GRÁFICO EXTRA: Scatter plot temporal (se houver coluna de data)
            if 'OrderDate' in pedidos_df.columns:
                fig2, (ax21, ax22) = plt.subplots(1, 2, figsize=(15, 6))
                
                # Tentar converter para datetime
                try:
                    pedidos_df['OrderDate'] = pd.to_datetime(pedidos_df['OrderDate'])
                    
                    # Scatter plot temporal
                    ax21.scatter(pedidos_df['OrderDate'], pedidos_df['TotalAmount'], 
                                alpha=0.6, c=pedidos_df['TotalAmount'], cmap='viridis')
                    ax21.set_title('Evolução Temporal dos Valores', fontsize=14, fontweight='bold')
                    ax21.set_xlabel('Data do Pedido', fontsize=12)
                    ax21.set_ylabel('Valor Total (R$)', fontsize=12)
                    ax21.tick_params(axis='x', rotation=45)
                    ax21.grid(True, alpha=0.3)
                    
                    # Média móvel
                    pedidos_df_sorted = pedidos_df.sort_values('OrderDate')
                    pedidos_df_sorted['Media_Movel'] = pedidos_df_sorted['TotalAmount'].rolling(window=7).mean()
                    
                    ax22.plot(pedidos_df_sorted['OrderDate'], pedidos_df_sorted['TotalAmount'], 
                             'o', alpha=0.3, label='Valores Diários')
                    ax22.plot(pedidos_df_sorted['OrderDate'], pedidos_df_sorted['Media_Movel'], 
                             'r-', linewidth=2, label='Média Móvel (7 dias)')
                    ax22.set_title('Média Móvel dos Valores', fontsize=14, fontweight='bold')
                    ax22.set_xlabel('Data do Pedido', fontsize=12)
                    ax22.set_ylabel('Valor Total (R$)', fontsize=12)
                    ax22.tick_params(axis='x', rotation=45)
                    ax22.legend()
                    ax22.grid(True, alpha=0.3)
                    
                    plt.tight_layout()
                    plt.show()
                except:
                    print("Não foi possível criar gráficos temporais (formato de data inválido)")
            
            # Imprimir resumo textual também
            print("=" * 80)
            print("RESUMO ESTATÍSTICO - VALORES TOTAIS DOS PEDIDOS")
            print("=" * 80)
            print(f"\nMedidas de Tendência Central:")
            print(f"  • Média: R$ {media_vendas:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            print(f"  • Mediana: R$ {mediana_vendas:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            
            print(f"\nMedidas de Dispersão:")
            print(f"  • Desvio Padrão: R$ {desvio_padrao_vendas:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            print(f"  • Coeficiente de Variação: {cv_vendas:.1f}%")
            print(f"  • Assimetria: {assimetria:.3f}")
            print(f"  • Curtose: {curtose:.3f}")
            
            print(f"\nIntervalo:")
            print(f"  • Mínimo: R$ {dados_valor_total.min():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            print(f"  • Máximo: R$ {dados_valor_total.max():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            print(f"  • Amplitude: R$ {dados_valor_total.max() - dados_valor_total.min():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            
except FileNotFoundError:
    print("Erro: Arquivo 'orders.csv' não encontrado no caminho especificado")
except Exception as e:
    print(f"Erro inesperado: {str(e)}")