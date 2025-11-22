import json
import datetime
from enum import Enum
from typing import Dict
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
        """Carrega os dados dos usuários do arquivo JSON"""
        try:
            with open(self.arquivo_dados, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                if 'usuarios' not in st.session_state:
                    st.session_state.usuarios = dados.get('usuarios', [])
        except (FileNotFoundError, json.JSONDecodeError):
            if 'usuarios' not in st.session_state:
                st.session_state.usuarios = []
    
    def salvar_dados(self):
        """Salva os dados dos usuários no arquivo JSON"""
        dados = {'usuarios': st.session_state.usuarios}
        try:
            with open(self.arquivo_dados, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
        except Exception as e:
            st.error(f"Erro ao salvar dados: {e}")
    
    def pagina_cadastro_usuario(self):
        st.header("📝 Cadastro de Usuário")
        
        if len(st.session_state.get('usuarios', [])) >= 5:
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
        """Calcula o IMC"""
        return peso / (altura ** 2)
    
    def determinar_divisao_treino(self, nivel: Nivel, objetivo: Objetivo) -> DivisaoTreino:
        """Determina a divisão de treino baseada no nível e objetivo"""
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
        """Gera treino para ganho de massa muscular"""
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
        
        # Usar ABC como fallback se divisão não estiver definida
        treino_base = exercicios_base.get(divisao, exercicios_base[DivisaoTreino.ABC])
        
        treino = {
            'divisao': divisao.value,
            'dias_semana': 3 if divisao == DivisaoTreino.AB else 4,
            'cardio': '2x por semana - 20min moderado' if ciclo % 2 == 0 else '1x por semana - 15min leve',
            'sessoes': treino_base
        }
        
        return treino
    
    def gerar_treino_perda_peso(self, usuario: Dict) -> Dict:
        """Gera treino para perda de peso"""
        nivel = Nivel(usuario['nivel'])
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
        
        treino_base = exercicios_base.get(divisao, exercicios_base[DivisaoTreino.AB])
        
        treino = {
            'divisao': divisao.value,
            'dias_semana': 4,
            'cardio_adicional': '1-2x por semana - 30min moderado',
            'sessoes': treino_base
        }
        
        return treino
    
    def gerar_treino_corrida(self, usuario: Dict) -> Dict:
        """Gera treino para performance na corrida"""
        nivel = Nivel(usuario['nivel'])
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
        
        treino_base = exercicios_base.get(divisao, exercicios_base[DivisaoTreino.AB])
        
        treino = {
            'divisao': divisao.value,
            'dias_semana': 4,
            'sessoes': treino_base
        }
        
        return treino
    
    def gerar_treino_futebol(self, usuario: Dict) -> Dict:
        """Gera treino para performance no futebol"""
        nivel = Nivel(usuario['nivel'])
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
        
        treino_base = exercicios_base.get(divisao, exercicios_base[DivisaoTreino.AB])
        
        treino = {
            'divisao': divisao.value,
            'dias_semana': 3,
            'observacoes': 'Integrar com treinos de futebol específicos',
            'sessoes': treino_base
        }
        
        return treino
    
    def gerar_treino_usuario(self, usuario: Dict) -> Dict:
        """Gera o treino baseado no objetivo do usuário"""
        objetivo = Objetivo(usuario['objetivo'])
        
        treinos = {
            Objetivo.GANHAR_MASSA: self.gerar_treino_massa,
            Objetivo.PERDER_PESO: self.gerar_treino_perda_peso,
            Objetivo.PERFORMANCE_CORRIDA: self.gerar_treino_corrida,
            Objetivo.PERFORMANCE_FUTEBOL: self.gerar_treino_futebol
        }
        
        return treinos[objetivo](usuario)
    
    def pagina_listar_usuarios(self):
        st.header("👥 Usuários Cadastrados")
        
        usuarios = st.session_state.get('usuarios', [])
        if not usuarios:
            st.info("Nenhum usuário cadastrado ainda.")
            return
        
        # Criar DataFrame para exibição
        dados_tabela = []
        for usuario in usuarios:
            imc = self.calcular_imc(usuario['peso'], usuario['altura'])
            dados_tabela.append({
                'ID': usuario['id'],
                'Nome': usuario['nome'],
                'Idade': usuario['idade'],
                'Peso': f"{usuario['peso']}kg",
                'Altura': f"{usuario['altura']}m",
                'IMC': f"{imc:.1f}",
                'Nível': usuario['nivel'].title(),
                'Objetivo': usuario['objetivo'].replace('_', ' ').title(),
                'Ciclo': usuario['ciclo_atual']
            })
        
        df = pd.DataFrame(dados_tabela)
        st.dataframe(df, use_container_width=True)
        
        # Estatísticas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Usuários", len(usuarios))
        with col2:
            st.metric("Limite Disponível", 5 - len(usuarios))
        with col3:
            if usuarios:
                idade_media = sum(u['idade'] for u in usuarios) / len(usuarios)
                st.metric("Idade Média", f"{idade_media:.1f}")
    
    def pagina_gerar_treino(self):
        st.header("💪 Gerar Treino Personalizado")
        
        usuarios = st.session_state.get('usuarios', [])
        if not usuarios:
            st.warning("Cadastre pelo menos um usuário primeiro!")
            return
        
        # Selecionar usuário
        usuario_selecionado = st.selectbox(
            "Selecione o usuário:",
            options=usuarios,
            format_func=lambda u: f"{u['id']} - {u['nome']} ({u['objetivo'].replace('_', ' ').title()})"
        )
        
        if usuario_selecionado and st.button("Gerar Treino", type="primary"):
            # Informações do usuário
            st.subheader(f"📊 Informações de {usuario_selecionado['nome']}")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Idade", usuario_selecionado['idade'])
            with col2:
                st.metric("Peso", f"{usuario_selecionado['peso']}kg")
            with col3:
                st.metric("Altura", f"{usuario_selecionado['altura']}m")
            with col4:
                imc = self.calcular_imc(usuario_selecionado['peso'], usuario_selecionado['altura'])
                st.metric("IMC", f"{imc:.1f}")
            
            # Gerar e exibir treino
            treino = self.gerar_treino_usuario(usuario_selecionado)
            
            st.subheader("🎯 Plano de Treino")
            
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**Divisão:** {treino['divisao']}")
                st.info(f"**Dias na semana:** {treino['dias_semana']}")
            with col2:
                st.info(f"**Ciclo atual:** {usuario_selecionado['ciclo_atual']}")
                if 'cardio' in treino:
                    st.info(f"**Cardio:** {treino['cardio']}")
            
            # Exibir sessões de treino
            for dia, exercicios in treino['sessoes'].items():
                with st.expander(f"📅 {dia}", expanded=True):
                    for i, exercicio in enumerate(exercicios, 1):
                        st.write(f"**{i}. {exercicio['nome']}**")
                        detalhes = []
                        for key, value in exercicio.items():
                            if key != 'nome':
                                detalhes.append(f"**{key}:** {value}")
                        st.write(" | ".join(detalhes))
                        st.divider()
    
    def pagina_dashboard(self):
        st.header("📈 Dashboard de Progresso")
        
        usuarios = st.session_state.get('usuarios', [])
        if not usuarios:
            st.info("Nenhum dado disponível. Cadastre usuários primeiro.")
            return
        
        # Métricas gerais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total de Usuários", len(usuarios))
        
        with col2:
            objetivos = [u['objetivo'] for u in usuarios]
            objetivo_mais_comum = max(set(objetivos), key=objetivos.count)
            st.metric("Objetivo Mais Comum", objetivo_mais_comum.replace('_', ' ').title())
        
        with col3:
            niveis = [u['nivel'] for u in usuarios]
            nivel_mais_comum = max(set(niveis), key=niveis.count)
            st.metric("Nível Mais Comum", nivel_mais_comum.title())
        
        with col4:
            ciclos_totais = sum(u['ciclo_atual'] for u in usuarios)
            st.metric("Ciclos Totais", ciclos_totais)
        
        # Distribuição por objetivo
        st.subheader("Distribuição por Objetivo")
        objetivos_df = pd.DataFrame([u['objetivo'] for u in usuarios], columns=['Objetivo'])
        contagem_objetivos = objetivos_df['Objetivo'].value_counts()
        st.bar_chart(contagem_objetivos)
    
    def executar(self):
        # Configuração da página
        st.set_page_config(
            page_title="App de Treinamento Personalizado",
            page_icon="💪",
            layout="wide"
        )
        
        # Inicializar session state se necessário
        if 'usuarios' not in st.session_state:
            st.session_state.usuarios = []
        
        # Sidebar com navegação
        st.sidebar.title("💪 App de Treinamento")
        st.sidebar.markdown("---")
        
        pagina = st.sidebar.radio(
            "Navegação",
            ["🏠 Dashboard", "📝 Cadastrar Usuário", "👥 Listar Usuários", "💪 Gerar Treino"]
        )
        
        st.sidebar.markdown("---")
        st.sidebar.info(
            "**Sistema de Treinamento Personalizado**\n\n"
            "• Ganho de Massa Muscular\n"
            "• Perda de Peso\n"
            "• Performance na Corrida\n"
            "• Performance no Futebol"
        )
        
        # Navegação entre páginas
        if pagina == "🏠 Dashboard":
            self.pagina_dashboard()
        elif pagina == "📝 Cadastrar Usuário":
            self.pagina_cadastro_usuario()
        elif pagina == "👥 Listar Usuários":
            self.pagina_listar_usuarios()
        elif pagina == "💪 Gerar Treino":
            self.pagina_gerar_treino()

# Executar o app
if __name__ == "__main__":
    app = AppTreinamentoStreamlit()
    app.executar()
