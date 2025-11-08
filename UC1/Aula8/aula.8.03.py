class MenuJapones:
    def init(self): 
        self.cardapio = { # Sashimis (1-5) 
            1: {"nome": "Sashimi de Salmão", "preco": 25.00, "categoria": "Sashimi"}, 
            2: {"nome": "Sashimi de Atum", "preco": 28.00, "categoria": "Sashimi"}, 
            3: {"nome": "Sashimi Misto", "preco": 35.00, "categoria": "Sashimi"}, 
            4: {"nome": "Sashimi de Peixe Branco", "preco": 22.00, "categoria": "Sashimi"}, 
            5: {"nome": "Sashimi de Polvo", "preco": 26.00, "categoria": "Sashimi"},

            # Sushis (6-10)
            6: {"nome": "Nigiri de Salmão", "preco": 8.00, "categoria": "Sushi"},
            7: {"nome": "Nigiri de Atum", "preco": 9.00, "categoria": "Sushi"},
            8: {"nome": "Nigiri de Camarão", "preco": 8.50, "categoria": "Sushi"},
            9: {"nome": "Nigiri de Polvo", "preco": 9.50, "categoria": "Sushi"},
            10: {"nome": "Nigiri de Ouriço", "preco": 15.00, "categoria": "Sushi"},
            
            # Rolls (11-20)
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
            
            # Temakis (21-25)
            21: {"nome": "Temaki de Salmão", "preco": 18.00, "categoria": "Temaki"},
            22: {"nome": "Temaki de Atum", "preco": 19.00, "categoria": "Temaki"},
            23: {"nome": "Temaki Misto", "preco": 22.00, "categoria": "Temaki"},
            24: {"nome": "Temaki Vegetariano", "preco": 16.00, "categoria": "Temaki"},
            25: {"nome": "Temaki de Kani", "preco": 20.00, "categoria": "Temaki"},
            
            # Pratos Quentes (26-30)
            26: {"nome": "Tempurá de Camarão", "preco": 35.00, "categoria": "Prato Quente"},
            27: {"nome": "Yakitori", "preco": 28.00, "categoria": "Prato Quente"},
            28: {"nome": "Teppanyaki", "preco": 45.00, "categoria": "Prato Quente"},
            29: {"nome": "Lámen", "preco": 32.00, "categoria": "Prato Quente"},
            30: {"nome": "Udon", "preco": 30.00, "categoria": "Prato Quente"},
            
            # Bebidas (31-35)
            31: {"nome": "Chá Verde", "preco": 8.00, "categoria": "Bebida"},
            32: {"nome": "Sake Quente", "preco": 25.00, "categoria": "Bebida"},
            33: {"nome": "Cerveja Japonesa", "preco": 18.00, "categoria": "Bebida"},
            34: {"nome": "Refrigerante", "preco": 7.00, "categoria": "Bebida"},
            35: {"nome": "Água Mineral", "preco": 5.00, "categoria": "Bebida"}
        }
        
        self.pedido = {}

    def exibir_menu(self):
        """Exibe o menu completo organizado por categorias"""
        print("=" * 60)
        print("           🍣 MENU RESTAURANTE JAPONÊS 🍱")
        print("=" * 60)
        
        categorias = {}
        for codigo, item in self.cardapio.items():
            categoria = item["categoria"]
            if categoria not in categorias:
                categorias[categoria] = []
            categorias[categoria].append((codigo, item))
        
        for categoria, itens in categorias.items():
            print(f"\n{categoria.upper()}:")
            print("-" * 40)
            for codigo, item in itens:
                print(f"{codigo:2d}. {item['nome']:<30} R$ {item['preco']:6.2f}")

    def fazer_pedido(self):
        """Permite que o cliente faça seu pedido"""
        print("\n" + "=" * 60)
        print("              🍣 FAZER PEDIDO 🍱")
        print("=" * 60)
        
        while True:
            try:
                self.exibir_menu()
                print("\nDigite o código do item que deseja pedir (0 para finalizar):")
                codigo = int(input("Código: "))
                
                if codigo == 0:
                    break
                
                if codigo not in self.cardapio:
                    print("❌ Código inválido! Tente novamente.")
                    continue
                
                quantidade = int(input(f"Quantidade de '{self.cardapio[codigo]['nome']}': "))
                
                if quantidade <= 0:
                    print("❌ Quantidade deve ser maior que zero!")
                    continue
                
                # Adiciona ao pedido
                if codigo in self.pedido:
                    self.pedido[codigo] += quantidade
                else:
                    self.pedido[codigo] = quantidade
                
                print(f"✅ {quantidade}x {self.cardapio[codigo]['nome']} adicionado ao pedido!")
                
            except ValueError:
                print("❌ Por favor, digite um número válido!")

def calcular_total(self):
    """Calcula o total do pedido"""
    total = 0
    for codigo, quantidade in self.pedido.items():
        total += self.cardapio[codigo]["preco"] * quantidade
    return total

def imprimir_comanda_cozinha(self):
    """Imprime a comanda para a cozinha"""
    if not self.pedido:
        print("Nenhum pedido foi feito!")
        return
    
    print("\n" + "=" * 60)
    print("              🍣 COMANDA DA COZINHA 🍱")
    print("=" * 60)
    print(f"Pedido: #{hash(str(self.pedido)) % 10000:04d}")
    print("-" * 60)
    
    # Agrupa por categoria
    pedido_por_categoria = {}
    for codigo, quantidade in self.pedido.items():
        categoria = self.cardapio[codigo]["categoria"]
        if categoria not in pedido_por_categoria:
            pedido_por_categoria[categoria] = []
        pedido_por_categoria[categoria].append((codigo, quantidade))
    
    for categoria, itens in pedido_por_categoria.items():
        print(f"\n{categoria.upper()}:")
        for codigo, quantidade in itens:
            item = self.cardapio[codigo]
            print(f"  [{quantidade:2d}x] {item['nome']}")
    
    print("\n" + "=" * 60)
    print("⚠️  PREPARAR COM CARINHO E ATENÇÃO!")
    print("=" * 60)

def imprimir_nota_cliente(self):
    """Imprime a nota fiscal para o cliente"""
    if not self.pedido:
        print("Nenhum pedido foi feito!")
        return
    
    print("\n" + "=" * 60)
    print("              🍣 NOTA FISCAL 🍱")
    print("=" * 60)
    print(f"Pedido: #{hash(str(self.pedido)) % 10000:04d}")
    print("-" * 60)
    
    total = 0
    for codigo, quantidade in self.pedido.items():
        item = self.cardapio[codigo]
        subtotal = item["preco"] * quantidade
        total += subtotal
        print(f"{quantidade:2d}x {item['nome']:<30} R$ {subtotal:6.2f}")
    
    print("-" * 60)
    print(f"{'TOTAL:':<35} R$ {total:6.2f}")
    print("=" * 60)
    print("🍣 Obrigado pela preferência! 🍱")
    print("=" * 60)
def main(): restaurante = MenuJapones()

while True:
    print("\n" + "=" * 60)
    print("        🍣 RESTAURANTE JAPONÊS - SISTEMA 🍱")
    print("=" * 60)
    print("1. Ver Menu Completo")
    print("2. Fazer Pedido")
    print("3. Imprimir Comanda para Cozinha")
    print("4. Imprimir Nota Fiscal")
    print("5. Sair")
    print("-" * 60)
    
    try:
        opcao = int(input("Escolha uma opção: "))
        
        if opcao == 1:
            restaurante.exibir_menu()
            input("\nPressione Enter para continuar...")
        
        elif opcao == 2:
            restaurante.fazer_pedido()
        
        elif opcao == 3:
            restaurante.imprimir_comanda_cozinha()
            input("\nPressione Enter para continuar...")
        
        elif opcao == 4:
            restaurante.imprimir_nota_cliente()
            input("\nPressione Enter para continuar...")
        
        elif opcao == 5:
            print("🍣 Obrigado por usar nosso sistema! 🍱")
            break
        
        else:
            print("❌ Opção inválida! Tente novamente.")
    
    except ValueError:
        print("❌ Por favor, digite um número válido!")
if name == "main": main()