import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import hashlib

class SistemaCadastroCandidatos:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Cadastro de Candidatos - Moderno")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f8f9fa')
        
        # Configurar estilo moderno
        self.configurar_estilo()
        
        self.criar_banco_dados()
        self.tela_inicial()
        
    def configurar_estilo(self):
        """Configura estilos modernos para os componentes"""
        style = ttk.Style()
        
        # Configurar tema
        style.theme_use('clam')
        
        # Cores modernas
        self.cor_primaria = '#2c3e50'
        self.cor_secundaria = '#3498db'
        self.cor_sucesso = '#27ae60'
        self.cor_alerta = '#e74c3c'
        self.cor_aviso = '#f39c12'
        self.cor_info = '#3498db'
        self.cor_fundo = '#ecf0f1'
        self.cor_texto = '#2c3e50'
        self.cor_borda = '#bdc3c7'
        
        # Configurar estilos personalizados
        style.configure('Titulo.TLabel', 
                       font=('Segoe UI', 18, 'bold'),
                       foreground=self.cor_primaria,
                       background=self.cor_fundo)
        
        style.configure('Subtitulo.TLabel',
                       font=('Segoe UI', 12),
                       foreground='#7f8c8d',
                       background=self.cor_fundo)
        
        style.configure('Card.TFrame',
                       background='white')
        
        # Configurar botões coloridos
        style.configure('Primario.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       background=self.cor_secundaria,
                       foreground='white')
        
        style.configure('Sucesso.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       background=self.cor_sucesso,
                       foreground='white')
        
        style.configure('Alerta.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       background=self.cor_alerta,
                       foreground='white')
        
        style.configure('Aviso.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       background=self.cor_aviso,
                       foreground='white')
        
        style.configure('Info.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       background=self.cor_info,
                       foreground='white')
        
        # Configurar Treeview
        style.configure('Treeview',
                       font=('Segoe UI', 9),
                       rowheight=25)
        
        style.configure('Treeview.Heading',
                       font=('Segoe UI', 10, 'bold'),
                       background=self.cor_primaria,
                       foreground='white')
        
    def criar_banco_dados(self):
        """Cria as tabelas necessárias no banco de dados"""
        conn = sqlite3.connect('sistema_candidatos.db')
        cursor = conn.cursor()
        
        # Tabela de usuários
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                perfil TEXT NOT NULL,
                ativo INTEGER DEFAULT 1
            )
        ''')
        
        # Tabela de candidatos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS candidatos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                telefone TEXT NOT NULL,
                cep TEXT NOT NULL,
                rua TEXT NOT NULL,
                numero TEXT NOT NULL,
                cpf TEXT UNIQUE NOT NULL,
                estado_civil TEXT NOT NULL,
                escolaridade TEXT NOT NULL,
                data_nascimento TEXT NOT NULL,
                data_cadastro TEXT NOT NULL,
                status TEXT DEFAULT 'Candidato'
            )
        ''')
        
        # Tabela de funcionários
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS funcionarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                candidato_id INTEGER UNIQUE,
                secao TEXT NOT NULL,
                funcao TEXT NOT NULL,
                horario TEXT NOT NULL,
                salario REAL NOT NULL,
                data_admissao TEXT NOT NULL,
                tipo_funcionario TEXT NOT NULL,
                tipo_recebimento TEXT NOT NULL,
                status TEXT DEFAULT 'Pendente DP',
                observacoes TEXT,
                FOREIGN KEY (candidato_id) REFERENCES candidatos (id)
            )
        ''')
        
        # Inserir usuário mestre se não existir
        cursor.execute('SELECT * FROM usuarios WHERE username = "admin"')
        if not cursor.fetchone():
            senha_hash = hashlib.sha256("admin123".encode()).hexdigest()
            cursor.execute(
                'INSERT INTO usuarios (username, password, perfil) VALUES (?, ?, ?)',
                ('admin', senha_hash, 'Mestre')
            )
        
        conn.commit()
        conn.close()
    
    def criar_card(self, parent, titulo="", padding=20):
        """Cria um card moderno"""
        card = ttk.Frame(parent, style='Card.TFrame', padding=padding)
        card.pack(fill='x', pady=10)
        
        if titulo:
            lbl_titulo = tk.Label(card, text=titulo, font=('Segoe UI', 12, 'bold'), 
                                 bg='white', fg=self.cor_primaria)
            lbl_titulo.pack(anchor='w', pady=(0, 15))
        
        return card
    
    def criar_botao(self, parent, texto, comando, estilo='Primario.TButton', **kwargs):
        """Cria um botão moderno"""
        return ttk.Button(parent, text=texto, command=comando, style=estilo, **kwargs)
    
    def tela_inicial(self):
        """Tela inicial com login e opção para candidatos"""
        self.limpar_tela()
        
        # Container principal
        container_principal = tk.Frame(self.root, bg=self.cor_fundo)
        container_principal.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Cabeçalho
        header_frame = tk.Frame(container_principal, bg=self.cor_fundo)
        header_frame.pack(fill='x', pady=(0, 40))
        
        lbl_titulo = tk.Label(header_frame, text="Sistema de Cadastro de Candidatos", 
                             font=('Segoe UI', 18, 'bold'), bg=self.cor_fundo, fg=self.cor_primaria)
        lbl_titulo.pack(pady=10)
        
        lbl_subtitulo = tk.Label(header_frame, text="Soluções em Gestão de Pessoas", 
                                font=('Segoe UI', 12), bg=self.cor_fundo, fg='#7f8c8d')
        lbl_subtitulo.pack()
        
        # Frame principal com layout em grid
        main_frame = tk.Frame(container_principal, bg=self.cor_fundo)
        main_frame.pack(fill='both', expand=True)
        
        # Coluna da esquerda - Login Colaboradores
        left_frame = self.criar_card(main_frame, "👥 Área do Colaborador")
        
        lbl_acesso = tk.Label(left_frame, text="Acesso Restrito", 
                             font=('Segoe UI', 12, 'bold'), bg='white', fg=self.cor_primaria)
        lbl_acesso.pack(pady=(0, 20))
        
        # Formulário de login
        form_frame = tk.Frame(left_frame, bg='white')
        form_frame.pack(fill='x', pady=10)
        
        lbl_usuario = tk.Label(form_frame, text="Usuário:", font=('Segoe UI', 10), bg='white')
        lbl_usuario.grid(row=0, column=0, sticky='w', pady=8, padx=(0, 10))
        
        self.entry_usuario = ttk.Entry(form_frame, width=25, font=('Segoe UI', 10))
        self.entry_usuario.grid(row=0, column=1, padx=10, pady=8, sticky='ew')
        
        lbl_senha = tk.Label(form_frame, text="Senha:", font=('Segoe UI', 10), bg='white')
        lbl_senha.grid(row=1, column=0, sticky='w', pady=8, padx=(0, 10))
        
        self.entry_senha = ttk.Entry(form_frame, width=25, show="•", font=('Segoe UI', 10))
        self.entry_senha.grid(row=1, column=1, padx=10, pady=8, sticky='ew')
        
        form_frame.columnconfigure(1, weight=1)
        
        btn_login = self.criar_botao(
            left_frame,
            texto="🚀 Entrar no Sistema",
            comando=self.fazer_login,
            estilo='Sucesso.TButton'
        )
        btn_login.pack(pady=20)
        
        # Coluna da direita - Área do Candidato
        right_frame = self.criar_card(main_frame, "👤 Área do Candidato")
        
        lbl_cadastro = tk.Label(right_frame, text="Cadastro Online", 
                               font=('Segoe UI', 12, 'bold'), bg='white', fg=self.cor_primaria)
        lbl_cadastro.pack(pady=(0, 20))
        
        lbl_info1 = tk.Label(right_frame, text="Interessado em fazer parte da nossa equipe?", 
                            font=('Segoe UI', 10), bg='white', fg='#7f8c8d')
        lbl_info1.pack(pady=8)
        
        lbl_info2 = tk.Label(right_frame, text="Cadastre seu currículo em nosso banco de talentos.", 
                            font=('Segoe UI', 9), bg='white', fg='#95a5a6')
        lbl_info2.pack(pady=8)
        
        btn_candidato = self.criar_botao(
            right_frame,
            texto="📝 Fazer Meu Cadastro",
            comando=self.tela_cadastro_candidato,
            estilo='Info.TButton'
        )
        btn_candidato.pack(pady=20)
        
        # Configurar layout em grid
        left_frame.pack(side='left', fill='both', expand=True, padx=10)
        right_frame.pack(side='right', fill='both', expand=True, padx=10)
        
        # Rodapé
        footer_frame = tk.Frame(container_principal, bg=self.cor_fundo)
        footer_frame.pack(fill='x', pady=20)
        
        lbl_rodape = tk.Label(footer_frame, 
                             text="Sistema desenvolvido para gestão de candidatos e funcionários",
                             font=('Segoe UI', 9), bg=self.cor_fundo, fg='#bdc3c7')
        lbl_rodape.pack()
        
        # Focar no campo de usuário
        self.entry_usuario.focus()
    
    def fazer_login(self):
        """Processa o login do usuário"""
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
        
        if not usuario or not senha:
            messagebox.showerror("Erro", "Preencha usuário e senha!")
            return
        
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        
        conn = sqlite3.connect('sistema_candidatos.db')
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM usuarios WHERE username = ? AND password = ? AND ativo = 1',
            (usuario, senha_hash)
        )
        usuario_data = cursor.fetchone()
        conn.close()
        
        if usuario_data:
            self.usuario_logado = {
                'id': usuario_data[0],
                'username': usuario_data[1],
                'perfil': usuario_data[3]
            }
            self.redirecionar_apos_login()
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos!")
    
    def redirecionar_apos_login(self):
        """Redireciona para a tela apropriada baseada no perfil"""
        perfil = self.usuario_logado['perfil']
        
        if perfil == 'Mestre':
            self.tela_usuario_mestre()
        elif perfil == 'RH':
            self.tela_rh()
        elif perfil == 'DP':
            self.tela_dp()
        elif perfil == 'Ambos':
            self.tela_selecao_perfil()
    
    def tela_selecao_perfil(self):
        """Tela para usuários com acesso a ambos os perfis"""
        self.limpar_tela()
        
        container = tk.Frame(self.root, bg=self.cor_fundo, padx=40, pady=40)
        container.pack(fill='both', expand=True)
        
        lbl_titulo = tk.Label(container, text="Selecione o Perfil de Acesso", 
                             font=('Segoe UI', 18, 'bold'), bg=self.cor_fundo, fg=self.cor_primaria)
        lbl_titulo.pack(pady=20)
        
        lbl_subtitulo = tk.Label(container, text="Escolha como deseja acessar o sistema:", 
                                font=('Segoe UI', 12), bg=self.cor_fundo, fg='#7f8c8d')
        lbl_subtitulo.pack(pady=10)
        
        # Frame dos botões
        botoes_frame = tk.Frame(container, bg=self.cor_fundo)
        botoes_frame.pack(pady=40)
        
        btn_rh = self.criar_botao(
            botoes_frame,
            texto="👨‍💼 RH - Recursos Humanos\n\nGerenciar candidatos e admissões",
            comando=self.tela_rh,
            estilo='Aviso.TButton'
        )
        btn_rh.grid(row=0, column=0, padx=15, pady=10, ipady=10)
        
        btn_dp = self.criar_botao(
            botoes_frame,
            texto="📋 DP - Departamento Pessoal\n\nValidar admissões e documentos",
            comando=self.tela_dp,
            estilo='Info.TButton'
        )
        btn_dp.grid(row=0, column=1, padx=15, pady=10, ipady=10)
        
        botoes_frame.columnconfigure(0, weight=1)
        botoes_frame.columnconfigure(1, weight=1)
        
        btn_voltar = self.criar_botao(
            container,
            texto="↩️ Voltar",
            comando=self.tela_inicial,
            estilo='Primario.TButton'
        )
        btn_voltar.pack(pady=20)
    
    def tela_cadastro_candidato(self):
        """Tela de cadastro para candidatos"""
        self.limpar_tela()
        
        # Container principal
        main_container = tk.Frame(self.root, bg=self.cor_fundo)
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_container, bg=self.cor_fundo)
        header_frame.pack(fill='x', pady=(0, 20))
        
        lbl_titulo = tk.Label(header_frame, text="📝 Cadastro de Candidato", 
                             font=('Segoe UI', 18, 'bold'), bg=self.cor_fundo, fg=self.cor_primaria)
        lbl_titulo.pack(pady=5)
        
        lbl_subtitulo = tk.Label(header_frame, text="Preencha seus dados para entrar em nosso banco de talentos", 
                                font=('Segoe UI', 12), bg=self.cor_fundo, fg='#7f8c8d')
        lbl_subtitulo.pack()
        
        # Container do formulário
        form_container = tk.Frame(main_container, bg=self.cor_fundo)
        form_container.pack(fill='both', expand=True)
        
        # Canvas e Scrollbar
        canvas = tk.Canvas(form_container, bg=self.cor_fundo, highlightthickness=0)
        scrollbar = ttk.Scrollbar(form_container, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.cor_fundo)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Card de informações pessoais
        card_pessoal = self.criar_card(scrollable_frame, "👤 Informações Pessoais")
        
        campos_pessoais = [
            ("Nome Completo:", "entry_nome"),
            ("Telefone:", "entry_telefone"),
            ("CPF:", "entry_cpf"),
            ("Data de Nascimento (DD/MM/AAAA):", "entry_data_nascimento"),
            ("Estado Civil:", "combo_estado_civil"),
            ("Escolaridade:", "combo_escolaridade")
        ]
        
        self.widgets_candidato = {}
        
        for i, (label, nome_widget) in enumerate(campos_pessoais):
            row_frame = tk.Frame(card_pessoal, bg='white')
            row_frame.pack(fill='x', pady=8)
            
            lbl = tk.Label(row_frame, text=label, width=30, anchor='e', bg='white', font=('Segoe UI', 9))
            lbl.pack(side='left', padx=(0, 10))
            
            if "combo" in nome_widget:
                if "estado_civil" in nome_widget:
                    opcoes = ["Solteiro", "Casado", "Separado", "Viúvo"]
                else:
                    opcoes = [
                        "Superior Cursando", "Superior Completo",
                        "Ensino Médio Completo", "Ensino Médio Cursando",
                        "Fundamental Completo", "Fundamental Incompleto"
                    ]
                
                combo = ttk.Combobox(row_frame, values=opcoes, state="readonly", width=30)
                combo.pack(side='left', fill='x', expand=True, padx=(0, 10))
                self.widgets_candidato[nome_widget] = combo
            else:
                entry = ttk.Entry(row_frame, width=30)
                entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
                self.widgets_candidato[nome_widget] = entry
        
        # Card de endereço
        card_endereco = self.criar_card(scrollable_frame, "🏠 Endereço")
        
        campos_endereco = [
            ("CEP:", "entry_cep"),
            ("Rua:", "entry_rua"),
            ("Número da casa:", "entry_numero")
        ]
        
        for i, (label, nome_widget) in enumerate(campos_endereco):
            row_frame = tk.Frame(card_endereco, bg='white')
            row_frame.pack(fill='x', pady=8)
            
            lbl = tk.Label(row_frame, text=label, width=30, anchor='e', bg='white', font=('Segoe UI', 9))
            lbl.pack(side='left', padx=(0, 10))
            
            entry = ttk.Entry(row_frame, width=30)
            entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
            self.widgets_candidato[nome_widget] = entry
        
        # Botões
        botoes_frame = tk.Frame(scrollable_frame, bg=self.cor_fundo, pady=20)
        botoes_frame.pack(fill='x')
        
        btn_cadastrar = self.criar_botao(
            botoes_frame,
            texto="✅ Cadastrar",
            comando=self.cadastrar_candidato,
            estilo='Sucesso.TButton'
        )
        btn_cadastrar.pack(side='right', padx=10)
        
        btn_voltar = self.criar_botao(
            botoes_frame,
            texto="↩️ Voltar",
            comando=self.tela_inicial,
            estilo='Primario.TButton'
        )
        btn_voltar.pack(side='right', padx=10)
        
        # Empacotar canvas e scrollbar
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def cadastrar_candidato(self):
        """Cadastra um novo candidato no sistema"""
        try:
            dados = {
                'nome': self.widgets_candidato['entry_nome'].get(),
                'telefone': self.widgets_candidato['entry_telefone'].get(),
                'cep': self.widgets_candidato['entry_cep'].get(),
                'rua': self.widgets_candidato['entry_rua'].get(),
                'numero': self.widgets_candidato['entry_numero'].get(),
                'cpf': self.widgets_candidato['entry_cpf'].get(),
                'estado_civil': self.widgets_candidato['combo_estado_civil'].get(),
                'escolaridade': self.widgets_candidato['combo_escolaridade'].get(),
                'data_nascimento': self.widgets_candidato['entry_data_nascimento'].get()
            }
            
            # Validação básica
            for campo, valor in dados.items():
                if not valor:
                    messagebox.showerror("Erro", f"Preencha o campo: {campo}")
                    return
            
            # Validar data
            try:
                datetime.strptime(dados['data_nascimento'], '%d/%m/%Y')
            except ValueError:
                messagebox.showerror("Erro", "Data de nascimento inválida! Use DD/MM/AAAA")
                return
            
            conn = sqlite3.connect('sistema_candidatos.db')
            cursor = conn.cursor()
            
            cursor.execute(
                '''INSERT INTO candidatos 
                (nome, telefone, cep, rua, numero, cpf, estado_civil, escolaridade, data_nascimento, data_cadastro)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (dados['nome'], dados['telefone'], dados['cep'], dados['rua'],
                 dados['numero'], dados['cpf'], dados['estado_civil'],
                 dados['escolaridade'], dados['data_nascimento'], 
                 datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
            )
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Sucesso", "✅ Cadastro realizado com sucesso!")
            self.tela_inicial()
            
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "❌ CPF já cadastrado no sistema!")
        except Exception as e:
            messagebox.showerror("Erro", f"❌ Erro ao cadastrar: {str(e)}")
    
    def tela_rh(self):
        """Tela principal do RH"""
        self.limpar_tela()
        
        container = tk.Frame(self.root, bg=self.cor_fundo, padx=20, pady=20)
        container.pack(fill='both', expand=True)
        
        # Header
        header_frame = tk.Frame(container, bg=self.cor_fundo)
        header_frame.pack(fill='x', pady=(0, 20))
        
        lbl_titulo = tk.Label(header_frame, text="👨‍💼 RH - Recursos Humanos", 
                             font=('Segoe UI', 18, 'bold'), bg=self.cor_fundo, fg=self.cor_primaria)
        lbl_titulo.pack(side='left')
        
        btn_voltar = self.criar_botao(
            header_frame,
            texto="↩️ Voltar",
            comando=self.tela_inicial,
            estilo='Primario.TButton'
        )
        btn_voltar.pack(side='right')
        
        # Abas
        notebook = ttk.Notebook(container)
        
        # Aba de candidatos
        frame_candidatos = ttk.Frame(notebook, padding=10)
        notebook.add(frame_candidatos, text="👥 Candidatos")
        
        lbl_candidatos = tk.Label(frame_candidatos, text="Lista de Candidatos", 
                                 font=('Segoe UI', 12, 'bold'), bg='white')
        lbl_candidatos.pack(pady=10)
        
        # Treeview
        tree_frame = tk.Frame(frame_candidatos)
        tree_frame.pack(fill='both', expand=True, pady=10)
        
        self.tree_candidatos = ttk.Treeview(
            tree_frame, 
            columns=("Nome", "CPF", "Status"), 
            show="headings",
            height=15
        )
        
        self.tree_candidatos.heading("Nome", text="Nome")
        self.tree_candidatos.heading("CPF", text="CPF")
        self.tree_candidatos.heading("Status", text="Status")
        
        self.tree_candidatos.column("Nome", width=200)
        self.tree_candidatos.column("CPF", width=150)
        self.tree_candidatos.column("Status", width=150)
        
        # Scrollbar para treeview
        tree_scroll = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree_candidatos.yview)
        self.tree_candidatos.configure(yscrollcommand=tree_scroll.set)
        
        self.tree_candidatos.pack(side='left', fill='both', expand=True)
        tree_scroll.pack(side='right', fill='y')
        
        btn_tornar_funcionario = self.criar_botao(
            frame_candidatos,
            texto="⭐ Tornar em Funcionário",
            comando=self.tela_tornar_funcionario,
            estilo='Aviso.TButton'
        )
        btn_tornar_funcionario.pack(pady=10)
        
        # Aba de admissões pendentes
        frame_pendentes = ttk.Frame(notebook, padding=10)
        notebook.add(frame_pendentes, text="⏳ Admissões Pendentes")
        
        lbl_pendentes = tk.Label(frame_pendentes, text="Admissões com Observações do DP", 
                                font=('Segoe UI', 12, 'bold'), bg='white')
        lbl_pendentes.pack(pady=10)
        
        tree_frame_pendentes = tk.Frame(frame_pendentes)
        tree_frame_pendentes.pack(fill='both', expand=True, pady=10)
        
        self.tree_pendentes = ttk.Treeview(
            tree_frame_pendentes,
            columns=("Nome", "Observações", "Status"), 
            show="headings",
            height=15
        )
        
        self.tree_pendentes.heading("Nome", text="Nome")
        self.tree_pendentes.heading("Observações", text="Observações")
        self.tree_pendentes.heading("Status", text="Status")
        
        self.tree_pendentes.column("Nome", width=150)
        self.tree_pendentes.column("Observações", width=300)
        self.tree_pendentes.column("Status", width=120)
        
        tree_scroll_pendentes = ttk.Scrollbar(tree_frame_pendentes, orient='vertical', command=self.tree_pendentes.yview)
        self.tree_pendentes.configure(yscrollcommand=tree_scroll_pendentes.set)
        
        self.tree_pendentes.pack(side='left', fill='both', expand=True)
        tree_scroll_pendentes.pack(side='right', fill='y')
        
        btn_editar_admissao = self.criar_botao(
            frame_pendentes,
            texto="✏️ Editar Admissão",
            comando=self.editar_admissao_pendente,
            estilo='Info.TButton'
        )
        btn_editar_admissao.pack(pady=10)
        
        notebook.pack(fill='both', expand=True, pady=10)
        
        self.carregar_candidatos_rh()
        self.carregar_admissoes_pendentes()
    
    def carregar_candidatos_rh(self):
        """Carrega a lista de candidatos para o RH"""
        for item in self.tree_candidatos.get_children():
            self.tree_candidatos.delete(item)
        
        conn = sqlite3.connect('sistema_candidatos.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, nome, cpf, status FROM candidatos')
        candidatos = cursor.fetchall()
        conn.close()
        
        for candidato in candidatos:
            self.tree_candidatos.insert("", "end", values=(candidato[1], candidato[2], candidato[3]), iid=candidato[0])
    
    def carregar_admissoes_pendentes(self):
        """Carrega admissões pendentes do RH"""
        for item in self.tree_pendentes.get_children():
            self.tree_pendentes.delete(item)
        
        conn = sqlite3.connect('sistema_candidatos.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT f.id, c.nome, f.observacoes, f.status 
            FROM funcionarios f 
            JOIN candidatos c ON f.candidato_id = c.id 
            WHERE f.status = 'Pendente RH' OR f.status = 'Rejeitado DP'
        ''')
        pendentes = cursor.fetchall()
        conn.close()
        
        for pendente in pendentes:
            status_color = "🔴 Rejeitado" if pendente[3] == "Rejeitado DP" else "🟡 Pendente"
            self.tree_pendentes.insert("", "end", values=(pendente[1], pendente[2], status_color), iid=pendente[0])
    
    def tela_tornar_funcionario(self):
        """Tela para transformar candidato em funcionário"""
        selecionado = self.tree_candidatos.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um candidato!")
            return
        
        candidato_id = selecionado[0]
        
        conn = sqlite3.connect('sistema_candidatos.db')
        cursor = conn.cursor()
        cursor.execute('SELECT nome FROM candidatos WHERE id = ?', (candidato_id,))
        nome_candidato = cursor.fetchone()[0]
        conn.close()
        
        self.limpar_tela()
        
        # Header
        header_frame = tk.Frame(self.root, bg=self.cor_fundo, padx=20, pady=20)
        header_frame.pack(fill='x')
        
        lbl_titulo = tk.Label(header_frame, text=f"Contratar: {nome_candidato}", 
                             font=('Segoe UI', 18, 'bold'), bg=self.cor_fundo, fg=self.cor_primaria)
        lbl_titulo.pack()
        
        # Formulário
        form_container = tk.Frame(self.root, bg=self.cor_fundo, padx=20, pady=20)
        form_container.pack(fill='both', expand=True)
        
        card_form = self.criar_card(form_container, "📋 Dados da Contratação")
        
        campos = [
            ("Seção:", "entry_secao"),
            ("Função:", "entry_funcao"),
            ("Horário:", "entry_horario"),
            ("Salário:", "entry_salario"),
            ("Data de Admissão (DD/MM/AAAA):", "entry_data_admissao"),
            ("Tipo de Funcionário:", "entry_tipo_funcionario"),
            ("Tipo de Recebimento:", "entry_tipo_recebimento")
        ]
        
        self.widgets_funcionario = {}
        
        for i, (label, nome_widget) in enumerate(campos):
            row_frame = tk.Frame(card_form, bg='white')
            row_frame.pack(fill='x', pady=8)
            
            lbl = tk.Label(row_frame, text=label, width=25, anchor='e', bg='white', font=('Segoe UI', 9))
            lbl.pack(side='left', padx=(0, 10))
            
            entry = ttk.Entry(row_frame, width=30)
            entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
            self.widgets_funcionario[nome_widget] = entry
        
        # Botões
        botoes_frame = tk.Frame(form_container, bg=self.cor_fundo, pady=20)
        botoes_frame.pack(fill='x')
        
        btn_confirmar = self.criar_botao(
            botoes_frame,
            texto="✅ Confirmar Contratação",
            comando=lambda: self.confirmar_contratacao(candidato_id),
            estilo='Sucesso.TButton'
        )
        btn_confirmar.pack(side='right', padx=10)
        
        btn_voltar = self.criar_botao(
            botoes_frame,
            texto="↩️ Voltar",
            comando=self.tela_rh,
            estilo='Primario.TButton'
        )
        btn_voltar.pack(side='right', padx=10)
    
    def confirmar_contratacao(self, candidato_id):
        """Confirma a contratação do candidato"""
        try:
            dados = {
                'secao': self.widgets_funcionario['entry_secao'].get(),
                'funcao': self.widgets_funcionario['entry_funcao'].get(),
                'horario': self.widgets_funcionario['entry_horario'].get(),
                'salario': self.widgets_funcionario['entry_salario'].get(),
                'data_admissao': self.widgets_funcionario['entry_data_admissao'].get(),
                'tipo_funcionario': self.widgets_funcionario['entry_tipo_funcionario'].get(),
                'tipo_recebimento': self.widgets_funcionario['entry_tipo_recebimento'].get()
            }
            
            # Validação
            for campo, valor in dados.items():
                if not valor:
                    messagebox.showerror("Erro", f"Preencha o campo: {campo}")
                    return
            
            # Validar data
            try:
                datetime.strptime(dados['data_admissao'], '%d/%m/%Y')
            except ValueError:
                messagebox.showerror("Erro", "Data de admissão inválida! Use DD/MM/AAAA")
                return
            
            # Validar salário
            try:
                float(dados['salario'])
            except ValueError:
                messagebox.showerror("Erro", "Salário deve ser um valor numérico!")
                return
            
            conn = sqlite3.connect('sistema_candidatos.db')
            cursor = conn.cursor()
            
            # Inserir funcionário
            cursor.execute(
                '''INSERT INTO funcionarios 
                (candidato_id, secao, funcao, horario, salario, data_admissao, tipo_funcionario, tipo_recebimento)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                (candidato_id, dados['secao'], dados['funcao'], dados['horario'],
                 float(dados['salario']), dados['data_admissao'], 
                 dados['tipo_funcionario'], dados['tipo_recebimento'])
            )
            
            # Atualizar status do candidato
            cursor.execute(
                'UPDATE candidatos SET status = "Funcionário Pendente" WHERE id = ?',
                (candidato_id,)
            )
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Sucesso", "Candidato contratado! Aguardando validação do DP.")
            self.tela_rh()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao contratar: {str(e)}")
    
    def editar_admissao_pendente(self):
        """Permite editar uma admissão pendente rejeitada pelo DP"""
        selecionado = self.tree_pendentes.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma admissão pendente!")
            return
        
        funcionario_id = selecionado[0]
        
        conn = sqlite3.connect('sistema_candidatos.db')
        cursor = conn.cursor()
        
        # Buscar dados do funcionário
        cursor.execute('''
            SELECT c.id, c.nome, f.secao, f.funcao, f.horario, f.salario, 
                   f.data_admissao, f.tipo_funcionario, f.tipo_recebimento, f.observacoes
            FROM funcionarios f 
            JOIN candidatos c ON f.candidato_id = c.id 
            WHERE f.id = ?
        ''', (funcionario_id,))
        
        funcionario = cursor.fetchone()
        conn.close()
        
        if not funcionario:
            messagebox.showerror("Erro", "Funcionário não encontrado!")
            return
        
        self.limpar_tela()
        
        # Header
        header_frame = tk.Frame(self.root, bg=self.cor_fundo, padx=20, pady=20)
        header_frame.pack(fill='x')
        
        lbl_titulo = tk.Label(header_frame, text=f"Editar Admissão: {funcionario[1]}", 
                             font=('Segoe UI', 18, 'bold'), bg=self.cor_fundo, fg=self.cor_primaria)
        lbl_titulo.pack()
        
        # Mostrar observações do DP
        if funcionario[9]:
            frame_obs = tk.Frame(self.root, bg='#ffebee', relief='solid', borderwidth=1, padx=10, pady=10)
            frame_obs.pack(fill='x', padx=20, pady=10)
            
            lbl_obs_titulo = tk.Label(frame_obs, text="Observações do DP:", 
                                     font=('Segoe UI', 10, 'bold'), bg='#ffebee', fg='#c62828')
            lbl_obs_titulo.pack(anchor='w')
            
            lbl_obs = tk.Label(frame_obs, text=funcionario[9], wraplength=600, 
                              justify='left', bg='#ffebee', font=('Segoe UI', 9))
            lbl_obs.pack(anchor='w')
        
        # Formulário
        form_container = tk.Frame(self.root, bg=self.cor_fundo, padx=20, pady=20)
        form_container.pack(fill='both', expand=True)
        
        card_form = self.criar_card(form_container, "✏️ Editar Dados da Admissão")
        
        campos = [
            ("Seção:", "entry_secao"),
            ("Função:", "entry_funcao"),
            ("Horário:", "entry_horario"),
            ("Salário:", "entry_salario"),
            ("Data de Admissão (DD/MM/AAAA):", "entry_data_admissao"),
            ("Tipo de Funcionário:", "entry_tipo_funcionario"),
            ("Tipo de Recebimento:", "entry_tipo_recebimento")
        ]
        
        # Valores padrão para os campos
        valores = [
            funcionario[2],  # secao
            funcionario[3],  # funcao
            funcionario[4],  # horario
            funcionario[5],  # salario
            funcionario[6],  # data_admissao
            funcionario[7],  # tipo_funcionario
            funcionario[8]   # tipo_recebimento
        ]
        
        self.widgets_funcionario_edicao = {}
        
        for i, (label, nome_widget) in enumerate(campos):
            row_frame = tk.Frame(card_form, bg='white')
            row_frame.pack(fill='x', pady=8)
            
            lbl = tk.Label(row_frame, text=label, width=25, anchor='e', bg='white', font=('Segoe UI', 9))
            lbl.pack(side='left', padx=(0, 10))
            
            entry = ttk.Entry(row_frame, width=30)
            entry.insert(0, str(valores[i]))
            entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
            self.widgets_funcionario_edicao[nome_widget] = entry
        
        # Botões
        botoes_frame = tk.Frame(form_container, bg=self.cor_fundo, pady=20)
        botoes_frame.pack(fill='x')
        
        btn_salvar = self.criar_botao(
            botoes_frame,
            texto="💾 Salvar Alterações",
            comando=lambda: self.salvar_edicao_admissao(funcionario_id, funcionario[0]),
            estilo='Sucesso.TButton'
        )
        btn_salvar.pack(side='right', padx=10)
        
        btn_cancelar = self.criar_botao(
            botoes_frame,
            texto="❌ Cancelar",
            comando=self.tela_rh,
            estilo='Alerta.TButton'
        )
        btn_cancelar.pack(side='right', padx=10)
    
    def salvar_edicao_admissao(self, funcionario_id, candidato_id):
        """Salva as alterações da admissão editada"""
        try:
            dados = {
                'secao': self.widgets_funcionario_edicao['entry_secao'].get(),
                'funcao': self.widgets_funcionario_edicao['entry_funcao'].get(),
                'horario': self.widgets_funcionario_edicao['entry_horario'].get(),
                'salario': self.widgets_funcionario_edicao['entry_salario'].get(),
                'data_admissao': self.widgets_funcionario_edicao['entry_data_admissao'].get(),
                'tipo_funcionario': self.widgets_funcionario_edicao['entry_tipo_funcionario'].get(),
                'tipo_recebimento': self.widgets_funcionario_edicao['entry_tipo_recebimento'].get()
            }
            
            # Validação
            for campo, valor in dados.items():
                if not valor:
                    messagebox.showerror("Erro", f"Preencha o campo: {campo}")
                    return
            
            # Validar data
            try:
                datetime.strptime(dados['data_admissao'], '%d/%m/%Y')
            except ValueError:
                messagebox.showerror("Erro", "Data de admissão inválida! Use DD/MM/AAAA")
                return
            
            # Validar salário
            try:
                float(dados['salario'])
            except ValueError:
                messagebox.showerror("Erro", "Salário deve ser um valor numérico!")
                return
            
            conn = sqlite3.connect('sistema_candidatos.db')
            cursor = conn.cursor()
            
            # Atualizar dados do funcionário
            cursor.execute(
                '''UPDATE funcionarios 
                SET secao = ?, funcao = ?, horario = ?, salario = ?, data_admissao = ?, 
                    tipo_funcionario = ?, tipo_recebimento = ?, status = 'Pendente DP', observacoes = NULL
                WHERE id = ?''',
                (dados['secao'], dados['funcao'], dados['horario'],
                 float(dados['salario']), dados['data_admissao'], 
                 dados['tipo_funcionario'], dados['tipo_recebimento'], funcionario_id)
            )
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Sucesso", "Admissão atualizada! Encaminhada para validação do DP.")
            self.tela_rh()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar alterações: {str(e)}")
    
    def tela_dp(self):
        """Tela principal do DP"""
        self.limpar_tela()
        
        container = tk.Frame(self.root, bg=self.cor_fundo, padx=20, pady=20)
        container.pack(fill='both', expand=True)
        
        # Header
        header_frame = tk.Frame(container, bg=self.cor_fundo)
        header_frame.pack(fill='x', pady=(0, 20))
        
        lbl_titulo = tk.Label(header_frame, text="📋 DP - Departamento Pessoal", 
                             font=('Segoe UI', 18, 'bold'), bg=self.cor_fundo, fg=self.cor_primaria)
        lbl_titulo.pack(side='left')
        
        btn_voltar = self.criar_botao(
            header_frame,
            texto="↩️ Voltar",
            comando=self.tela_inicial,
            estilo='Primario.TButton'
        )
        btn_voltar.pack(side='right')
        
        # Abas para o DP
        notebook = ttk.Notebook(container)
        
        # Aba de admissões para validação
        frame_admissoes = ttk.Frame(notebook, padding=10)
        notebook.add(frame_admissoes, text="✅ Validação de Admissões")
        
        lbl_admissoes = tk.Label(frame_admissoes, text="Admissões para Validação", 
                                font=('Segoe UI', 12, 'bold'), bg='white')
        lbl_admissoes.pack(pady=10)
        
        # Treeview para admissões pendentes
        tree_frame_admissoes = tk.Frame(frame_admissoes)
        tree_frame_admissoes.pack(fill='both', expand=True, pady=10)
        
        self.tree_admissoes_dp = ttk.Treeview(
            tree_frame_admissoes,
            columns=("Nome", "CPF", "Função", "Status"), 
            show="headings",
            height=15
        )
        
        self.tree_admissoes_dp.heading("Nome", text="Nome")
        self.tree_admissoes_dp.heading("CPF", text="CPF")
        self.tree_admissoes_dp.heading("Função", text="Função")
        self.tree_admissoes_dp.heading("Status", text="Status")
        
        tree_scroll_admissoes = ttk.Scrollbar(tree_frame_admissoes, orient='vertical', command=self.tree_admissoes_dp.yview)
        self.tree_admissoes_dp.configure(yscrollcommand=tree_scroll_admissoes.set)
        
        self.tree_admissoes_dp.pack(side='left', fill='both', expand=True)
        tree_scroll_admissoes.pack(side='right', fill='y')
        
        # Frame de botões para validação
        frame_botoes_admissoes = tk.Frame(frame_admissoes, bg='white')
        frame_botoes_admissoes.pack(pady=10)
        
        btn_validar = self.criar_botao(
            frame_botoes_admissoes,
            texto="✅ Validar Admissão",
            comando=self.validar_admissao,
            estilo='Sucesso.TButton'
        )
        btn_validar.pack(side='left', padx=5)
        
        btn_devolver = self.criar_botao(
            frame_botoes_admissoes,
            texto="↩️ Devolver ao RH",
            comando=self.devolver_rh,
            estilo='Alerta.TButton'
        )
        btn_devolver.pack(side='left', padx=5)
        
        # Nova aba para visualizar todos os cadastros
        frame_visualizar = ttk.Frame(notebook, padding=10)
        notebook.add(frame_visualizar, text="👁️ Visualizar Todos os Cadastros")
        
        lbl_visualizar = tk.Label(frame_visualizar, text="Lista Completa de Cadastros", 
                                 font=('Segoe UI', 12, 'bold'), bg='white')
        lbl_visualizar.pack(pady=10)
        
        # Treeview para mostrar todos os dados
        tree_frame_visualizar = tk.Frame(frame_visualizar)
        tree_frame_visualizar.pack(fill='both', expand=True, pady=10)
        
        self.tree_todos_cadastros = ttk.Treeview(
            tree_frame_visualizar,
            columns=("Tipo", "Nome", "CPF", "Status", "Detalhes"), 
            show="headings",
            height=15
        )
        
        self.tree_todos_cadastros.heading("Tipo", text="Tipo")
        self.tree_todos_cadastros.heading("Nome", text="Nome")
        self.tree_todos_cadastros.heading("CPF", text="CPF")
        self.tree_todos_cadastros.heading("Status", text="Status")
        self.tree_todos_cadastros.heading("Detalhes", text="Detalhes")
        
        # Configurar largura das colunas
        self.tree_todos_cadastros.column("Tipo", width=100)
        self.tree_todos_cadastros.column("Nome", width=150)
        self.tree_todos_cadastros.column("CPF", width=120)
        self.tree_todos_cadastros.column("Status", width=120)
        self.tree_todos_cadastros.column("Detalhes", width=200)
        
        tree_scroll_visualizar = ttk.Scrollbar(tree_frame_visualizar, orient='vertical', command=self.tree_todos_cadastros.yview)
        self.tree_todos_cadastros.configure(yscrollcommand=tree_scroll_visualizar.set)
        
        self.tree_todos_cadastros.pack(side='left', fill='both', expand=True)
        tree_scroll_visualizar.pack(side='right', fill='y')
        
        # Botões
        botoes_frame = tk.Frame(frame_visualizar, bg='white')
        botoes_frame.pack(pady=10)
        
        btn_carregar = self.criar_botao(
            botoes_frame,
            texto="🔄 Carregar Todos os Dados",
            comando=self.carregar_todos_cadastros,
            estilo='Info.TButton'
        )
        btn_carregar.pack(side='left', padx=5)
        
        btn_detalhes = self.criar_botao(
            botoes_frame,
            texto="🔍 Ver Detalhes Completos",
            comando=self.mostrar_detalhes_completos,
            estilo='Aviso.TButton'
        )
        btn_detalhes.pack(side='left', padx=5)
        
        notebook.pack(fill='both', expand=True, pady=10)
        
        self.carregar_admissoes_dp()
    
    def carregar_admissoes_dp(self):
        """Carrega admissões pendentes para o DP"""
        for item in self.tree_admissoes_dp.get_children():
            self.tree_admissoes_dp.delete(item)
        
        conn = sqlite3.connect('sistema_candidatos.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT f.id, c.nome, c.cpf, f.funcao, f.status 
            FROM funcionarios f 
            JOIN candidatos c ON f.candidato_id = c.id 
            WHERE f.status = 'Pendente DP' OR f.status = 'Pendente RH'
        ''')
        admissoes = cursor.fetchall()
        conn.close()
        
        for adm in admissoes:
            self.tree_admissoes_dp.insert("", "end", 
                                         values=(adm[1], adm[2], adm[3], adm[4]), 
                                         iid=adm[0])
    
    def carregar_todos_cadastros(self):
        """Carrega todos os cadastros do sistema"""
        for item in self.tree_todos_cadastros.get_children():
            self.tree_todos_cadastros.delete(item)
        
        conn = sqlite3.connect('sistema_candidatos.db')
        cursor = conn.cursor()
        
        # Carregar candidatos
        cursor.execute('SELECT id, nome, cpf, status FROM candidatos')
        candidatos = cursor.fetchall()
        
        for cand in candidatos:
            detalhes = f"Candidato - Data Cadastro: {cand[3]}"
            self.tree_todos_cadastros.insert("", "end", 
                                           values=("Candidato", cand[1], cand[2], cand[3], detalhes),
                                           iid=f"c_{cand[0]}")
        
        # Carregar funcionários
        cursor.execute('''
            SELECT f.id, c.nome, c.cpf, f.status, f.funcao, f.data_admissao 
            FROM funcionarios f 
            JOIN candidatos c ON f.candidato_id = c.id
        ''')
        funcionarios = cursor.fetchall()
        
        for func in funcionarios:
            detalhes = f"Funcionário - Função: {func[4]}, Admissão: {func[5]}"
            self.tree_todos_cadastros.insert("", "end", 
                                           values=("Funcionário", func[1], func[2], func[3], detalhes),
                                           iid=f"f_{func[0]}")
        
        conn.close()
    
    def mostrar_detalhes_completos(self):
        """Mostra todos os detalhes de um cadastro selecionado"""
        selecionado = self.tree_todos_cadastros.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um cadastro para ver os detalhes!")
            return
        
        item_id = selecionado[0]
        
        conn = sqlite3.connect('sistema_candidatos.db')
        cursor = conn.cursor()
        
        if item_id.startswith('c_'):  # É um candidato
            cand_id = item_id[2:]
            cursor.execute('SELECT * FROM candidatos WHERE id = ?', (cand_id,))
            candidato = cursor.fetchone()
            
            if candidato:
                detalhes = f"""
DADOS COMPLETOS DO CANDIDATO:

ID: {candidato[0]}
Nome: {candidato[1]}
Telefone: {candidato[2]}
CEP: {candidato[3]}
Rua: {candidato[4]}
Número: {candidato[5]}
CPF: {candidato[6]}
Estado Civil: {candidato[7]}
Escolaridade: {candidato[8]}
Data Nascimento: {candidato[9]}
Data Cadastro: {candidato[10]}
Status: {candidato[11]}
"""
                self.mostrar_popup_detalhes(detalhes, "Detalhes do Candidato")
        
        elif item_id.startswith('f_'):  # É um funcionário
            func_id = item_id[2:]
            cursor.execute('''
                SELECT c.*, f.* 
                FROM funcionarios f 
                JOIN candidatos c ON f.candidato_id = c.id 
                WHERE f.id = ?
            ''', (func_id,))
            funcionario = cursor.fetchone()
            
            if funcionario:
                detalhes = f"""
DADOS COMPLETOS DO FUNCIONÁRIO:

INFORMAÇÕES PESSOAIS:
Nome: {funcionario[1]}
Telefone: {funcionario[2]}
CEP: {funcionario[3]}
Rua: {funcionario[4]}
Número: {funcionario[5]}
CPF: {funcionario[6]}
Estado Civil: {funcionario[7]}
Escolaridade: {funcionario[8]}
Data Nascimento: {funcionario[9]}
Data Cadastro: {funcionario[10]}
Status: {funcionario[11]}

INFORMAÇÕES FUNCIONAIS:
Seção: {funcionario[14]}
Função: {funcionario[15]}
Horário: {funcionario[16]}
Salário: R$ {funcionario[17]:.2f}
Data Admissão: {funcionario[18]}
Tipo Funcionário: {funcionario[19]}
Tipo Recebimento: {funcionario[20]}
Status Admissão: {funcionario[21]}
Observações: {funcionario[22] or 'Nenhuma'}
"""
                self.mostrar_popup_detalhes(detalhes, "Detalhes do Funcionário")
        
        conn.close()
    
    def mostrar_popup_detalhes(self, detalhes, titulo):
        """Mostra um popup com os detalhes completos"""
        popup = tk.Toplevel(self.root)
        popup.title(titulo)
        popup.geometry("600x500")
        popup.configure(bg='white')
        
        # Frame com scrollbar
        frame = tk.Frame(popup, bg='white')
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        text_widget = tk.Text(frame, wrap="word", font=('Segoe UI', 10), bg='#f8f9fa')
        text_widget.insert("1.0", detalhes)
        text_widget.config(state="disabled")
        
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        btn_fechar = self.criar_botao(popup, text="Fechar", comando=popup.destroy, estilo='Primario.TButton')
        btn_fechar.pack(pady=10)
    
    def validar_admissao(self):
        """Valida uma admissão no DP"""
        selecionado = self.tree_admissoes_dp.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma admissão!")
            return
        
        funcionario_id = selecionado[0]
        
        conn = sqlite3.connect('sistema_candidatos.db')
        cursor = conn.cursor()
        
        # Atualizar status
        cursor.execute(
            'UPDATE funcionarios SET status = "Admitido" WHERE id = ?',
            (funcionario_id,)
        )
        
        # Pegar candidato_id
        cursor.execute('SELECT candidato_id FROM funcionarios WHERE id = ?', (funcionario_id,))
        candidato_id = cursor.fetchone()[0]
        
        # Atualizar status do candidato
        cursor.execute(
            'UPDATE candidatos SET status = "Funcionário" WHERE id = ?',
            (candidato_id,)
        )
        
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Sucesso", "Admissão validada com sucesso!")
        self.carregar_admissoes_dp()
    
    def devolver_rh(self):
        """Devolve uma admissão para o RH com observações"""
        selecionado = self.tree_admissoes_dp.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma admissão!")
            return
        
        funcionario_id = selecionado[0]
        
        # Janela para inserir observações
        popup = tk.Toplevel(self.root)
        popup.title("Observações para o RH")
        popup.geometry("400x300")
        popup.configure(bg='white')
        
        lbl_obs = tk.Label(popup, text="Descreva as inconsistências encontradas:", 
                          font=('Segoe UI', 10, 'bold'), bg='white')
        lbl_obs.pack(pady=10)
        
        text_observacoes = tk.Text(popup, height=10, width=50, font=('Segoe UI', 9))
        text_observacoes.pack(pady=10, padx=10, fill='both', expand=True)
        
        def confirmar_devolucao():
            observacoes = text_observacoes.get("1.0", "end-1c")
            if not observacoes.strip():
                messagebox.showerror("Erro", "Descreva as observações!")
                return
            
            conn = sqlite3.connect('sistema_candidatos.db')
            cursor = conn.cursor()
            
            # Atualizar status para "Rejeitado DP" e adicionar observações
            cursor.execute(
                'UPDATE funcionarios SET status = "Rejeitado DP", observacoes = ? WHERE id = ?',
                (observacoes, funcionario_id)
            )
            
            conn.commit()
            conn.close()
            
            popup.destroy()
            messagebox.showinfo("Sucesso", "Admissão devolvida ao RH para correção!")
            self.carregar_admissoes_dp()
        
        btn_confirmar = self.criar_botao(
            popup,
            texto="Devolver ao RH",
            comando=confirmar_devolucao,
            estilo='Alerta.TButton'
        )
        btn_confirmar.pack(pady=10)
    
    def tela_usuario_mestre(self):
        """Tela do usuário mestre para gerenciar usuários"""
        self.limpar_tela()
        
        container = tk.Frame(self.root, bg=self.cor_fundo, padx=20, pady=20)
        container.pack(fill='both', expand=True)
        
        lbl_titulo = tk.Label(container, text="👑 Usuário Mestre - Gerenciar Usuários", 
                             font=('Segoe UI', 18, 'bold'), bg=self.cor_fundo, fg=self.cor_primaria)
        lbl_titulo.pack(pady=10)
        
        # Formulário de novo usuário
        card_form = self.criar_card(container, "➕ Novo Usuário")
        
        campos = [
            ("Usuário:", "entry_novo_user"),
            ("Senha:", "entry_nova_senha"),
            ("Perfil:", "combo_perfil")
        ]
        
        self.widgets_usuario = {}
        
        for i, (label, nome_widget) in enumerate(campos):
            row_frame = tk.Frame(card_form, bg='white')
            row_frame.pack(fill='x', pady=8)
            
            lbl = tk.Label(row_frame, text=label, width=15, anchor='e', bg='white', font=('Segoe UI', 9))
            lbl.pack(side='left', padx=(0, 10))
            
            if nome_widget == "combo_perfil":
                combo = ttk.Combobox(row_frame, values=["RH", "DP", "Ambos"], state="readonly", width=20)
                combo.pack(side='left', padx=(0, 10))
                self.widgets_usuario[nome_widget] = combo
            else:
                show = "•" if "senha" in nome_widget else None
                entry = ttk.Entry(row_frame, width=20, show=show)
                entry.pack(side='left', padx=(0, 10))
                self.widgets_usuario[nome_widget] = entry
        
        btn_criar = self.criar_botao(
            card_form,
            texto="👤 Criar Usuário",
            comando=self.criar_usuario,
            estilo='Sucesso.TButton'
        )
        btn_criar.pack(pady=10)
        
        # Lista de usuários existentes
        card_usuarios = self.criar_card(container, "📋 Usuários Existentes")
        
        self.tree_usuarios = ttk.Treeview(
            card_usuarios,
            columns=("Usuário", "Perfil", "Status"), 
            show="headings",
            height=10
        )
        
        self.tree_usuarios.heading("Usuário", text="Usuário")
        self.tree_usuarios.heading("Perfil", text="Perfil")
        self.tree_usuarios.heading("Status", text="Status")
        
        self.tree_usuarios.pack(fill='both', expand=True, pady=10)
        
        btn_desativar = self.criar_botao(
            card_usuarios,
            texto="🔄 Ativar/Desativar Usuário",
            comando=self.toggle_usuario,
            estilo='Aviso.TButton'
        )
        btn_desativar.pack(pady=5)
        
        btn_voltar = self.criar_botao(
            container,
            texto="↩️ Voltar",
            comando=self.tela_inicial,
            estilo='Primario.TButton'
        )
        btn_voltar.pack(pady=10)
        
        self.carregar_usuarios()
    
    def criar_usuario(self):
        """Cria um novo usuário no sistema"""
        usuario = self.widgets_usuario['entry_novo_user'].get()
        senha = self.widgets_usuario['entry_nova_senha'].get()
        perfil = self.widgets_usuario['combo_perfil'].get()
        
        if not usuario or not senha or not perfil:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
        
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        
        try:
            conn = sqlite3.connect('sistema_candidatos.db')
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO usuarios (username, password, perfil) VALUES (?, ?, ?)',
                (usuario, senha_hash, perfil)
            )
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Sucesso", "Usuário criado com sucesso!")
            self.widgets_usuario['entry_novo_user'].delete(0, "end")
            self.widgets_usuario['entry_nova_senha'].delete(0, "end")
            self.widgets_usuario['combo_perfil'].set("")
            self.carregar_usuarios()
            
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Usuário já existe!")
    
    def carregar_usuarios(self):
        """Carrega a lista de usuários"""
        for item in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(item)
        
        conn = sqlite3.connect('sistema_candidatos.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, perfil, ativo FROM usuarios WHERE username != "admin"')
        usuarios = cursor.fetchall()
        conn.close()
        
        for usuario in usuarios:
            status = "✅ Ativo" if usuario[3] else "❌ Inativo"
            self.tree_usuarios.insert("", "end", 
                                     values=(usuario[1], usuario[2], status), 
                                     iid=usuario[0])
    
    def toggle_usuario(self):
        """Ativa/desativa um usuário"""
        selecionado = self.tree_usuarios.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um usuário!")
            return
        
        usuario_id = selecionado[0]
        
        conn = sqlite3.connect('sistema_candidatos.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT ativo FROM usuarios WHERE id = ?', (usuario_id,))
        ativo_atual = cursor.fetchone()[0]
        
        novo_status = 0 if ativo_atual else 1
        
        cursor.execute('UPDATE usuarios SET ativo = ? WHERE id = ?', (novo_status, usuario_id))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Sucesso", f"Usuário {'ativado' if novo_status else 'desativado'}!")
        self.carregar_usuarios()
    
    def limpar_tela(self):
        """Limpa todos os widgets da tela"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def executar(self):
        """Inicia a aplicação"""
        self.root.mainloop()

# Executar a aplicação
if __name__ == "__main__":
    app = SistemaCadastroCandidatos()
    app.executar()