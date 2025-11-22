import json
import datetime
from enum import Enum
from typing import List, Dict, Any
import streamlit as st
import pandas as pd

class Objetivo(Enum):
    GANHAR_MASSA = "ganhar_massa"
    PERDER_PESO = "perder_peso"
    PERFORMANCE_CORRIDA = "performance_corrida"
    PERFORMANCE_FUTEBOL = "performance_futebol"

class Nivel(Enum):
    INICIANTE = "iniciante"
    INTERMEDIARIO = "intermediario"
    AVANCADO = "avancado"

class DivisaoTreino(Enum):
    AB = "A-B (Superior/Inferior)"
    ABC = "A-B-C (Push/Pull/Legs)"
    ABCD = "A-B-C-D (4 dias específicos)"
    ABCDE = "A-B-C-D-E (5 dias específicos)"

class AppTreinamentoStreamlit:
    def __init__(self):
        self.arquivo_dados = "dados_usuarios.json"
        self.carregar_dados()
    
    def carregar_dados(self):
        try:
            with open(self.arquivo_dados, 'r') as f:
                dados = json.load(f)
                st.session_state.usuarios = dados.get('usuarios', [])
        except FileNotFoundError:
            st.session_state.usuarios = []
    
    def salvar_dados(self):
        dados = {'usuarios': st.session_state.usuarios}
        with open(self.arquivo_dados, 'w') as f:
            json.dump(dados, f, indent=2)
    
    def pagina_cadastro_usuario(self):
        st.header("📝 Cadastro de Usuário")
        
        if len(st.session_state.usuarios) >= 5:
            st.warning("Limite de 5 usuários atingido!")
            return
        
        with st.form("cadastro_usuario"):
            col1, col2 = st.columns(2)
            
            with col1:
                nome = st.text_input("Nome completo")
                idade = st.number_input("Idade", min_value=1, max_value=100, value=25)
                peso = st.number_input("Peso (kg)", min_value=0.0, value=70.0)
            
            with col2:
                altura = st.number_input("Altura (m)", min_value=0.0, value=1.75, step=0.01)
                nivel = st.selectbox(
                    "Nível de experiência",
                    options=list(Nivel),
                    format_func=lambda x: x.value.title()
                )
                objetivo = st.selectbox(
                    "Objetivo",
                    options=list(Objetivo),
                    format_func=lambda x: x.value.replace('_', ' ').title()
                )
            
            submitted = st.form_submit_button("Cadastrar Usuário")
            
            if submitted:
                if not nome:
                    st.error("Por favor, informe o nome!")
                    return
                
                usuario = {
                    'id': len(st.session_state.usuarios) + 1,
                    'nome': nome,
                    'idade': idade,
                    'peso': peso,
                    'altura': altura,
                    'nivel': nivel.value,
                    'objetivo': objetivo.value,
                    'data_cadastro': datetime.datetime.now().isoformat(),
                    'ciclo_atual': 1,
                    'ultima_troca': datetime.datetime.now().isoformat()
                }
                
                st.session_state.usuarios.append(usuario)
                self.salvar_dados()
                st.success(f"Usuário {nome} cadastrado com sucesso!")
                st.balloons()
    
    def calcular_imc(self, peso, altura):
        return peso / (altura ** 2)
    
    def determinar_divisao_treino(self, nivel: Nivel, objetivo: Objetivo) -> DivisaoTreino:
        if nivel == Nivel.INICIANTE:
            return DivisaoTreino.AB
        elif nivel == Nivel.INTERMEDIARIO:
            return DivisaoTreino.ABC
        else:  # AVANCADO
            if objetivo in [Objetivo.PERFORMANCE_CORRIDA, Objetivo.PERFORMANCE_FUTEBOL]:
                return DivisaoTreino.ABCD
            else:
                return DivisaoTreino.ABCDE
    
    def gerar_treino_massa(self, usuario: Dict) -> Dict:
        nivel = Nivel(usuario['nivel'])
        ciclo = usuario['ciclo_atual']
        divisao = self.determinar_divisao_treino(nivel, Objetivo.GANHAR_MASSA)
        
        exercicios_base = {
            DivisaoTreino.AB: {
                'A - Superior': [
                    {'nome': 'Supino Reto com Barra', 'series': 4, 'repeticoes': '8-12', 'carga': 'Progressiva'},
                    {'nome': 'Remada Curvada', 'series': 4, 'repeticoes': '8-12', 'carga': 'Progressiva'},
                    {'nome': 'Desenvolvimento Militar', 'series': 3, 'repeticoes': '10-12', 'carga': 'Média'},
                    {'nome': 'Pull-down Frente', 'series': 3, 'repeticoes': '10-15', 'carga': 'Média'},
                    {'nome': 'Rosca Direta', 'series': 3, 'repeticoes': '12-15', 'carga': 'Leve'},
                    {'nome': 'Tríceps Corda', 'series': 3, 'repeticoes': '12-15', 'carga': 'Leve'}
                ],
                'B - Inferior': [
                    {'nome': 'Agachamento Livre', 'series': 4, 'repeticoes': '8-12', 'carga': 'Progressiva'},
                    {'nome': 'Leg Press 45°', 'series': 4, 'repeticoes': '10-15', 'carga': 'Progressiva'},
                    {'nome': 'Cadeira Extensora', 'series': 3, 'repeticoes': '12-15', 'carga': 'Média'},
                    {'nome': 'Mesa Flexora', 'series': 3, 'repeticoes': '12-15', 'carga': 'Média'},
                    {'nome': 'Panturrilha Sentado', 'series': 4, 'repeticoes': '15-20', 'carga': 'Progressiva'},
                    {'nome': 'Abdominal Supra', 'series': 3, 'repeticoes': '15-20', 'carga': 'Corpo'}
                ]
            },
            DivisaoTreino.ABC: {
                'A - Push (Empurrar)': [
                    {'nome': 'Supino Reto com Barra', 'series': 4, 'repeticoes': '6-10', 'carga': 'Pesada'},
                    {'nome': 'Supino Inclinado com Halteres', 'series': 3, 'repeticoes': '8-12', 'carga': 'Média'},
                    {'nome': 'Desenvolvimento Militar', 'series': 4, 'repeticoes': '8-12', 'carga': 'Progressiva'},
                    {'nome': 'Elevação Lateral', 'series': 3, 'repeticoes': '12-15', 'carga': 'Leve'},
                    {'nome': 'Tríceps Francês', 'series': 3, 'repeticoes': '10-12', 'carga': 'Média'},
                    {'nome': 'Tríceps Testa', 'series': 3, 'repeticoes': '12-15', 'carga': 'Leve'}
                ],
                'B - Pull (Puxar)': [
                    {'nome': 'Barra Fixa', 'series': 4, 'repeticoes': '6-10', 'carga': 'Progressiva'},
                    {'nome': 'Remada Curvada', 'series': 4, 'repeticoes': '8-12', 'carga': 'Pesada'},
                    {'nome': 'Pull-down Frente', 'series': 3, 'repeticoes': '10-12', 'carga': 'Média'},
                    {'nome': 'Remada Cavalinho', 'series': 3, 'repeticoes': '12-15', 'carga': 'Média'},
                    {'nome': 'Rosca Direta', 'series': 3, 'repeticoes': '10-12', 'carga': 'Média'},
                    {'nome': 'Rosca Martelo', 'series': 3, 'repeticoes': '12-15', 'carga': 'Leve'}
                ],
                'C - Legs (Pernas)': [
                    {'nome': 'Agachamento Livre', 'series': 5, 'repeticoes': '6-10', 'carga': 'Pesada'},
                    {'nome': 'Leg Press 45°', 'series': 4, 'repeticoes': '10-15', 'carga': 'Progressiva'},
                    {'nome': 'Cadeira Extensora', 'series': 4, 'repeticoes': '12-15', 'carga': 'Média'},
                    {'nome': 'Mesa Flexora', 'series': 4, 'repeticoes': '12-15', 'carga': 'Média'},
                    {'nome': 'Panturrilha em Pé', 'series': 5, 'repeticoes': '15-20', 'carga': 'Progressiva'},
                    {'nome': 'Gêmeos Sentado', 'series': 4, 'repeticoes': '15-20', 'carga': 'Progressiva'}
                ]
            }
        }
        
        if divisao not in exercicios_base:
            divisao = DivisaoTreino.ABC
        
        treino = {
            'divisao': divisao.value,
            'dias_semana': 3 if divisao == DivisaoTreino.AB else 4,
            'cardio': '2x por semana - 20min moderado' if ciclo % 2 == 0 else '1x por semana - 15min leve',
            'sessoes': exercicios_base[divisao]
        }
        
        if ciclo % 2 == 0:
            for dia, exercicios in treino['sessoes'].items():
                for exercicio in exercicios:
                    if 'Progressiva' in exercicio['carga']:
                        exercicio['repeticoes'] = '12-15'
                        exercicio['series'] += 1
        else:
            for dia, exercicios in treino['sessoes'].items():
                for exercicio in exercicios:
                    if 'Progressiva' in exercicio['carga']:
                        exercicio['repeticoes'] = '6-8'
        
        return treino
    
    def gerar_treino_perda_peso(self, usuario: Dict) -> Dict:
        nivel = Nivel(usuario['nivel'])
        ciclo = usuario['ciclo_atual']
        divisao = self.determinar_divisao_treino(nivel, Objetivo.PERDER_PESO)
        
        exercicios_base = {
            DivisaoTreino.AB: {
                'A - Superior + Cardio': [
                    {'nome': 'Supino Reto com Halteres', 'series': 4, 'repeticoes': '12-15', 'descanso': '30s'},
                    {'nome': 'Remada Curvada', 'series': 4, 'repeticoes': '12-15', 'descanso': '30s'},
                    {'nome': 'Desenvolvimento Arnold', 'series': 3, 'repeticoes': '15-20', 'descanso': '30s'},
                    {'nome': 'Pull-down Frente', 'series': 3, 'repeticoes': '15-20', 'descanso': '30s'},
                    {'nome': 'Burpees', 'series': 4, 'repeticoes': '10-12', 'descanso': '45s'},
                    {'nome': 'Cardio - Esteira Inclinada', 'series': 1, 'duracao': '20min', 'intensidade': '70%'}
                ],
                'B - Inferior + Cardio': [
                    {'nome': 'Agachamento Goblet', 'series': 4, 'repeticoes': '15-20', 'descanso': '30s'},
                    {'nome': 'Leg Press 45°', 'series': 4, 'repeticoes': '15-20', 'descanso': '30s'},
                    {'nome': 'Afundos Alternados', 'series': 3, 'repeticoes': '12-15 cada', 'descanso': '30s'},
                    {'nome': 'Elevação Pélvica', 'series': 3, 'repeticoes': '15-20', 'descanso': '30s'},
                    {'nome': 'Jumping Jacks', 'series': 4, 'repeticoes': '30s', 'descanso': '30s'},
                    {'nome': 'Cardio - Bicicleta', 'series': 1, 'duracao': '20min', 'intensidade': '75%'}
                ]
            }
        }
        
        if divisao not in exercicios_base:
            divisao = DivisaoTreino.AB
        
        treino = {
            'divisao': divisao.value,
            'dias_semana': 4 if divisao == DivisaoTreino.AB else 5,
            'cardio_adicional': '1-2x por semana - 30min moderado',
            'sessoes': exercicios_base[divisao]
        }
        
        if ciclo % 3 == 0:
            for dia, exercicios in treino['sessoes'].items():
                for exercicio in exercicios:
                    if 'descanso' in exercicio:
                        exercicio['descanso'] = '15s'
                    if 'HIIT' in exercicio['nome']:
                        exercicio['series'] = 10
        
        return treino
    
    def gerar_treino_corrida(self, usuario: Dict) -> Dict:
        nivel = Nivel(usuario['nivel'])
        ciclo = usuario['ciclo_atual']
        divisao = self.determinar_divisao_treino(nivel, Objetivo.PERFORMANCE_CORRIDA)
        
        exercicios_base = {
            DivisaoTreino.AB: {
                'A - Inferior + Core': [
                    {'nome': 'Agachamento Livre', 'series': 4, 'repeticoes': '12-15', 'carga': 'Média'},
                    {'nome': 'Afundos em Caminhada', 'series': 3, 'repeticoes': '10 cada', 'carga': 'Corpo'},
                    {'nome': 'Elevação Pélvica', 'series': 4, 'repeticoes': '15-20', 'carga': 'Progressiva'},
                    {'nome': 'Panturrilha em Pé', 'series': 5, 'repeticoes': '20-25', 'carga': 'Progressiva'},
                    {'nome': 'Prancha Abdominal', 'series': 3, 'tempo': '60s', 'descanso': '30s'},
                    {'nome': 'Corrida Contínua', 'series': 1, 'distancia': '5km', 'ritmo': 'Confortável'}
                ],
                'B - Superior + Mobilidade': [
                    {'nome': 'Remada Curvada', 'series': 3, 'repeticoes': '12-15', 'carga': 'Leve'},
                    {'nome': 'Desenvolvimento Militar', 'series': 3, 'repeticoes': '12-15', 'carga': 'Leve'},
                    {'nome': 'Pull-down Frente', 'series': 3, 'repeticoes': '12-15', 'carga': 'Leve'},
                    {'nome': 'Elevação Lateral', 'series': 3, 'repeticoes': '15-20', 'carga': 'Leve'},
                    {'nome': 'Mobilidade Quadril', 'series': 3, 'tempo': '30s cada', 'exercicios': 'Alongamentos'},
                    {'nome': 'TIRO - 400m', 'series': 6, 'descanso': '2min', 'ritmo': 'Rápido'}
                ]
            }
        }
        
        if divisao not in exercicios_base:
            divisao = DivisaoTreino.AB
        
        treino = {
            'divisao': divisao.value,
            'dias_semana': 4 if divisao == DivisaoTreino.AB else 6,
            'sessoes': exercicios_base[divisao]
        }
        
        if ciclo % 3 == 0:
            for dia, exercicios in treino['sessoes'].items():
                for exercicio in exercicios:
                    if 'distancia' in exercicio:
                        if nivel == Nivel.INICIANTE:
                            exercicio['distancia'] = '6km'
                        else:
                            exercicio['distancia'] = '16km'
        
        return treino
    
    def gerar_treino_futebol(self, usuario: Dict) -> Dict:
        nivel = Nivel(usuario['nivel'])
        ciclo = usuario['ciclo_atual']
        divisao = self.determinar_divisao_treino(nivel, Objetivo.PERFORMANCE_FUTEBOL)
        
        exercicios_base = {
            DivisaoTreino.AB: {
                'A - Inferior + Potência': [
                    {'nome': 'Agachamento Livre', 'series': 4, 'repeticoes': '8-12', 'carga': 'Progressiva'},
                    {'nome': 'Leg Press 45°', 'series': 4, 'repeticoes': '10-15', 'carga': 'Progressiva'},
                    {'nome': 'Cadeira Extensora', 'series': 3, 'repeticoes': '12-15', 'carga': 'Média'},
                    {'nome': 'Afundos Estáticos', 'series': 3, 'repeticoes': '10 cada perna', 'carga': 'Média'},
                    {'nome': 'Panturrilha em Pé', 'series': 4, 'repeticoes': '15-20', 'carga': 'Progressiva'},
                    {'nome': 'Pulo Caixa', 'series': 4, 'repeticoes': '8', 'altura': 'Progressiva'}
                ],
                'B - Superior + Velocidade': [
                    {'nome': 'Remada Curvada', 'series': 4, 'repeticoes': '8-12', 'carga': 'Média'},
                    {'nome': 'Desenvolvimento Militar', 'series': 3, 'repeticoes': '10-12', 'carga': 'Média'},
                    {'nome': 'Pull-down Frente', 'series': 3, 'repeticoes': '10-15', 'carga': 'Média'},
                    {'nome': 'Supino Reto', 'series': 3, 'repeticoes': '10-12', 'carga': 'Média'},
                    {'nome': 'Sprints - 20m', 'series': 6, 'descanso': '60s', 'intensidade': 'Máxima'},
                    {'nome': 'Shuttle Run', 'series': 4, 'descanso': '90s', 'distancia': '5-10-5'}
                ]
            }
        }
        
        if divisao not in exercicios_base:
            divisao = DivisaoTreino.AB
        
        treino = {
            'divisao': divisao.value,
            'dias_semana': 3 if divisao == DivisaoTreino.AB else 4,
            'observacoes': 'Integrar com treinos de futebol específicos',
            'sessoes': exercicios_base[divisao]
        }
        
        if ciclo % 2 == 0:
            for dia, exercicios in treino['sessoes'].items():
                for exercicio in exercicios:
                    if 'carga' in exercicio and exercicio['carga'] == 'Pesada':
                        exercicio['repeticoes'] = '8-12'
                        exercicio['series'] = 4
        else:
            for dia, exercicios in treino['sessoes'].items():
                for exercicio in exercicios:
                    if 'carga' in exercicio and exercicio['carga'] == 'Pesada':
                        exercicio['repeticoes'] = '3-5'
        
        return treino
    
    def gerar_treino_usuario(self, usuario: Dict) -> Dict:
        objetivo = Objetivo(usuario['objetivo'])
        
        treinos = {
            Objetivo.GANHAR_MASSA: self.gerar_treino_massa,
            Objetivo.PERDER_PESO: self.gerar_treino_perda_peso,
            Objetivo.PERFORMANCE_CORRIDA: self.gerar_treino_corrida,
            Objetivo.PERFORMANCE_FUTEBOL: self.gerar_treino_futebol
        }
        
        return treinos[objetivo](usuario)
    
    def verificar_troca_ciclo(self, usuario: Dict) -> bool:
        ultima_troca = datetime.datetime.fromisoformat(usuario['ultima_troca'])
        dias_desde_troca = (datetime.datetime.now() - ultima_troca).days
        return dias_desde_troca >= 21
    
    def atualizar_ciclo(self, usuario_id: int):
        for usuario in st.session_state.usuarios:
            if usuario['id'] == usuario_id:
                if self.verificar_troca_ciclo(usuario):
                    usuario['ciclo_atual'] += 1
                    usuario['ultima_troca'] = datetime.datetime.now().isoformat()
                    self.salvar_dados()
                    st.success(f"Ciclo atualizado para {usuario['nome']}! Novo ciclo: {usuario['ciclo_atual']}")
                break
    
    def pagina_listar_usuarios(self):
        st.header("👥 Usuários Cadastrados")
        
        if not st.session_state.usuarios:
            st.info("Nenhum usuário cadastrado ainda.")
            return
        
        dados_tabela = []
        for usuario in st.session_state.usuarios:
            dados_tabela.append({
                'ID': usuario['id'],
                'Nome': usuario['nome'],
                'Idade': usuario['idade'],
                'Peso': f"{usuario['peso']}kg",
                'Altura': f"{usuario['altura']}m",
                'Nível': usuario['nivel'].title(),
                'Objetivo': usuario['objetivo'].replace('_', ' ').title(),
                'Ciclo': usuario['ciclo_atual']
            })
        
        df = pd.DataFrame(dados_tabela)
        st.dataframe(df, use_container_width=True)
        
        # Estatísticas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Usuários", len(st.session_state.usuarios))
        with col2:
            st.metric("Limite Disponível", 5 - len(st.session_state.usuarios))
        with col3:
            if st.session_state.usuarios:
                imc_medio = sum(self.calcular_imc(u['peso'], u['altura']) for u in st.session_state.usuarios) / len(st.session_state.usuarios)
                st.metric("IMC Médio", f"{imc_medio:.1f}")
    
    def pagina_gerar_treino(self):
        st.header("💪 Gerar Treino Personalizado")
        
        if not st.session_state.usuarios:
            st.warning("Cadastre pelo menos um usuário primeiro!")
            return
        
        usuarios_options = {f"{u['id']} - {u['nome']}": u['id'] for u in st.session_state.usuarios}
        usuario_selecionado = st.selectbox(
            "Selecione o usuário:",
            options=list(usuarios_options.keys())
        )
        
        if usuario_selecionado:
            usuario_id = usuarios_options[usuario_selecionado]
            usuario = next((u for u in st.session_state.usuarios if u['id'] == usuario_id), None)
            
            if usuario and st.button("Gerar Treino", type="primary"):
                self.atualizar_ciclo(usuario_id)
                
                # Informações do usuário
                st.subheader(f"📊 Informações de {usuario['nome']}")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Idade", usuario['idade'])
                with col2:
                    st.metric("Peso", f"{usuario['peso']}kg")
                with col3:
                    st.metric("Altura", f"{usuario['altura']}m")
                with col4:
                    imc = self.calcular_imc(usuario['peso'], usuario['altura'])
                    st.metric("IMC", f"{imc:.1f}")
                
                # Gerar treino
                treino = self.gerar_treino_usuario(usuario)
                
                # Informações do treino
                st.subheader("🎯 Plano de Treino")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.info(f"**Divisão:** {treino['divisao']}")
                    st.info(f"**Dias na semana:** {treino['dias_semana']}")
                
                with col2:
                    st.info(f"**Ciclo atual:** {usuario['ciclo_atual']}")
                    if 'cardio' in treino:
                        st.info(f"**Cardio:** {treino['cardio']}")
                    if 'cardio_adicional' in treino:
                        st.info(f"**Cardio adicional:** {treino['cardio_adicional']}")
                
                if 'observacoes' in treino:
                    st.warning(f"**Observações:** {treino['observacoes']}")
                
                # Sessões de treino
                for dia, exercicios in treino['sessoes'].items():
                    with st.expander(f"📅 {dia}", expanded=True):
                        for i, exercicio in enumerate(exercicios, 1):
                            with st.container():
                                col1, col2 = st.columns([3, 2])
                                
                                with col1:
                                    st.write(f"**{i}. {exercicio['nome']}**")
                                
                                with col2:
                                    detalhes = []
                                    for key, value in exercicio.items():
                                        if key != 'nome':
                                            detalhes.append(f"**{key}:** {value}")
                                    st.write(" | ".join(detalhes))
                            
                            st.divider()
    
    def pagina_dashboard(self):
        st.header("📈 Dashboard de Progresso")
        
        if not st.session_state.usuarios:
            st.info("Nenhum dado disponível. Cadastre usuários primeiro.")
            return
        
        # Métricas gerais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_usuarios = len(st.session_state.usuarios)
            st.metric("Total de Usuários", total_usuarios)
        
        with col2:
            objetivos = [u['objetivo'] for u in st.session_state.usuarios]
            objetivo_mais_comum = max(set(objetivos), key=objetivos.count)
            st.metric("Objetivo Mais Comum", objetivo_mais_comum.replace('_', ' ').title())
        
        with col3:
            niveis = [u['nivel'] for u in st.session_state.usuarios]
            nivel_mais_comum = max(set(niveis), key=niveis.count)
            st.metric("Nível Mais Comum", nivel_mais_comum.title())
        
        with col4:
            ciclos_totais = sum(u['ciclo_atual'] for u in st.session_state.usuarios)
            st.metric("Ciclos Totais", ciclos_totais)
        
        # Gráfico de distribuição por objetivo
        st.subheader("Distribuição por Objetivo")
        objetivos_df = pd.DataFrame([u['objetivo'] for u in st.session_state.usuarios], columns=['Objetivo'])
        contagem_objetivos = objetivos_df['Objetivo'].value_counts()
        st.bar_chart(contagem_objetivos)
        
        # Tabela de IMC
        st.subheader("Análise de IMC")
        dados_imc = []
        for usuario in st.session_state.usuarios:
            imc = self.calcular_imc(usuario['peso'], usuario['altura'])
            classificacao = self.classificar_imc(imc)
            dados_imc.append({
                'Nome': usuario['nome'],
                'IMC': f"{imc:.1f}",
                'Classificação': classificacao,
                'Peso': f"{usuario['peso']}kg",
                'Altura': f"{usuario['altura']}m"
            })
        
        st.dataframe(pd.DataFrame(dados_imc), use_container_width=True)
    
    def classificar_imc(self, imc):
        if imc < 18.5:
            return "Abaixo do peso"
        elif imc < 25:
            return "Peso normal"
        elif imc < 30:
            return "Sobrepeso"
        else:
            return "Obesidade"
    
    def executar(self):
        st.set_page_config(
            page_title="App de Treinamento Personalizado",
            page_icon="💪",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Inicializar session state se necessário
        if 'usuarios' not in st.session_state:
            st.session_state.usuarios = []
        
        # Sidebar
        st.sidebar.title("💪 App de Treinamento")
        st.sidebar.markdown("---")
        
        pagina = st.sidebar.radio(
            "Navegação",
            ["🏠 Dashboard", "📝 Cadastrar Usuário", "👥 Listar Usuários", "💪 Gerar Treino"]
        )
        
        st.sidebar.markdown("---")
        st.sidebar.info(
            "**Desenvolvido para:**\n"
            "• Ganho de Massa Muscular\n"
            "• Perda de Peso\n"
            "• Performance na Corrida\n"
            "• Performance no Futebol"
        )
        
        # Conteúdo principal
        if pagina == "🏠 Dashboard":
            self.pagina_dashboard()
        elif pagina == "📝 Cadastrar Usuário":
            self.pagina_cadastro_usuario()
        elif pagina == "👥 Listar Usuários":
            self.pagina_listar_usuarios()
        elif pagina == "💪 Gerar Treino":
            self.pagina_gerar_treino()

if __name__ == "__main__":
    app = AppTreinamentoStreamlit()
    app.executar()
