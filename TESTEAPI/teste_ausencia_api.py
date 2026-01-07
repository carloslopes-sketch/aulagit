import requests
import urllib.parse
import json
import re
from datetime import datetime, timedelta

class AnalisadorRespostas:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://api.iopoint.com.br"
        self.endpoint = "/API/CUSTOMER/CREATENEWABSENCE"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    def testar_e_analisar_resposta(self, params, nome_teste):
        """Testa com parâmetros específicos e analisa a resposta"""
        print(f"\n{'='*60}")
        print(f"TESTE: {nome_teste}")
        print(f"{'='*60}")
        print(f"Parâmetros: {json.dumps(params, indent=2)}")
        
        # Construir URL com parâmetros
        query_string = urllib.parse.urlencode(params)
        url = f"{self.base_url}{self.endpoint}?{query_string}"
        print(f"\nURL: {url}")
        
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            print(f"Status: {response.status_code}")
            print(f"Content-Type: {response.headers.get('Content-Type')}")
            print(f"Tamanho: {len(response.text)} caracteres")
            
            # Salvar resposta em arquivo para análise
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"resposta_{nome_teste}_{timestamp}.html"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f"Resposta salva em: {filename}")
            
            # Análise da resposta
            self.analisar_conteudo(response.text, nome_teste)
            
            return response.text
            
        except Exception as e:
            print(f"❌ Erro: {str(e)}")
            return None
    
    def analisar_conteudo(self, conteudo, nome_teste):
        """Analisa o conteúdo HTML retornado"""
        print(f"\n📊 ANÁLISE DO CONTEÚDO:")
        
        # Converter para minúsculas para busca
        conteudo_lower = conteudo.lower()
        
        # Procurar por palavras-chave indicativas
        palavras_chave = {
            'sucesso': ['sucesso', 'success', 'criado', 'cadastrado', 'registrado'],
            'erro': ['erro', 'error', 'falha', 'inválido', 'invalid'],
            'ausência': ['ausência', 'ausencia', 'absence', 'falt', 'falta'],
            'mensagem': ['mensagem', 'message', 'alert', 'notice'],
            'id': ['id=', 'id:', 'número', 'codigo', 'code'],
            'matrícula': ['matrícula', 'matricula', 'employee', 'funcionário']
        }
        
        for categoria, palavras in palavras_chave.items():
            encontradas = []
            for palavra in palavras:
                if palavra in conteudo_lower:
                    # Encontrar contexto ao redor da palavra
                    idx = conteudo_lower.find(palavra)
                    if idx != -1:
                        contexto = conteudo[max(0, idx-50):min(len(conteudo), idx+50)]
                        encontradas.append(f"'{palavra}' → ...{contexto}...")
            
            if encontradas:
                print(f"\n🔍 {categoria.upper()} encontrado:")
                for encontro in encontradas[:3]:  # Mostrar até 3 ocorrências
                    print(f"   {encontro}")
        
        # Procurar por padrões JSON ou estruturas de dados
        if '{' in conteudo and '}' in conteudo:
            print(f"\n📄 Possível conteúdo JSON detectado")
            # Tentar extrair JSON
            try:
                # Encontrar primeiro { e último }
                inicio = conteudo.find('{')
                fim = conteudo.rfind('}') + 1
                if inicio != -1 and fim > inicio:
                    json_str = conteudo[inicio:fim]
                    dados = json.loads(json_str)
                    print(f"✅ JSON válido encontrado!")
                    print(json.dumps(dados, indent=2, ensure_ascii=False))
            except:
                pass
        
        # Verificar se é uma página HTML com mensagem
        if '<html' in conteudo_lower:
            print(f"\n🌐 Conteúdo HTML detectado")
            
            # Extrair título se existir
            titulo_match = re.search(r'<title[^>]*>(.*?)</title>', conteudo, re.IGNORECASE)
            if titulo_match:
                print(f"   Título: {titulo_match.group(1)}")
            
            # Extrair texto do body
            body_match = re.search(r'<body[^>]*>(.*?)</body>', conteudo, re.IGNORECASE | re.DOTALL)
            if body_match:
                texto_body = body_match.group(1)
                # Remover tags HTML
                texto_limpo = re.sub(r'<[^>]+>', ' ', texto_body)
                texto_limpo = re.sub(r'\s+', ' ', texto_limpo).strip()
                
                if len(texto_limpo) > 0:
                    print(f"\n📝 Texto da página (resumido):")
                    print(f"   {texto_limpo[:200]}...")
                    
                    # Procurar por números que possam ser IDs
                    numeros = re.findall(r'\b\d{3,}\b', texto_limpo)
                    if numeros:
                        print(f"\n🔢 Números encontrados (possíveis IDs): {numeros}")
        
        # Mostrar primeiras linhas do conteúdo
        print(f"\n📋 PRIMEIRAS LINHAS DO CONTEÚDO:")
        linhas = conteudo.split('\n')
        for i, linha in enumerate(linhas[:10]):
            if linha.strip():
                print(f"   Linha {i+1}: {linha[:100]}...")
    
    def teste_completo(self):
        """Executa um teste completo com os melhores parâmetros"""
        print("=" * 70)
        print("TESTE COMPLETO - CRIAR AUSÊNCIA")
        print("=" * 70)
        
        # Parâmetros que parecem mais promissores
        params = {
            "matricula": "4297",
            "dt_inicio": "2026-01-07",
            "dt_fim": "2026-01-09",
            "justificativa": "Teste de ausência via API",
            "ativo": "S",
            "tipo": "D",
            "quantidade": "1",
            "tipo_aprovacao": "A",
            "observacao": "Criado via teste automático"
        }
        
        resposta = self.testar_e_analisar_resposta(params, "completo")
        
        if resposta:
            # Verificar se podemos considerar sucesso
            if any(palavra in resposta.lower() for palavra in ['sucesso', 'success', 'criado', 'id']):
                print(f"\n✅ PROVÁVEL SUCESSO!")
                print("A ausência pode ter sido criada com sucesso.")
                print("Verifique no sistema IOPoint se a ausência aparece.")
            else:
                print(f"\n⚠️  Resposta recebida mas sem indicadores claros de sucesso.")
                print("Verifique o arquivo HTML salvo para mais detalhes.")
    
    def verificar_no_sistema(self):
        """Sugere como verificar se a ausência foi criada"""
        print("\n" + "=" * 70)
        print("COMO VERIFICAR SE A AUSÊNCIA FOI CRIADA")
        print("=" * 70)
        
        print("1. Acesse o sistema IOPoint")
        print("2. Vá para o módulo de Ausências/Faltas")
        print("3. Busque pela matrícula 4297")
        print("4. Verifique se há uma ausência para 07-09/01/2026")
        print("5. Ou verifique se há uma ausência com justificativa 'Teste de ausência via API'")
        print("\nSe encontrar, o endpoint funciona via GET com query parameters!")
        
        # Também podemos tentar listar ausências via API se houver endpoint
        print("\n" + "=" * 70)
        print("TENTANDO LISTAR AUSÊNCIAS VIA API")
        print("=" * 70)
        
        endpoints_listagem = [
            "/API/CUSTOMER/GETABSENCES",
            "/API/CUSTOMER/LISTABSENCES",
            "/API/ABSENCES",
            "/v1/ausencias"
        ]
        
        for endpoint in endpoints_listagem:
            url = f"{self.base_url}{endpoint}"
            print(f"\nTestando: {endpoint}")
            
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                print(f"  Status: {response.status_code}")
                
                if response.status_code == 200:
                    print(f"  🔍 Conteúdo (início): {response.text[:200]}")
                    
                    # Verificar se parece ser uma lista
                    if '[' in response.text and ']' in response.text:
                        print(f"  📋 Possível array/lista JSON")
                        try:
                            dados = json.loads(response.text)
                            if isinstance(dados, list):
                                print(f"  ✅ Lista com {len(dados)} itens")
                                for i, item in enumerate(dados[:3]):
                                    print(f"     Item {i+1}: {str(item)[:100]}...")
                        except:
                            pass
                            
            except Exception as e:
                print(f"  ❌ Erro: {str(e)}")

def main():
    token = "d69b709ea7482f061b938f91f-da42596"
    
    print("🔍 ANALISADOR DE RESPOSTAS - ENDPOINT GET")
    print("=" * 70)
    print("Status 200 recebido! Agora vamos analisar o conteúdo...")
    
    analisador = AnalisadorRespostas(token)
    
    # Executar teste completo
    analisador.teste_completo()
    
    # Opção para verificar no sistema
    print("\nDeseja verificar se a ausência foi criada no sistema?")
    resposta = input("(s/n): ").strip().lower()
    
    if resposta == 's':
        analisador.verificar_no_sistema()
    
    print("\n" + "=" * 70)
    print("PRÓXIMOS PASSOS:")
    print("=" * 70)
    print("1. Verifique os arquivos HTML salvos na pasta atual")
    print("2. Abra-os no navegador para ver como são exibidos")
    print("3. Procure por mensagens de sucesso/erro")
    print("4. Verifique no sistema IOPoint se a ausência aparece")
    print("5. Se funcionou, use GET com query params no seu código")

if __name__ == "__main__":
    main()