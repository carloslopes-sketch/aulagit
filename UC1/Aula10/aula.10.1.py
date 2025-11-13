import sys
try:
 print("Tentando importar a biblioteca Pandas...")
 import pandas as pd
 print("Pandas importado com sucesso!")
 
 # É uma boa prática verificar a versão
 print(f"Versão do Pandas instalada: {pd.__version__}")
 print(f"Versão do Python: {sys.version.split()[0]}")
 
except ImportError:
 print("\n--- ERRO ---")
 print("A biblioteca Pandas não foi encontrada.")
 print("Por favor, instale-a usando o comando no seu terminal:")
 print("pip install pandas")
except Exception as e:
 print(f"Ocorreu um erro inesperado: {e}")
finally:
 print("Verificação de setup concluída.\n")

 #******************************************************************************************
 # SEGUNDO EXEMPLO:

import pandas as pd

try:         
    print("--- Criando uma Série (1D) com Cargos e Salários ---")
    
    dados_salarios = {
    'Analista de Dados': 7000.50,
    'Cientista de Dados': 12000.00,
    'Engenheiro de Dados': 11000.00,
    'Analista de BI': 6500.00
    }
    
    # Criamos a Série a partir do dicionário
    serie_salarios = pd.Series(dados_salarios)
    
    print("\n--- Série Criada ---")
    print(serie_salarios)
    
    # Explorando a estrutura
    print("\n--- Explorando a Estrutura da Série ---")
    print(f"Índice (Chaves): {list(serie_salarios.index)}")
    print(f"Valores: {list(serie_salarios.values)}")
    
    # Acessando um valor pelo índice (chave)
    print("\n--- Acessando um Valor ---")
    print(f"Salário do Cientista de Dados: R$ {serie_salarios['Cientista de Dados']:.2f}")
except NameError:
 print("\nERRO: O pandas (pd) não foi importado corretamente.")
except Exception as e:
 print(f"Ocorreu um erro ao criar a Série: {e}")
finally:
 print("Exploração de Séries concluída.\n")

 #******************************************************************************************
 # TERCEIRO EXEMPLO:

 # --- 3. Criando um DataFrame (Estrutura 2D) ---
import pandas as pd

try:
    print("--- Criando um DataFrame (2D) de Filmes ---")
    
    dados_filmes = {
    'nome_do_filme': ['O Poderoso Chefão', 'Interestelar', 'Parasita', 'Matrix'],
    'ano_de_lancamento': [1972, 2014, 2019, 1999],
    'genero': ['Criminal', 'Ficção Científica', 'Suspense', 'Ficção Científica']
    }
    
    # Criamos o DataFrame a partir do dicionário
    df_filmes = pd.DataFrame(dados_filmes)
    
    print("\n--- DataFrame Criado ---")
    print(df_filmes)
    
    print("\n--- Informações do DataFrame (.info()) ---")
    df_filmes.info()
    
except NameError:
 print("\nERRO: O pandas (pd) não foi importado corretamente.")
except Exception as e:
 print(f"Ocorreu um erro ao criar o DataFrame: {e}")
finally:
 print("Criação de DataFrame concluída.\n")