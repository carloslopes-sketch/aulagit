import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import json
import os

class RestauranteApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🍣 Sistema Restaurante Japonês")
        self.root.geometry("1200x700")
        self.root.resizable(True, True)
        
        # Configurar estilo
        self.setup_styles()
        
        # Inicializar dados
        self.cardapio = self.carregar_cardapio()
        self.pedidos = self.carregar_pedidos()
        self.numero_pedido = 1000 + len(self.pedidos)
        
        # Configurar layout principal
        self.setup_ui()
        
    def setup_styles(self):
        """Configura estilos para a interface"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar cores
        self.bg_color = "#2b2b2b"
        self.fg_color = "#ffffff"
        self.accent_color = "#3498db"
        self.success_color = "#27ae60"
        self.warning_color = "#e74c3c"
        
        # Aplicar cores
        self.root.configure(bg=self.bg_color)
        
    def carregar_cardapio(self):
        """Carrega o cardápio padrão"""
        return {
            1: {"nome": "Sashimi de Salmão", "preco": 25.00, "categoria": "Sashimi"},
            2: {"nome": "Sashimi de Atum", "preco": 28.00, "categoria": "Sashimi"},
            3: {"nome": "Sashimi Misto", "preco": 35.00, "categoria": "Sashimi"},
            4: {"nome": "Sashimi de Peixe Branco", "preco": 22.00, "categoria": "Sashimi"},
            5: {"nome": "Sashimi de Polvo", "preco": 26.00, "categoria": "Sashimi"},
            6: {"nome": "Nigiri de Salmão", "preco": 8.00, "categoria": "Sushi"},
            7: {"nome": "Nigiri de Atum", "preco": 9.00, "categoria": "Sushi"},
            8: {"nome": "Nigiri de Camarão", "preco": 8.50, "categoria": "Sushi"},
            9: {"nome": "Nigiri de Polvo", "preco": 9.50, "categoria": "Sushi"},
            10: {"nome": "Nigiri de Ouriço", "preco": 15.00, "categoria": "Sushi"},
            11: {"nome": "California Roll", "preco": 22.00, "categoria": "Roll"},
            12: {"nome": "Philadelphia Roll", "preco": 24.00, "categoria": "Roll"},
            13: {"nome": "Spicy Tuna Roll", "preco": 26.00, "categoria": "Roll"},
            14: {"nome": "Dragon Roll", "preco": 32.00, "categoria": "Roll"},
            15: {"nome": "Rainbow Roll", "preco": 28.00, "categoria": "Roll"},
            16: {"nome": "Tempura Roll", "preco": 25.00, "categoria": "Roll"},
            17: {"nome": "Salmon Skin Roll", "preco": 20.00, "categoria": "Roll"},
            18: {"nome": "Spider Roll", "preco": 30.00, "categoria": "Roll"},
            19: {"nome": "Caterpillar Roll", "preco": 29.00, "categoria": "Roll"},
            20: {"nome": "Dynamite Roll", "preco": 27.00, "categoria": "Roll"},
            21: {"nome": "Temaki de Salmão", "preco": 18.00, "categoria": "Temaki"},
            22: {"nome": "Temaki de Atum", "preco": 19.00, "categoria": "Temaki"},
            23: {"nome": "Temaki Misto", "preco": 22.00, "categoria": "Temaki"},
            24: {"nome": "Temaki Vegetariano", "preco": 16.00, "categoria": "Temaki"},
            25: {"nome": "Temaki de Kani", "preco": 20.00, "categoria": "Temaki"},
            26: {"nome": "Tempurá de Camarão", "preco": 35.00, "categoria": "Prato Quente"},
            27: {"nome": "Yakitori", "preco": 28.00, "categoria": "Prato Quente"},
            28: {"nome": "Teppanyaki", "preco": 45.00, "categoria": "Prato Quente"},
            29: {"nome": "Lámen", "preco": 32.00, "categoria": "Prato Quente"},
            30: {"nome": "Udon", "preco": 30.00, "categoria": "Prato Quente"},
            31: {"nome": "Chá Verde", "preco": 8.00, "categoria": "Bebida"},
            32: {"nome": "Sake Quente", "preco": 25.00, "categoria": "Bebida"},
            33: {"nome": "Cerveja Japonesa", "preco": 18.00, "categoria": "Bebida"},
            34: {"nome": "Refrigerante", "preco": 7.00, "categoria": "Bebida"},
            35: {"nome": "Água Mineral", "preco": 5.00, "categoria": "Bebida"}
        }
    
    def carregar_pedidos(self):
        """Carrega pedidos do arquivo JSON"""
        try:
            if os.path.exists("pedidos.json"):
                with open("pedidos.json", "r", encoding="utf-8") as f:
                    return json.load(f)
        except:
            pass
        return {}
    
    def salvar_pedidos(self):
        """Salva pedidos no arquivo JSON"""
        try:
            with open("pedidos.json", "w", encoding="utf-8") as f:
                json.dump(self.pedidos, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar pedidos: {e}")
    
    def gerar_numero_pedido(self):
        """Gera um número único para o pedido"""
        self.numero_pedido += 1
        return self.numero_pedido
    
    def setup_ui(self):
        """Configura a interface do usuário"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Barra lateral com menu
        self.setup_sidebar(main_frame)
        
        # Área de conteúdo
        self.setup_content_area(main_frame)
        
    def setup_sidebar(self, parent):
        """Configura a barra lateral com menu"""
        sidebar = tk.Frame(parent, bg=self.bg_color, width=200, relief="raised", bd=2)
        sidebar.pack(side="left", fill="y", padx=(0, 10))
        sidebar.pack_propagate(False)
        
        # Título
        title_label = tk.Label(sidebar, text="🍣 SUSHI HOUSE", 
                             font=("Arial", 16, "bold"),
                             bg=self.bg_color, fg=self.fg_color)
        title_label.pack(pady=20)
        
        # Botões do menu
        menu_buttons = [
            ("📋 Ver Cardápio", self.mostrar_cardapio),
            ("➕ Novo Pedido", self.novo_pedido),
            ("📦 Pedidos Pendentes", self.mostrar_pedidos_pendentes),
            ("🍳 Comanda Cozinha", self.imprimir_comanda),
            ("✅ Confirmar Entrega", self.confirmar_entrega),
            ("🧾 Nota Fiscal", self.gerar_nota),
            ("📊 Relatório", self.mostrar_relatorio),
            ("🚪 Sair", self.sair)
        ]
        
        for text, command in menu_buttons:
            btn = tk.Button(sidebar, text=text, command=command,
                          font=("Arial", 12), bg=self.accent_color, 
                          fg="white", relief="raised", bd=2,
                          width=20, height=2)
            btn.pack(padx=10, pady=5)
    
    def setup_content_area(self, parent):
        """Configura a área de conteúdo principal"""
        self.content_frame = tk.Frame(parent, bg=self.bg_color)
        self.content_frame.pack(side="right", fill="both", expand=True)
        
        # Título da área de conteúdo
        self.content_title = tk.Label(self.content_frame, text="Bem-vindo ao Sistema",
                                    font=("Arial", 20, "bold"),
                                    bg=self.bg_color, fg=self.fg_color)
        self.content_title.pack(pady=20)
        
        # Área de texto para conteúdo
        text_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        text_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.content_text = tk.Text(text_frame, wrap="word", font=("Arial", 11),
                                  bg="#1a1a1a", fg="white", insertbackground="white")
        scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=self.content_text.yview)
        self.content_text.configure(yscrollcommand=scrollbar.set)
        
        self.content_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Frame para ações específicas
        self.action_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        self.action_frame.pack(fill="x", padx=20, pady=10)
        
    def clear_content(self):
        """Limpa a área de conteúdo"""
        self.content_text.delete("1.0", "end")
        for widget in self.action_frame.winfo_children():
            widget.destroy()
    
    def mostrar_cardapio(self):
        """Exibe o cardápio completo"""
        self.clear_content()
        self.content_title.configure(text="🍣 Cardápio Completo")
        
        texto = "=" * 60 + "\n"
        texto += "           🍣 MENU RESTAURANTE JAPONÊS 🍱\n"
        texto += "=" * 60 + "\n\n"
        
        # Agrupar por categoria
        categorias = {}
        for codigo, item in self.cardapio.items():
            categoria = item["categoria"]
            if categoria not in categorias:
                categorias[categoria] = []
            categorias[categoria].append((codigo, item))
        
        for categoria, itens in categorias.items():
            texto += f"\n{categoria.upper()}:\n"
            texto += "-" * 40 + "\n"
            for codigo, item in itens:
                texto += f"{codigo:2d}. {item['nome']:<30} R$ {item['preco']:6.2f}\n"
        
        self.content_text.insert("1.0", texto)
    
    def novo_pedido(self):
        """Interface para criar novo pedido"""
        self.clear_content()
        self.content_title.configure(text="➕ Novo Pedido")
        
        # Frame para dados da mesa
        mesa_frame = tk.Frame(self.action_frame, bg=self.bg_color)
        mesa_frame.pack(fill="x", pady=10)
        
        tk.Label(mesa_frame, text="Número da Mesa:", 
                font=("Arial", 12), bg=self.bg_color, fg=self.fg_color).pack(side="left", padx=10)
        
        self.mesa_var = tk.StringVar()
        mesa_entry = tk.Entry(mesa_frame, textvariable=self.mesa_var, width=10, font=("Arial", 12))
        mesa_entry.pack(side="left", padx=10)
        
        # Frame principal para itens
        main_items_frame = tk.Frame(self.action_frame, bg=self.bg_color)
        main_items_frame.pack(fill="both", expand=True, pady=10)
        
        # Frame para cardápio e pedido
        items_frame = tk.Frame(main_items_frame, bg=self.bg_color)
        items_frame.pack(fill="both", expand=True)
        
        # Frame do cardápio
        cardapio_frame = tk.Frame(items_frame, bg=self.bg_color)
        cardapio_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        tk.Label(cardapio_frame, text="Cardápio:", 
                font=("Arial", 12, "bold"), bg=self.bg_color, fg=self.fg_color).pack(anchor="w")
        
        # Treeview para cardápio
        cardapio_tree_frame = tk.Frame(cardapio_frame, bg=self.bg_color)
        cardapio_tree_frame.pack(fill="both", expand=True, pady=5)
        
        self.cardapio_tree = ttk.Treeview(cardapio_tree_frame, columns=("Código", "Item", "Preço", "Categoria"), 
                                        show="headings", height=15)
        
        for col in ("Código", "Item", "Preço", "Categoria"):
            self.cardapio_tree.heading(col, text=col)
        
        self.cardapio_tree.column("Código", width=60)
        self.cardapio_tree.column("Item", width=200)
        self.cardapio_tree.column("Preço", width=80)
        self.cardapio_tree.column("Categoria", width=100)
        
        # Preencher treeview
        for codigo, item in self.cardapio.items():
            self.cardapio_tree.insert("", "end", values=(
                codigo, item["nome"], f"R$ {item['preco']:.2f}", item["categoria"]
            ))
        
        cardapio_scroll = ttk.Scrollbar(cardapio_tree_frame, orient="vertical", command=self.cardapio_tree.yview)
        self.cardapio_tree.configure(yscrollcommand=cardapio_scroll.set)
        
        self.cardapio_tree.pack(side="left", fill="both", expand=True)
        cardapio_scroll.pack(side="right", fill="y")
        
        # Frame do pedido
        pedido_frame = tk.Frame(items_frame, bg=self.bg_color)
        pedido_frame.pack(side="right", fill="both", expand=True, padx=5)
        
        tk.Label(pedido_frame, text="Itens do Pedido:", 
                font=("Arial", 12, "bold"), bg=self.bg_color, fg=self.fg_color).pack(anchor="w")
        
        # Treeview para pedido
        pedido_tree_frame = tk.Frame(pedido_frame, bg=self.bg_color)
        pedido_tree_frame.pack(fill="both", expand=True, pady=5)
        
        self.pedido_tree = ttk.Treeview(pedido_tree_frame, columns=("Item", "Quantidade", "Subtotal"), 
                                      show="headings", height=15)
        
        for col in ("Item", "Quantidade", "Subtotal"):
            self.pedido_tree.heading(col, text=col)
        
        self.pedido_tree.column("Item", width=200)
        self.pedido_tree.column("Quantidade", width=80)
        self.pedido_tree.column("Subtotal", width=100)
        
        pedido_scroll = ttk.Scrollbar(pedido_tree_frame, orient="vertical", command=self.pedido_tree.yview)
        self.pedido_tree.configure(yscrollcommand=pedido_scroll.set)
        
        self.pedido_tree.pack(side="left", fill="both", expand=True)
        pedido_scroll.pack(side="right", fill="y")
        
        # Controles
        control_frame = tk.Frame(main_items_frame, bg=self.bg_color)
        control_frame.pack(fill="x", pady=10)
        
        tk.Label(control_frame, text="Quantidade:", 
                bg=self.bg_color, fg=self.fg_color).pack(side="left", padx=10)
        
        self.quantidade_var = tk.StringVar(value="1")
        quantidade_entry = tk.Entry(control_frame, textvariable=self.quantidade_var, width=10)
        quantidade_entry.pack(side="left", padx=10)
        
        add_btn = tk.Button(control_frame, text="Adicionar Item", 
                           command=self.adicionar_item_pedido, bg=self.accent_color, fg="white")
        add_btn.pack(side="left", padx=10)
        
        # Botões de ação
        btn_frame = tk.Frame(main_items_frame, bg=self.bg_color)
        btn_frame.pack(fill="x", pady=10)
        
        finalizar_btn = tk.Button(btn_frame, text="Finalizar Pedido", 
                                 command=self.finalizar_pedido, 
                                 bg=self.success_color, fg="white", font=("Arial", 12))
        finalizar_btn.pack(side="left", padx=10)
        
        limpar_btn = tk.Button(btn_frame, text="Limpar Pedido", 
                              command=self.limpar_pedido_atual,
                              bg=self.warning_color, fg="white", font=("Arial", 12))
        limpar_btn.pack(side="left", padx=10)
        
        # Dicionário para armazenar pedido atual
        self.pedido_atual = {}
    
    def adicionar_item_pedido(self):
        """Adiciona item ao pedido atual"""
        try:
            selection = self.cardapio_tree.selection()
            if not selection:
                messagebox.showwarning("Aviso", "Selecione um item do cardápio!")
                return
            
            item_id = selection[0]
            values = self.cardapio_tree.item(item_id, "values")
            codigo = int(values[0])
            quantidade = int(self.quantidade_var.get())
            
            if quantidade <= 0:
                messagebox.showwarning("Aviso", "Quantidade deve ser maior que zero!")
                return
            
            # Adicionar ao pedido atual
            if codigo in self.pedido_atual:
                self.pedido_atual[codigo] += quantidade
            else:
                self.pedido_atual[codigo] = quantidade
            
            # Atualizar treeview do pedido
            self.atualizar_pedido_tree()
            
            messagebox.showinfo("Sucesso", f"{quantidade}x {values[1]} adicionado ao pedido!")
            
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar item: {e}")
    
    def atualizar_pedido_tree(self):
        """Atualiza a treeview do pedido atual"""
        # Limpar treeview
        for item in self.pedido_tree.get_children():
            self.pedido_tree.delete(item)
        
        # Preencher com itens do pedido
        total_geral = 0
        for codigo, quantidade in self.pedido_atual.items():
            item = self.cardapio[codigo]
            subtotal = item["preco"] * quantidade
            total_geral += subtotal
            self.pedido_tree.insert("", "end", values=(
                item["nome"], quantidade, f"R$ {subtotal:.2f}"
            ))
        
        # Adicionar linha do total
        if self.pedido_atual:
            self.pedido_tree.insert("", "end", values=(
                "TOTAL", "", f"R$ {total_geral:.2f}"
            ))
    
    def limpar_pedido_atual(self):
        """Limpa o pedido atual"""
        self.pedido_atual = {}
        self.atualizar_pedido_tree()
        messagebox.showinfo("Sucesso", "Pedido limpo!")
    
    def finalizar_pedido(self):
        """Finaliza o pedido atual"""
        try:
            if not self.pedido_atual:
                messagebox.showwarning("Aviso", "Adicione itens ao pedido antes de finalizar!")
                return
            
            mesa = self.mesa_var.get().strip()
            if not mesa or not mesa.isdigit():
                messagebox.showwarning("Aviso", "Informe um número de mesa válido!")
                return
            
            mesa = int(mesa)
            if mesa <= 0:
                messagebox.showwarning("Aviso", "Número da mesa deve ser maior que zero!")
                return
            
            # Gerar número do pedido
            numero_pedido = self.gerar_numero_pedido()
            
            # Salvar pedido
            self.pedidos[numero_pedido] = {
                "mesa": mesa,
                "itens": self.pedido_atual.copy(),
                "status": "pendente",
                "data_hora": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }
            
            self.salvar_pedidos()
            
            messagebox.showinfo("Sucesso", 
                              f"Pedido #{numero_pedido} finalizado com sucesso!\n"
                              f"Mesa: {mesa}\n"
                              f"Status: Pendente")
            
            # Limpar para novo pedido
            self.limpar_pedido_atual()
            self.mesa_var.set("")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao finalizar pedido: {e}")
    
    def mostrar_pedidos_pendentes(self):
        """Exibe pedidos pendentes"""
        self.clear_content()
        self.content_title.configure(text="📦 Pedidos Pendentes")
        
        pedidos_pendentes = {num: ped for num, ped in self.pedidos.items() 
                           if ped["status"] == "pendente"}
        
        if not pedidos_pendentes:
            self.content_text.insert("1.0", "📭 Nenhum pedido pendente!")
            return
        
        texto = f"Total de pedidos pendentes: {len(pedidos_pendentes)}\n\n"
        
        for numero, pedido in pedidos_pendentes.items():
            texto += f"📋 Pedido #{numero} - Mesa {pedido['mesa']}\n"
            texto += f"🕒 Horário: {pedido['data_hora']}\n"
            texto += "Itens:\n"
            
            for codigo, quantidade in pedido["itens"].items():
                item = self.cardapio[codigo]
                texto += f"  [{quantidade:2d}x] {item['nome']}\n"
            
            texto += "-" * 40 + "\n\n"
        
        self.content_text.insert("1.0", texto)
    
    def imprimir_comanda(self):
        """Interface para imprimir comanda da cozinha"""
        self.clear_content()
        self.content_title.configure(text="🍳 Comanda da Cozinha")
        
        pedidos_pendentes = {num: ped for num, ped in self.pedidos.items() 
                           if ped["status"] == "pendente"}
        
        if not pedidos_pendentes:
            self.content_text.insert("1.0", "📭 Nenhum pedido pendente para imprimir!")
            return
        
        # Lista de pedidos pendentes
        tk.Label(self.action_frame, text="Selecione o pedido para imprimir:",
                font=("Arial", 12), bg=self.bg_color, fg=self.fg_color).pack(anchor="w", pady=10)
        
        self.pedido_var = tk.StringVar()
        pedidos_list = [f"#{num} - Mesa {ped['mesa']}" for num, ped in pedidos_pendentes.items()]
        self.pedido_combo = ttk.Combobox(self.action_frame, textvariable=self.pedido_var,
                                       values=pedidos_list, state="readonly", width=30)
        self.pedido_combo.pack(pady=10)
        
        imprimir_btn = tk.Button(self.action_frame, text="🖨️ Imprimir Comanda",
                               command=self.gerar_comanda, bg=self.accent_color, fg="white")
        imprimir_btn.pack(pady=10)
    
    def gerar_comanda(self):
        """Gera a comanda para impressão"""
        try:
            selecao = self.pedido_combo.get()
            if not selecao:
                messagebox.showwarning("Aviso", "Selecione um pedido!")
                return
            
            numero_pedido = int(selecao.split("#")[1].split(" ")[0])
            pedido = self.pedidos[numero_pedido]
            
            self.clear_content()
            self.content_title.configure(text=f"🍳 Comanda - Pedido #{numero_pedido}")
            
            texto = "=" * 60 + "\n"
            texto += "              🍣 COMANDA DA COZINHA 🍱\n"
            texto += "=" * 60 + "\n"
            texto += f"Pedido: #{numero_pedido}\n"
            texto += f"Mesa: {pedido['mesa']}\n"
            texto += f"Horário: {pedido['data_hora']}\n"
            texto += f"Status: ⌛ Pendente\n"
            texto += "-" * 60 + "\n\n"
            
            # Agrupar por categoria
            pedido_por_categoria = {}
            for codigo, quantidade in pedido["itens"].items():
                categoria = self.cardapio[codigo]["categoria"]
                if categoria not in pedido_por_categoria:
                    pedido_por_categoria[categoria] = []
                pedido_por_categoria[categoria].append((codigo, quantidade))
            
            for categoria, itens in pedido_por_categoria.items():
                texto += f"{categoria.upper()}:\n"
                for codigo, quantidade in itens:
                    item = self.cardapio[codigo]
                    texto += f"  [{quantidade:2d}x] {item['nome']}\n"
                texto += "\n"
            
            texto += "=" * 60 + "\n"
            texto += "⚠️  PREPARAR COM CARINHO E ATENÇÃO!\n"
            texto += "=" * 60 + "\n"
            texto += "\n📝 Status: ⌛ Pendente (aguardando confirmação de entrega)"
            
            self.content_text.insert("1.0", texto)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar comanda: {e}")
    
    def confirmar_entrega(self):
        """Interface para confirmar entrega"""
        self.clear_content()
        self.content_title.configure(text="✅ Confirmar Entrega")
        
        pedidos_pendentes = {num: ped for num, ped in self.pedidos.items() 
                           if ped["status"] == "pendente"}
        
        if not pedidos_pendentes:
            self.content_text.insert("1.0", "📭 Nenhum pedido pendente para confirmar entrega!")
            return
        
        # Lista de pedidos pendentes
        tk.Label(self.action_frame, text="Selecione o pedido entregue:",
                font=("Arial", 12), bg=self.bg_color, fg=self.fg_color).pack(anchor="w", pady=10)
        
        self.entrega_var = tk.StringVar()
        entregas_list = [f"#{num} - Mesa {ped['mesa']}" for num, ped in pedidos_pendentes.items()]
        self.entrega_combo = ttk.Combobox(self.action_frame, textvariable=self.entrega_var,
                                        values=entregas_list, state="readonly", width=30)
        self.entrega_combo.pack(pady=10)
        
        confirmar_btn = tk.Button(self.action_frame, text="✅ Confirmar Entrega",
                                command=self.executar_confirmar_entrega,
                                bg=self.success_color, fg="white", font=("Arial", 12))
        confirmar_btn.pack(pady=10)
    
    def executar_confirmar_entrega(self):
        """Executa a confirmação de entrega"""
        try:
            selecao = self.entrega_combo.get()
            if not selecao:
                messagebox.showwarning("Aviso", "Selecione um pedido!")
                return
            
            numero_pedido = int(selecao.split("#")[1].split(" ")[0])
            
            # Confirmar entrega
            self.pedidos[numero_pedido]["status"] = "entregue"
            self.pedidos[numero_pedido]["hora_entrega"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            
            self.salvar_pedidos()
            
            messagebox.showinfo("Sucesso", 
                              f"✅ PEDIDO #{numero_pedido} CONFIRMADO COMO ENTREGUE!\n"
                              f"📍 Mesa: {self.pedidos[numero_pedido]['mesa']}\n"
                              f"🕒 Horário da entrega: {self.pedidos[numero_pedido]['hora_entrega']}")
            
            # Atualizar interface
            self.confirmar_entrega()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao confirmar entrega: {e}")
    
    def gerar_nota(self):
        """Interface para gerar nota fiscal"""
        self.clear_content()
        self.content_title.configure(text="🧾 Nota Fiscal")
        
        if not self.pedidos:
            self.content_text.insert("1.0", "📭 Nenhum pedido cadastrado!")
            return
        
        # Lista de todos os pedidos
        tk.Label(self.action_frame, text="Selecione o pedido:",
                font=("Arial", 12), bg=self.bg_color, fg=self.fg_color).pack(anchor="w", pady=10)
        
        self.nota_var = tk.StringVar()
        notas_list = [f"#{num} - Mesa {ped['mesa']} ({ped['status']})" for num, ped in self.pedidos.items()]
        self.nota_combo = ttk.Combobox(self.action_frame, textvariable=self.nota_var,
                                     values=notas_list, state="readonly", width=30)
        self.nota_combo.pack(pady=10)
        
        gerar_btn = tk.Button(self.action_frame, text="🧾 Gerar Nota",
                            command=self.executar_gerar_nota, bg=self.accent_color, fg="white")
        gerar_btn.pack(pady=10)
    
    def executar_gerar_nota(self):
        """Executa a geração da nota fiscal"""
        try:
            selecao = self.nota_combo.get()
            if not selecao:
                messagebox.showwarning("Aviso", "Selecione um pedido!")
                return
            
            numero_pedido = int(selecao.split("#")[1].split(" ")[0])
            pedido = self.pedidos[numero_pedido]
            
            self.clear_content()
            self.content_title.configure(text=f"🧾 Nota Fiscal - Pedido #{numero_pedido}")
            
            texto = "=" * 60 + "\n"
            texto += "              🍣 NOTA FISCAL 🍱\n"
            texto += "=" * 60 + "\n"
            texto += f"Pedido: #{numero_pedido}\n"
            texto += f"Mesa: {pedido['mesa']}\n"
            texto += f"Horário: {pedido['data_hora']}\n"
            texto += f"Status: {pedido['status'].upper()}\n"
            
            if "hora_entrega" in pedido:
                texto += f"Entrega: {pedido['hora_entrega']}\n"
            
            texto += "-" * 60 + "\n"
            
            total = 0
            for codigo, quantidade in pedido["itens"].items():
                item = self.cardapio[codigo]
                subtotal = item["preco"] * quantidade
                total += subtotal
                texto += f"{quantidade:2d}x {item['nome']:<30} R$ {subtotal:6.2f}\n"
            
            texto += "-" * 60 + "\n"
            texto += f"{'TOTAL:':<35} R$ {total:6.2f}\n"
            texto += "=" * 60 + "\n"
            texto += "🍣 Obrigado pela preferência! 🍱\n"
            texto += "=" * 60
            
            self.content_text.insert("1.0", texto)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar nota: {e}")
    
    def mostrar_relatorio(self):
        """Exibe relatório de pedidos"""
        self.clear_content()
        self.content_title.configure(text="📊 Relatório de Pedidos")
        
        if not self.pedidos:
            self.content_text.insert("1.0", "📭 Nenhum pedido foi realizado!")
            return
        
        pedidos_pendentes = {num: ped for num, ped in self.pedidos.items() 
                           if ped["status"] == "pendente"}
        pedidos_entregues = {num: ped for num, ped in self.pedidos.items() 
                           if ped["status"] == "entregue"}
        
        texto = "=" * 60 + "\n"
        texto += "              📊 RELATÓRIO DE PEDIDOS\n"
        texto += "=" * 60 + "\n\n"
        texto += "📋 RESUMO:\n"
        texto += f"Pedidos Pendentes: {len(pedidos_pendentes)}\n"
        texto += f"Pedidos Entregues: {len(pedidos_entregues)}\n"
        texto += f"Total de Pedidos: {len(self.pedidos)}\n\n"
        
        if pedidos_pendentes:
            texto += "⌛ PEDIDOS PENDENTES:\n"
            for numero, pedido in pedidos_pendentes.items():
                texto += f"  #{numero} - Mesa {pedido['mesa']} - {pedido['data_hora']}\n"
            texto += "\n"
        
        if pedidos_entregues:
            texto += "✅ PEDIDOS ENTREGUES:\n"
            for numero, pedido in pedidos_entregues.items():
                texto += f"  #{numero} - Mesa {pedido['mesa']} - Entregue: {pedido['hora_entrega']}\n"
        
        self.content_text.insert("1.0", texto)
    
    def sair(self):
        """Fecha a aplicação"""
        if messagebox.askokcancel("Sair", "Deseja realmente sair do sistema?"):
            self.root.destroy()

    def run(self):
        """Executa a aplicação"""
        self.root.mainloop()

if __name__ == "__main__":
    app = RestauranteApp()
    app.run()