import random
import datetime

class MenuJapones:
    def __init__(self):
        self.cardapio = {
            # Sashimis (1-5)
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
        
        self.pedidos = {}  # Dicionário para armazenar todos os pedidos
        self.numero_pedido = 1000  # Número inicial do pedido
    
    def gerar_numero_pedido(self):
        """Gera um número único para o pedido"""
        self.numero_pedido += 1
        return self.numero_pedido
    
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
        
        # Solicitar número da mesa
        while True:
            try:
                mesa = int(input("Número da mesa: "))
                if mesa <= 0:
                    print("❌ Número da mesa deve ser maior que zero!")
                    continue
                break
            except ValueError:
                print("❌ Por favor, digite um número válido para a mesa!")
        
        # Gerar número do pedido
        numero_pedido = self.gerar_numero_pedido()
        pedido_atual = {
            "mesa": mesa,
            "itens": {},
            "status": "pendente",  # pendente, entregue
            "data_hora": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        
        print(f"\n📋 Pedido #{numero_pedido} - Mesa {mesa}")
        print("-" * 40)
        
        while True:
            try:
                self.exibir_menu()
                print(f"\nPedido #{numero_pedido} - Mesa {mesa}")
                print("Digite o código do item que deseja pedir (0 para finalizar):")
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
                
                # Adiciona ao pedido atual
                if codigo in pedido_atual["itens"]:
                    pedido_atual["itens"][codigo] += quantidade
                else:
                    pedido_atual["itens"][codigo] = quantidade
                
                print(f"✅ {quantidade}x {self.cardapio[codigo]['nome']} adicionado ao pedido!")
                
            except ValueError:
                print("❌ Por favor, digite um número válido!")
        
        # Salvar pedido apenas se houver itens
        if pedido_atual["itens"]:
            self.pedidos[numero_pedido] = pedido_atual
            print(f"\n🎉 Pedido #{numero_pedido} finalizado com sucesso!")
            print(f"📍 Mesa: {mesa}")
            print(f"🕒 Horário: {pedido_atual['data_hora']}")
            print("Status: ⌛ Pendente")
        else:
            print("❌ Nenhum item foi adicionado ao pedido!")
    
    def listar_pedidos_pendentes(self):
        """Lista todos os pedidos pendentes"""
        pedidos_pendentes = {num: ped for num, ped in self.pedidos.items() 
                           if ped["status"] == "pendente"}
        
        if not pedidos_pendentes:
            print("📭 Nenhum pedido pendente!")
            return None
        
        print("\n" + "=" * 60)
        print("              📋 PEDIDOS PENDENTES")
        print("=" * 60)
        
        for numero, pedido in pedidos_pendentes.items():
            print(f"\nPedido #{numero} - Mesa {pedido['mesa']}")
            print(f"Horário: {pedido['data_hora']}")
            print("Itens:")
            for codigo, quantidade in pedido["itens"].items():
                item = self.cardapio[codigo]
                print(f"  [{quantidade:2d}x] {item['nome']}")
            print("-" * 40)
        
        return pedidos_pendentes
    
    def confirmar_entrega(self):
        """Confirma que o pedido foi entregue ao cliente"""
        pedidos_pendentes = self.listar_pedidos_pendentes()
        
        if not pedidos_pendentes:
            return
        
        try:
            numero_pedido = int(input("\nDigite o número do pedido a ser marcado como entregue: "))
            
            if numero_pedido not in self.pedidos:
                print("❌ Pedido não encontrado!")
                return
            
            if self.pedidos[numero_pedido]["status"] == "entregue":
                print("❌ Este pedido já foi entregue!")
                return
            
            # Confirmar entrega
            self.pedidos[numero_pedido]["status"] = "entregue"
            self.pedidos[numero_pedido]["hora_entrega"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            
            print(f"\n✅ PEDIDO #{numero_pedido} CONFIRMADO COMO ENTREGUE!")
            print(f"📍 Mesa: {self.pedidos[numero_pedido]['mesa']}")
            print(f"🕒 Horário da entrega: {self.pedidos[numero_pedido]['hora_entrega']}")
            
        except ValueError:
            print("❌ Por favor, digite um número válido!")
    
    def imprimir_comanda_cozinha(self):
        """Imprime a comanda para a cozinha - NÃO ALTERA STATUS"""
        pedidos_pendentes = self.listar_pedidos_pendentes()
        
        if not pedidos_pendentes:
            return
        
        try:
            numero_pedido = int(input("\nDigite o número do pedido para imprimir comanda: "))
            
            if numero_pedido not in self.pedidos:
                print("❌ Pedido não encontrado!")
                return
            
            pedido = self.pedidos[numero_pedido]
            
            # Verificar se o pedido está pendente
            if pedido["status"] != "pendente":
                print("❌ Este pedido não está mais pendente!")
                return
            
            print("\n" + "=" * 60)
            print("              🍣 COMANDA DA COZINHA 🍱")
            print("=" * 60)
            print(f"Pedido: #{numero_pedido}")
            print(f"Mesa: {pedido['mesa']}")
            print(f"Horário: {pedido['data_hora']}")
            print(f"Status: ⌛ Pendente")
            print("-" * 60)
            
            # Agrupa por categoria
            pedido_por_categoria = {}
            for codigo, quantidade in pedido["itens"].items():
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
            
            # NÃO altera o status - permanece como "pendente"
            print("\n📝 Status mantido como: ⌛ Pendente (aguardando confirmação de entrega)")
        
        except ValueError:
            print("❌ Por favor, digite um número válido!")
    
    def imprimir_nota_cliente(self):
        """Imprime a nota fiscal para o cliente"""
        try:
            numero_pedido = int(input("Digite o número do pedido para imprimir nota: "))
            
            if numero_pedido not in self.pedidos:
                print("❌ Pedido não encontrado!")
                return
            
            pedido = self.pedidos[numero_pedido]
            
            print("\n" + "=" * 60)
            print("              🍣 NOTA FISCAL 🍱")
            print("=" * 60)
            print(f"Pedido: #{numero_pedido}")
            print(f"Mesa: {pedido['mesa']}")
            print(f"Horário: {pedido['data_hora']}")
            print(f"Status: {pedido['status'].upper()}")
            print("-" * 60)
            
            total = 0
            for codigo, quantidade in pedido["itens"].items():
                item = self.cardapio[codigo]
                subtotal = item["preco"] * quantidade
                total += subtotal
                print(f"{quantidade:2d}x {item['nome']:<30} R$ {subtotal:6.2f}")
            
            print("-" * 60)
            print(f"{'TOTAL:':<35} R$ {total:6.2f}")
            print("=" * 60)
            print("🍣 Obrigado pela preferência! 🍱")
            print("=" * 60)
        
        except ValueError:
            print("❌ Por favor, digite um número válido!")
    
    def relatorio_pedidos(self):
        """Exibe relatório de todos os pedidos"""
        if not self.pedidos:
            print("📭 Nenhum pedido foi realizado!")
            return
        
        print("\n" + "=" * 60)
        print("              📊 RELATÓRIO DE PEDIDOS")
        print("=" * 60)
        
        pedidos_pendentes = {num: ped for num, ped in self.pedidos.items() if ped["status"] == "pendente"}
        pedidos_entregues = {num: ped for num, ped in self.pedidos.items() if ped["status"] == "entregue"}
        
        print(f"\n📋 RESUMO:")
        print(f"Pedidos Pendentes: {len(pedidos_pendentes)}")
        print(f"Pedidos Entregues: {len(pedidos_entregues)}")
        print(f"Total de Pedidos: {len(self.pedidos)}")
        
        if pedidos_pendentes:
            print(f"\n⌛ PEDIDOS PENDENTES:")
            for numero, pedido in pedidos_pendentes.items():
                print(f"  #{numero} - Mesa {pedido['mesa']} - {pedido['data_hora']}")
        
        if pedidos_entregues:
            print(f"\n✅ PEDIDOS ENTREGUES:")
            for numero, pedido in pedidos_entregues.items():
                print(f"  #{numero} - Mesa {pedido['mesa']} - Entregue: {pedido['hora_entrega']}")

def main():
    restaurante = MenuJapones()
    
    while True:
        print("\n" + "=" * 60)
        print("        🍣 RESTAURANTE JAPONÊS - SISTEMA 🍱")
        print("=" * 60)
        print("1. Ver Menu Completo")
        print("2. Fazer Pedido")
        print("3. Listar Pedidos Pendentes")
        print("4. Imprimir Comanda para Cozinha")
        print("5. Confirmar Entrega do Pedido")
        print("6. Imprimir Nota Fiscal")
        print("7. Relatório de Pedidos")
        print("8. Sair")
        print("-" * 60)
        
        try:
            opcao = int(input("Escolha uma opção: "))
            
            if opcao == 1:
                restaurante.exibir_menu()
                input("\nPressione Enter para continuar...")
            
            elif opcao == 2:
                restaurante.fazer_pedido()
                input("\nPressione Enter para continuar...")
            
            elif opcao == 3:
                restaurante.listar_pedidos_pendentes()
                input("\nPressione Enter para continuar...")
            
            elif opcao == 4:
                restaurante.imprimir_comanda_cozinha()
                input("\nPressione Enter para continuar...")
            
            elif opcao == 5:
                restaurante.confirmar_entrega()
                input("\nPressione Enter para continuar...")
            
            elif opcao == 6:
                restaurante.imprimir_nota_cliente()
                input("\nPressione Enter para continuar...")
            
            elif opcao == 7:
                restaurante.relatorio_pedidos()
                input("\nPressione Enter para continuar...")
            
            elif opcao == 8:
                print("🍣 Obrigado por usar nosso sistema! 🍱")
                break
            
            else:
                print("❌ Opção inválida! Tente novamente.")
        
        except ValueError:
            print("❌ Por favor, digite um número válido!")

if __name__ == "__main__":
    main()