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
    pedidos_df = pd.read_csv("../aula8/orders.csv")
    
    if 'TotalAmount' not in pedidos_df.columns:
        print("Erro: Coluna 'TotalAmount' não encontrada")
        print(f"Colunas disponíveis: {list(pedidos_df.columns)}")
    else:
        dados_valor_total = pedidos_df['TotalAmount'].dropna()
        
        if dados_valor_total.empty:
            print("Erro: Nenhum dado disponível")
        else:
            # ==================== CÁLCULOS ESTATÍSTICOS ====================
            media_vendas = dados_valor_total.mean()
            mediana_vendas = dados_valor_total.median()
            variancia_vendas = np.var(dados_valor_total, ddof=0)
            desvio_padrao_vendas = np.std(dados_valor_total, ddof=0)
            cv_vendas = (desvio_padrao_vendas / media_vendas) * 100
            assimetria = dados_valor_total.skew()
            curtose = dados_valor_total.kurtosis()
            
            # ==================== DETECÇÃO DE OUTLIERS ====================
            Q1 = dados_valor_total.quantile(0.25)
            Q3 = dados_valor_total.quantile(0.75)
            IQR = Q3 - Q1
            limite_inferior = Q1 - 1.5 * IQR
            limite_superior = Q3 + 1.5 * IQR
            
            outliers_inferiores = dados_valor_total[dados_valor_total < limite_inferior]
            outliers_superiores = dados_valor_total[dados_valor_total > limite_superior]
            todos_outliers = pd.concat([outliers_inferiores, outliers_superiores])
            dados_sem_outliers = dados_valor_total[(dados_valor_total >= limite_inferior) & 
                                                   (dados_valor_total <= limite_superior)]
            
            # ==================== FUNÇÃO PARA FORMATAR VALORES ====================
            def formatar_valor(valor):
                return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            
            # ==================== GRUPO 1: VISUALIZAÇÃO BÁSICA E DISTRIBUIÇÃO ====================
            print("\n" + "="*80)
            print("GRUPO 1: VISUALIZAÇÃO BÁSICA E DISTRIBUIÇÃO")
            print("="*80)
            
            fig1, axs1 = plt.subplots(2, 2, figsize=(14, 10))
            fig1.suptitle('GRUPO 1: VISUALIZAÇÃO BÁSICA E DISTRIBUIÇÃO', fontsize=16, fontweight='bold')
            
            # Gráfico 1.1: Histograma com distribuição
            ax1 = axs1[0, 0]
            n, bins, patches = ax1.hist(dados_valor_total, bins=30, edgecolor='black', alpha=0.7, 
                                       density=True, color='skyblue')
            dados_valor_total.plot(kind='kde', ax=ax1, color='darkblue', linewidth=2)
            ax1.axvline(media_vendas, color='red', linestyle='--', linewidth=2, 
                       label=f'Média: {formatar_valor(media_vendas)}')
            ax1.axvline(mediana_vendas, color='green', linestyle='--', linewidth=2,
                       label=f'Mediana: {formatar_valor(mediana_vendas)}')
            ax1.set_title('1. Distribuição dos Valores Totais', fontsize=12, fontweight='bold')
            ax1.set_xlabel('Valor (R$)', fontsize=10)
            ax1.set_ylabel('Densidade', fontsize=10)
            ax1.legend(fontsize=9)
            ax1.grid(True, alpha=0.3)
            
            # Gráfico 1.2: Boxplot básico
            ax2 = axs1[0, 1]
            box = ax2.boxplot([dados_valor_total], patch_artist=True, 
                             boxprops=dict(facecolor='lightcoral', alpha=0.7),
                             medianprops=dict(color='black', linewidth=2),
                             whiskerprops=dict(color='gray', linewidth=1.5))
            ax2.set_title('2. Boxplot - Visão Geral', fontsize=12, fontweight='bold')
            ax2.set_ylabel('Valor (R$)', fontsize=10)
            ax2.set_xticklabels(['Valores Totais'])
            ax2.grid(True, alpha=0.3)
            
            # Gráfico 1.3: Gráfico de violino
            ax3 = axs1[1, 0]
            violin_parts = ax3.violinplot([dados_valor_total], showmeans=True, showmedians=True)
            for pc in violin_parts['bodies']:
                pc.set_facecolor('#FFD700')
                pc.set_alpha(0.7)
            ax3.set_title('3. Gráfico de Violino', fontsize=12, fontweight='bold')
            ax3.set_ylabel('Valor (R$)', fontsize=10)
            ax3.grid(True, alpha=0.3)
            
            # Gráfico 1.4: Medidas de tendência central
            ax4 = axs1[1, 1]
            medidas = ['Média', 'Mediana', 'Moda']
            valores = [media_vendas, mediana_vendas, dados_valor_total.mode()[0]]
            cores = ['#FF6B6B', '#4ECDC4', '#45B7D1']
            bars = ax4.bar(medidas, valores, color=cores, edgecolor='black', linewidth=1.5)
            ax4.set_title('4. Medidas de Tendência Central', fontsize=12, fontweight='bold')
            ax4.set_ylabel('Valor (R$)', fontsize=10)
            for bar, valor in zip(bars, valores):
                height = bar.get_height()
                ax4.text(bar.get_x() + bar.get_width()/2., height + 0.01*max(valores),
                        formatar_valor(valor), ha='center', va='bottom', fontsize=9)
            ax4.grid(True, alpha=0.3, axis='y')
            
            plt.tight_layout()
            plt.show()
            
            # ==================== GRUPO 2: ANÁLISE DETALHADA DE OUTLIERS ====================
            print("\n" + "="*80)
            print("GRUPO 2: ANÁLISE DETALHADA DE OUTLIERS")
            print("="*80)
            
            fig2, axs2 = plt.subplots(2, 2, figsize=(14, 10))
            fig2.suptitle('GRUPO 2: ANÁLISE DETALHADA DE OUTLIERS', fontsize=16, fontweight='bold')
            
            # Gráfico 2.1: Boxplot com limites
            ax1 = axs2[0, 0]
            box = ax1.boxplot([dados_valor_total], patch_artist=True, 
                             boxprops=dict(facecolor='lightblue', alpha=0.7),
                             medianprops=dict(color='red', linewidth=2))
            ax1.axhline(limite_superior, color='green', linestyle='--', alpha=0.7, 
                       label=f'Lim. Sup: {formatar_valor(limite_superior)}')
            ax1.axhline(limite_inferior, color='orange', linestyle='--', alpha=0.7,
                       label=f'Lim. Inf: {formatar_valor(limite_inferior)}')
            ax1.axhline(media_vendas, color='blue', linestyle='-', alpha=0.5)
            ax1.set_title('1. Boxplot com Limites de Outliers', fontsize=12, fontweight='bold')
            ax1.set_ylabel('Valor (R$)', fontsize=10)
            ax1.legend(fontsize=9)
            ax1.grid(True, alpha=0.3)
            
            # Gráfico 2.2: Scatter plot colorido por tipo
            ax2 = axs2[0, 1]
            cores = ['red' if x < limite_inferior else 
                    'orange' if x > limite_superior else 
                    'blue' for x in dados_valor_total]
            ax2.scatter(range(len(dados_valor_total)), dados_valor_total, c=cores, alpha=0.6, s=30)
            ax2.axhline(limite_superior, color='green', linestyle='--', alpha=0.7, linewidth=1.5)
            ax2.axhline(limite_inferior, color='orange', linestyle='--', alpha=0.7, linewidth=1.5)
            ax2.set_title('2. Identificação de Outliers', fontsize=12, fontweight='bold')
            ax2.set_xlabel('Índice do Pedido', fontsize=10)
            ax2.set_ylabel('Valor (R$)', fontsize=10)
            ax2.grid(True, alpha=0.3)
            
            # Gráfico 2.3: Proporção de outliers
            ax3 = axs2[1, 0]
            categorias = ['Dados Normais', 'Outliers Inf', 'Outliers Sup']
            contagem = [len(dados_sem_outliers), len(outliers_inferiores), len(outliers_superiores)]
            cores_pizza = ['lightblue', 'red', 'orange']
            wedges, texts, autotexts = ax3.pie(contagem, labels=categorias, colors=cores_pizza, 
                                              autopct='%1.1f%%', startangle=90, explode=(0.05, 0.1, 0.1))
            ax3.set_title('3. Proporção de Outliers', fontsize=12, fontweight='bold')
            
            # Gráfico 2.4: Histograma com outliers destacados
            ax4 = axs2[1, 1]
            dados_normais = dados_sem_outliers
            out_inf = outliers_inferiores
            out_sup = outliers_superiores
            n, bins, patches = ax4.hist([dados_normais, out_inf, out_sup], 
                                       bins=30, stacked=True, 
                                       color=['lightblue', 'red', 'orange'],
                                       edgecolor='black', alpha=0.7,
                                       label=['Normais', 'Outliers Inf', 'Outliers Sup'])
            ax4.axvline(limite_inferior, color='red', linestyle='--', linewidth=2, alpha=0.7)
            ax4.axvline(limite_superior, color='orange', linestyle='--', linewidth=2, alpha=0.7)
            ax4.set_title('4. Histograma com Outliers', fontsize=12, fontweight='bold')
            ax4.set_xlabel('Valor (R$)', fontsize=10)
            ax4.set_ylabel('Frequência', fontsize=10)
            ax4.legend(fontsize=9)
            ax4.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.show()
            
            # ==================== GRUPO 3: IMPACTO E COMPARAÇÃO ====================
            print("\n" + "="*80)
            print("GRUPO 3: IMPACTO E COMPARAÇÃO")
            print("="*80)
            
            fig3, axs3 = plt.subplots(2, 2, figsize=(14, 10))
            fig3.suptitle('GRUPO 3: IMPACTO E COMPARAÇÃO', fontsize=16, fontweight='bold')
            
            # Gráfico 3.1: Comparação com/sem outliers
            ax1 = axs3[0, 0]
            dados_comparacao = [dados_valor_total, dados_sem_outliers]
            labels = ['Com Outliers', 'Sem Outliers']
            cores_comparacao = ['lightcoral', 'lightgreen']
            bp = ax1.boxplot(dados_comparacao, patch_artist=True, labels=labels)
            for patch, color in zip(bp['boxes'], cores_comparacao):
                patch.set_facecolor(color)
                patch.set_alpha(0.7)
            ax1.set_title('1. Comparação: Com vs Sem Outliers', fontsize=12, fontweight='bold')
            ax1.set_ylabel('Valor (R$)', fontsize=10)
            ax1.grid(True, alpha=0.3)
            
            # Gráfico 3.2: Impacto nas medidas estatísticas
            ax2 = axs3[0, 1]
            medidas_com = [media_vendas, desvio_padrao_vendas, cv_vendas]
            medidas_sem = [
                dados_sem_outliers.mean(),
                dados_sem_outliers.std(),
                (dados_sem_outliers.std() / dados_sem_outliers.mean()) * 100
            ]
            x = np.arange(3)
            width = 0.35
            bars1 = ax2.bar(x - width/2, medidas_com, width, 
                          label='Com Outliers', color='lightcoral', alpha=0.7)
            bars2 = ax2.bar(x + width/2, medidas_sem, width, 
                          label='Sem Outliers', color='lightgreen', alpha=0.7)
            ax2.set_title('2. Impacto nas Medidas', fontsize=12, fontweight='bold')
            ax2.set_xticks(x)
            ax2.set_xticklabels(['Média', 'Desvio Padrão', 'CV (%)'])
            ax2.legend(fontsize=9)
            ax2.grid(True, alpha=0.3, axis='y')
            
            # Gráfico 3.3: Z-scores
            ax3 = axs3[1, 0]
            z_scores = stats.zscore(dados_valor_total)
            cores_zscore = []
            for z in z_scores:
                if z < -3:
                    cores_zscore.append('red')
                elif z > 3:
                    cores_zscore.append('orange')
                elif abs(z) > 2:
                    cores_zscore.append('yellow')
                else:
                    cores_zscore.append('blue')
            ax3.scatter(range(len(z_scores)), z_scores, c=cores_zscore, alpha=0.6, s=30)
            ax3.axhline(3, color='orange', linestyle='--', linewidth=2, alpha=0.7, label='Z = 3')
            ax3.axhline(-3, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Z = -3')
            ax3.axhline(0, color='green', linestyle='-', linewidth=1, alpha=0.5)
            ax3.set_title('3. Z-scores dos Valores', fontsize=12, fontweight='bold')
            ax3.set_xlabel('Índice do Pedido', fontsize=10)
            ax3.set_ylabel('Z-score', fontsize=10)
            ax3.legend(fontsize=9)
            ax3.grid(True, alpha=0.3)
            
            # Gráfico 3.4: QQ-Plot para normalidade
            ax4 = axs3[1, 1]
            stats.probplot(dados_valor_total, dist="norm", plot=ax4)
            ax4.get_lines()[0].set_marker('o')
            ax4.get_lines()[0].set_markersize(4)
            ax4.get_lines()[0].set_alpha(0.6)
            ax4.get_lines()[1].set_linewidth(2)
            ax4.get_lines()[1].set_color('red')
            ax4.set_title('4. QQ-Plot - Teste de Normalidade', fontsize=12, fontweight='bold')
            ax4.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.show()
            
            # ==================== GRUPO 4: RESUMOS E TABELAS ====================
            print("\n" + "="*80)
            print("GRUPO 4: RESUMOS E TABELAS")
            print("="*80)
            
            fig4, axs4 = plt.subplots(2, 2, figsize=(14, 10))
            fig4.suptitle('GRUPO 4: RESUMOS E TABELAS', fontsize=16, fontweight='bold')
            
            # Gráfico 4.1: Tabela de medidas estatísticas
            ax1 = axs4[0, 0]
            ax1.axis('tight')
            ax1.axis('off')
            dados_tabela1 = [
                ["Medida", "Valor", "Interpretação"],
                ["Nº de Pedidos", f"{len(dados_valor_total):,}".replace(',', '.'), "Total analisado"],
                ["Média", formatar_valor(media_vendas), "Valor médio"],
                ["Mediana", formatar_valor(mediana_vendas), "Valor central"],
                ["Desvio Padrão", formatar_valor(desvio_padrao_vendas), "Dispersão absoluta"],
                ["CV", f"{cv_vendas:.1f}%", "Dispersão relativa"],
                ["Assimetria", f"{assimetria:.3f}", "Simetria dos dados"],
                ["Curtose", f"{curtose:.3f}", "Achatamento da curva"],
                ["Mínimo", formatar_valor(dados_valor_total.min()), "Valor mínimo"],
                ["Máximo", formatar_valor(dados_valor_total.max()), "Valor máximo"]
            ]
            tabela1 = ax1.table(cellText=dados_tabela1, cellLoc='left', 
                               colWidths=[0.25, 0.25, 0.4],
                               loc='center', fontsize=9)
            tabela1.auto_set_font_size(False)
            tabela1.set_fontsize(8)
            tabela1.scale(1, 1.2)
            for i in range(len(dados_tabela1)):
                for j in range(3):
                    if i == 0:
                        tabela1[(i, j)].set_facecolor('#34495E')
                        tabela1[(i, j)].set_text_props(weight='bold', color='white')
            ax1.set_title('1. Resumo Estatístico', fontsize=12, fontweight='bold', pad=20)
            
            # Gráfico 4.2: Tabela de outliers
            ax2 = axs4[0, 1]
            ax2.axis('tight')
            ax2.axis('off')
            dados_tabela2 = [
                ["Tipo", "Quantidade", "Percentual", "Valor Médio"],
                ["Dados Normais", f"{len(dados_sem_outliers):,}".replace(',', '.'),
                 f"{(len(dados_sem_outliers)/len(dados_valor_total)*100):.1f}%",
                 formatar_valor(dados_sem_outliers.mean())],
                ["Outliers Inferiores", f"{len(outliers_inferiores):,}".replace(',', '.'),
                 f"{(len(outliers_inferiores)/len(dados_valor_total)*100):.1f}%",
                 formatar_valor(outliers_inferiores.mean()) if len(outliers_inferiores) > 0 else "R$ 0,00"],
                ["Outliers Superiores", f"{len(outliers_superiores):,}".replace(',', '.'),
                 f"{(len(outliers_superiores)/len(dados_valor_total)*100):.1f}%",
                 formatar_valor(outliers_superiores.mean()) if len(outliers_superiores) > 0 else "R$ 0,00"]
            ]
            tabela2 = ax2.table(cellText=dados_tabela2, cellLoc='center', 
                               colWidths=[0.25, 0.2, 0.2, 0.35],
                               loc='center', fontsize=9)
            tabela2.scale(1, 1.2)
            cores_celulas = ['#2C3E50', '#ECF0F1', '#FFB8B8', '#FFE0B2']
            for i in range(len(dados_tabela2)):
                for j in range(4):
                    tabela2[(i, j)].set_facecolor(cores_celulas[i])
                    if i == 0:
                        tabela2[(i, j)].set_text_props(weight='bold', color='white')
            ax2.set_title('2. Resumo de Outliers', fontsize=12, fontweight='bold', pad=20)
            
            # Gráfico 4.3: Medidas de dispersão (radar)
            ax3 = axs4[1, 0]
            try:
                from matplotlib.patches import Circle
                categorias = ['Variância', 'Desvio Padrão', 'CV (%)', 'Amplitude']
                valores_disp = [variancia_vendas, desvio_padrao_vendas, cv_vendas, 
                              dados_valor_total.max() - dados_valor_total.min()]
                valores_norm = [v/max(valores_disp)*100 for v in valores_disp]
                valores_norm += valores_norm[:1]
                angles = np.linspace(0, 2*np.pi, len(categorias), endpoint=False).tolist()
                angles += angles[:1]
                ax3 = plt.subplot(2, 2, 3, projection='polar')
                ax3.plot(angles, valores_norm, 'o-', linewidth=2, color='purple')
                ax3.fill(angles, valores_norm, alpha=0.25, color='purple')
                ax3.set_xticks(angles[:-1])
                ax3.set_xticklabels(categorias, fontsize=9)
                ax3.set_title('3. Medidas de Dispersão', fontsize=12, fontweight='bold', pad=20)
                ax3.grid(True)
            except:
                ax3.text(0.5, 0.5, 'Gráfico não disponível', ha='center', va='center', fontsize=12)
                ax3.set_title('3. Medidas de Dispersão', fontsize=12, fontweight='bold')
            
            # Gráfico 4.4: Histograma cumulativo
            ax4 = axs4[1, 1]
            n, bins, patches = ax4.hist(dados_valor_total, bins=30, edgecolor='black', 
                                       alpha=0.5, color='lightblue', density=True, 
                                       label='Frequência')
            hist, bin_edges = np.histogram(dados_valor_total, bins=30, density=True)
            cumsum = np.cumsum(hist) * np.diff(bin_edges)
            ax4.plot(bin_edges[1:], cumsum, 'r-', linewidth=2, label='Distribuição Acumulada')
            ax4.set_title('4. Histograma Cumulativo', fontsize=12, fontweight='bold')
            ax4.set_xlabel('Valor (R$)', fontsize=10)
            ax4.set_ylabel('Densidade / Cumulativa', fontsize=10)
            ax4.legend(fontsize=9)
            ax4.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.show()
            
            # ==================== GRUPO 5: LISTA DETALHADA DE OUTLIERS ====================
            if len(todos_outliers) > 0:
                print("\n" + "="*80)
                print("GRUPO 5: LISTA DETALHADA DE OUTLIERS")
                print("="*80)
                
                fig5, ax = plt.subplots(figsize=(12, 8))
                ax.axis('tight')
                ax.axis('off')
                
                # Preparar dados para tabela
                dados_detalhados = []
                dados_detalhados.append(["Índice", "Valor (R$)", "Tipo", "Diferença do Limite", "Z-score"])
                
                # Ordenar outliers
                todos_outliers_sorted = todos_outliers.sort_values()
                
                for idx, valor in todos_outliers_sorted.items():
                    tipo = "Inferior" if valor < limite_inferior else "Superior"
                    if tipo == "Inferior":
                        diferenca = limite_inferior - valor
                    else:
                        diferenca = valor - limite_superior
                    
                    z = (valor - media_vendas) / desvio_padrao_vendas
                    
                    dados_detalhados.append([
                        str(idx),
                        formatar_valor(valor),
                        tipo,
                        formatar_valor(diferenca),
                        f"{z:.2f}"
                    ])
                
                # Criar tabela
                tabela = ax.table(cellText=dados_detalhados, cellLoc='center', 
                                 colWidths=[0.1, 0.2, 0.15, 0.2, 0.15],
                                 loc='center', fontsize=9)
                
                tabela.auto_set_font_size(False)
                tabela.set_fontsize(8)
                tabela.scale(1, 1.1)
                
                # Colorir cabeçalho
                for j in range(5):
                    tabela[(0, j)].set_facecolor('#2C3E50')
                    tabela[(0, j)].set_text_props(weight='bold', color='white')
                
                # Colorir linhas baseado no tipo
                for i in range(1, len(dados_detalhados)):
                    tipo = dados_detalhados[i][2]
                    cor = '#FFB8B8' if tipo == 'Inferior' else '#FFE0B2'
                    for j in range(5):
                        tabela[(i, j)].set_facecolor(cor)
                
                ax.set_title('LISTA DETALHADA DE OUTLIERS', fontsize=14, fontweight='bold', pad=20)
                plt.tight_layout()
                plt.show()
            
            # ==================== RESUMO TEXTUAL ====================
            print("\n" + "="*80)
            print("RESUMO FINAL DA ANÁLISE")
            print("="*80)
            
            print(f"\n📊 MEDIDAS DE TENDÊNCIA CENTRAL:")
            print(f"   • Média: {formatar_valor(media_vendas)}")
            print(f"   • Mediana: {formatar_valor(mediana_vendas)}")
            print(f"   • Moda: {formatar_valor(dados_valor_total.mode()[0])}")
            
            print(f"\n📈 MEDIDAS DE DISPERSÃO:")
            print(f"   • Desvio Padrão: {formatar_valor(desvio_padrao_vendas)}")
            print(f"   • Coeficiente de Variação: {cv_vendas:.1f}%")
            print(f"   • Amplitude: {formatar_valor(dados_valor_total.max() - dados_valor_total.min())}")
            
            print(f"\n🎯 ANÁLISE DE OUTLIERS:")
            print(f"   • Limite Inferior: {formatar_valor(limite_inferior)}")
            print(f"   • Limite Superior: {formatar_valor(limite_superior)}")
            print(f"   • Outliers Inferiores: {len(outliers_inferiores)} ({len(outliers_inferiores)/len(dados_valor_total)*100:.1f}%)")
            print(f"   • Outliers Superiores: {len(outliers_superiores)} ({len(outliers_superiores)/len(dados_valor_total)*100:.1f}%)")
            print(f"   • Total Outliers: {len(todos_outliers)} ({len(todos_outliers)/len(dados_valor_total)*100:.1f}%)")
            
            print(f"\n📐 MEDIDAS DE FORMA:")
            print(f"   • Assimetria: {assimetria:.3f}")
            print(f"   • Curtose: {curtose:.3f}")
            
            print(f"\n📋 RESUMO GERAL:")
            print(f"   • Total de pedidos: {len(dados_valor_total):,}".replace(',', '.'))
            print(f"   • Valor mínimo: {formatar_valor(dados_valor_total.min())}")
            print(f"   • Valor máximo: {formatar_valor(dados_valor_total.max())}")
            print(f"   • Soma total: {formatar_valor(dados_valor_total.sum())}")
            
except FileNotFoundError:
    print("Erro: Arquivo 'orders.csv' não encontrado")
except Exception as e:
    print(f"Erro inesperado: {str(e)}")