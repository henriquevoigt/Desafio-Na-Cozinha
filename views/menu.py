import subprocess
import os
from controllers.investigacao import *
from controllers.recomendacao import recomendar_cardapio_guloso
from controllers.oficina import analisar_producao
from controllers.financas import maximizar_lucro_cardapio, gerar_menu_namorados
from controllers.logistica import rotear_entrega, planejar_infraestrutura, rotear_multiplas_entregas

def limpar_tela():
    comando = "cls" if os.name == "nt" else "clear"
    subprocess.run([comando], shell=True)

def exibir_receita_resumida(receita):
    print(f"[{receita.id}] {receita.name}")
    print(f"    Tempo: {receita.prepTimeMinutes}min | Dificuldade: {receita.difficulty}")
    print(f"    Ingredientes: {receita.ingredients[:3]}...")
    print("-" * 40)

def exibir_receita_completa(receita):
    limpar_tela()
    print("=" * 60)
    print(f"RECEITA: {receita.name.upper()} (ID: {receita.id})")
    print("=" * 60)
    print(f" Dificuldade: {receita.difficulty}")
    print(f" Tempo de Preparo: {receita.prepTimeMinutes} min")
    print(f" Tempo de Cozimento: {receita.cookTimeMinutes} min")
    print("-" * 60)
    print("INGREDIENTES:")
    for ing in receita.ingredients:
        print(f"   - {ing}")
    print("-" * 60)
    print("MODO DE PREPARO:")

    if isinstance(receita.instructions, list):
        for i, passo in enumerate(receita.instructions, 1):
            print(f"   {i}. {passo}")
    else:
        print(f"   {receita.instructions}")
    print("=" * 60)

def sub_menu_busca(trie_nomes, trie_ids, trie_categorias, indice_ingredientes):
    while True:
        limpar_tela()
        print("=" * 40)
        print("  MODO CONSULTA RÁPIDA")
        print("=" * 40)
        print(" [1] Buscar por ID (Trie)")
        print(" [2] Buscar por Nome (Trie)")
        print(" [3] Buscar por Ingrediente (Hash)")
        print(" [4] Buscar por Categoria (Trie)")
        print(" [5] Ver receita completa por ID")
        print(" [0] Voltar ao Menu Principal")
        print("=" * 40)
        
        opcao = input("\nEscolha o tipo de busca: ")

        if opcao == '1':
            limpar_tela()
            print("--- BUSCA POR ID ---")
            prefixo = input("Digite o ID (ou início do ID): ").strip()
            
            resultados_brutos = trie_ids.search_prefix(prefixo)
            resultados_unicos = list({r.id: r for r in resultados_brutos}.values())
            
            if not resultados_unicos:
                print(f"\n Nenhum ID encontrado começando com '{prefixo}'.")
            else:
                print(f"\n {len(resultados_unicos)} resultado(s) encontrado(s)!\n")
                for receita in resultados_unicos:
                    exibir_receita_resumida(receita)
            input("\nPressione ENTER para voltar...")

        elif opcao == '2':
            limpar_tela()
            print("--- BUSCA POR NOME ---")
            prefixo = input("Digite o começo do nome ou palavra-chave: ").strip()

            resultados_brutos = trie_nomes.search_prefix(prefixo)
            resultados_unicos = list({r.id: r for r in resultados_brutos}.values())
            
            if not resultados_unicos:
                print(f"\n Nenhuma receita encontrada com '{prefixo}'.")
            else:
                print(f"\n {len(resultados_unicos)} resultado(s) encontrado(s)!\n")
                for receita in resultados_unicos:
                    exibir_receita_resumida(receita)
            input("\nPressione ENTER para voltar...")

        elif opcao == '4':
            limpar_tela()
            print("--- BUSCA POR CATEGORIA ---")
            prefixo = input("Digite a categoria (ex: Italian, Brazilian, etc.): ").strip()

            resultados_brutos = trie_categorias.search_prefix(prefixo)
            resultados_unicos = list({r.id: r for r in resultados_brutos}.values())
            
            if not resultados_unicos:
                print(f"\n Nenhuma categoria encontrada começando com '{prefixo}'.")
            else:
                print(f"\n {len(resultados_unicos)} resultado(s) encontrado(s)!\n")
                for receita in resultados_unicos:
                    exibir_receita_resumida(receita)
            input("\nPressione ENTER para voltar...")

        elif opcao == '3':
            limpar_tela()
            print("--- BUSCA POR INGREDIENTE ---")
            ingrediente = input("Digite o nome do ingrediente: ").strip().lower()
            
            if ingrediente in indice_ingredientes:
                resultados = indice_ingredientes[ingrediente]
                print(f"\n {len(resultados)} resultado(s) encontrado(s)!\n")
                for receita in resultados:
                    exibir_receita_resumida(receita)
            else:
                print(f"\n Nenhuma receita encontrada com '{ingrediente}'.")
                
            input("\nPressione ENTER para voltar...")

        elif opcao == '5':
            limpar_tela()
            print("--- VER RECEITA COMPLETA ---")
            id_busca = input("Digite o ID exato da receita: ").strip()

            resultados_brutos = trie_ids.search_prefix(id_busca)

            receita_encontrada = None
            for r in resultados_brutos:
                if str(r.id) == id_busca:
                    receita_encontrada = r
                    break
            
            if receita_encontrada:
                exibir_receita_completa(receita_encontrada)
            else:
                print(f"\n Receita com ID '{id_busca}' não encontrada.")
            
            input("\nPressione ENTER para voltar...")
            
        elif opcao == '0':
            break
        else:
            print("\n Opção inválida!")
            input("Pressione ENTER para voltar...")

def sub_menu_investigacao(estante_de_receitas, hash_table):
    while True:
        limpar_tela()
        print("=" * 40)
        print("MODO INVESTIGAÇÃO (SABOTAGEM)")
        print("=" * 40)
        print(" Critério de validação de Hash:")
        print(" [1] Validar por ID")
        print(" [2] Validar por Nome")
        print(" [3] Validar por Ingrediente")
        print(" [4] Sabotar uma receita (Teste de Segurança)")
        print(" [0] Voltar ao Menu Principal")
        print("=" * 40)
        
        opcao = input("\nEscolha uma opção: ")
        if opcao == '0':
            break
        elif opcao == '1':
            investigar_por_id(estante_de_receitas, hash_table)
        elif opcao == '2':
            investigar_por_nome(estante_de_receitas, hash_table)
        elif opcao == '3':
            investigar_por_ingrediente(estante_de_receitas, hash_table)
        elif opcao == '4':
            sabotar_receita(estante_de_receitas)
        else:
            print("\n Opção inválida!")
            input("Pressione ENTER para voltar...")

def sub_menu_chef(estante_de_receitas):
    while True:
        limpar_tela()
        print("=" * 40)
        print("MODO CHEF (ALGORITMO GULOSO)")
        print("=" * 40)
        print(" Otimização: Maximizar quantidade de pratos pelo tempo.")
        print(" [1] Gerar Cardápio")
        print(" [0] Voltar ao Menu Principal")
        print("=" * 40)
        
        opcao = input("\nEscolha uma opção: ")
        if opcao == '0':
            break
        elif opcao == '1':
            limpar_tela()
            print("--- GERADOR DE CARDÁPIO ---")
            try:
                tempo_max = int(input("Quanto tempo livre o Chef Jacquin tem? (em minutos): "))
                
                cardapio, tempo_gasto = recomendar_cardapio_guloso(estante_de_receitas, tempo_max)
                
                if not cardapio:
                    print("\nTempo insuficiente para preparar qualquer receita do banco de dados!")
                else:
                    print(f"\nCardápio Otimizado! ({len(cardapio)} receitas em {tempo_gasto} minutos)\n")
                    for receita in cardapio:
                        tempo_total = receita.prepTimeMinutes + receita.cookTimeMinutes
                        print(f"- [{receita.id}] {receita.name} (Tempo: {tempo_total} min)")
            except ValueError:
                print("\nPor favor, digite um número inteiro válido.")
                
            input("\nPressione ENTER para voltar...")
        else:
            print("\nOpção inválida!")
            input("Pressione ENTER para voltar...")

def sub_menu_oficina(estante_de_receitas):
    limpar_tela()
    print("=" * 40)
    print(" MODO OFICINA DE PRODUÇÃO (MÓDULO 5)")
    print("=" * 40)
    print(" Analisando dependências de preparo com Grafos...\n")
    
    deu_certo, resultado = analisar_producao(estante_de_receitas)
    
    if not deu_certo:
        print(" [!] ALERTA DO SISTEMA [!]")
        print(f" {resultado}")
    else:
        print(" [OK] Análise concluída. Nenhum ciclo encontrado.")
        print(" Ordem de preparo topológica otimizada:\n")
        # imprime as 10 primeiras
        for i, prato in enumerate(resultado[:10]):
            print(f"   {i+1}. {prato}")
        if len(resultado) > 10:
            print(f"   ... e mais {len(resultado) - 10} pratos prontos para a linha.")
            
    input("\nPressione ENTER para voltar ao menu...")

def sub_menu_financas(estante_de_receitas):
    while True:
        limpar_tela()
        print("=" * 45)
        print(" MODO INTELIGÊNCIA FINANCEIRA")
        print("=" * 45)
        print(" [1] Maximizar Lucro do Cardápio (PD - Módulo 6)")
        print(" [2] Criar Combos Dia dos Namorados (Backtracking)")
        print(" [0] Voltar ao Menu Principal")
        print("=" * 45)
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == '0':
            break
            
        elif opcao == '1':
            limpar_tela()
            print("--- MAXIMIZADOR DE LUCRO (PROGRAMAÇÃO DINÂMICA) ---")
            try:
                orcamento = float(input("Qual o orçamento de custo máximo para os pratos? R$ "))
                sucesso, resultado = maximizar_lucro_cardapio(estante_de_receitas, orcamento)
                
                if not sucesso:
                    print(f"\n[!] {resultado}")
                else:
                    lucro_max, custo_real, pratos = resultado
                    print(f"\n[OK] Análise Combinatória Concluída (Matriz Knapsack)")
                    print(f" Custo Total: R$ {custo_real:.2f} (Dentro do limite de R$ {orcamento:.2f})")
                    print(f" Potencial de Venda Maximizada: R$ {lucro_max:.2f}")
                    print("\n Pratos Selecionados:")
                    for prato in pratos:
                        print(f"  - {prato.name} (Custo: R$ {prato.custo:.2f} | Venda: R$ {prato.valor_venda:.2f})")
            except ValueError:
                print("\nPor favor, digite um valor válido.")
            input("\nPressione ENTER para voltar...")
            
        elif opcao == '2':
            limpar_tela()
            print("--- GERADOR DE COMBOS (BACKTRACKING) ---")
            try:
                orcamento = float(input("Qual o limite de custo para fechar o Combo? R$ "))
                sucesso, combos = gerar_menu_namorados(estante_de_receitas, orcamento)
                
                if not sucesso:
                    print(f"\n[!] {combos}")
                else:
                    print(f"\n[OK] {len(combos)} combinações encontradas via Poda (Pruning)!\n")
                    for i, combo in enumerate(combos[:5]):
                        custo = sum(p.custo for p in combo)
                        venda = sum(p.valor_venda for p in combo)
                        print(f"Combo {i+1} (Custo: R$ {custo:.2f} | Venda: R$ {venda:.2f})")
                        print(f"  Entrada:   {combo[0].name}")
                        print(f"  Principal: {combo[1].name}")
                        print(f"  Sobremesa: {combo[2].name}\n")
            except ValueError:
                print("\nPor favor, digite um valor válido.")
            input("\nPressione ENTER para voltar...")

def sub_menu_logistica():
    while True:
        limpar_tela()
        print("=" * 45)
        print(" MODO LOGÍSTICA DE ENTREGAS (GRAFOS)")
        print("=" * 45)
        print(" [1] Calcular Rota Única (Dijkstra - Mod. 7)")
        print(" [2] Planejar Filiais (Prim / MST - Mod. 7)")
        print(" [3] Rota do Entregador (Caixeiro Viajante - Mod. 8)")
        print(" [0] Voltar ao Menu Principal")
        print("=" * 45)
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == '0':
            break
            
        elif opcao == '1':
            limpar_tela()
            print("--- GPS JACQUIN (DIJKSTRA) ---")
            print("ID 1 = UFPel Anglo | ID 4 = Laranjal | ID 14 = Balsa | ID 24 = Rodoviária")
            try:
                destino = int(input("\nDigite o ID do bairro de destino: "))
                sucesso, resultado = rotear_entrega(destino)
                
                if not sucesso:
                    print(f"\n[!] {resultado}")
                else:
                    tempo, rota = resultado
                    print(f"\n[OK] Rota calculada com sucesso!")
                    print(f" Tempo estimado: {tempo} minutos")
                    print(f" Caminho: {' -> '.join(rota)}")
            except ValueError:
                print("\nPor favor, digite um número de ID válido.")
            input("\nPressione ENTER para voltar...")
            
        elif opcao == '2':
            limpar_tela()
            print("--- PROJETO DE EXPANSAO (ÁRVORE GERADORA MÍNIMA) ---")
            sucesso, resultado = planejar_infraestrutura()
            
            if not sucesso:
                print(f"\n[!] {resultado}")
            else:
                custo, conexoes = resultado
                print(f"\n[OK] Malha de rede calculada (Algoritmo de Prim)!")
                print(f" Custo total da infraestrutura: {custo} min")
                print("\n Conexões estratégicas selecionadas:")
                for c in conexoes:
                    print(f"  + {c}")
            input("\nPressione ENTER para voltar...")

        elif opcao == '3':
            limpar_tela()
            print("--- ROTA DO MOTOBOY (CAIXEIRO VIAJANTE / TSP) ---")
            print("IDs Populares: 1 (Anglo), 4 (Laranjal), 12 (Baronesa), 18 (Pestano)")
            destinos = input("\nDigite os IDs das entregas separados por vírgula (ex: 4, 12, 18): ")
            
            sucesso, resultado = rotear_multiplas_entregas(destinos)
            
            if not sucesso:
                print(f"\n[!] {resultado}")
            else:
                tempo, rota, pedidos = resultado
                print(f"\n[OK] Heurística do Vizinho Mais Próximo aplicada!")
                print(f" Tempo total (ida e volta): {tempo} minutos")
                print(f"\n Rota Passo a Passo:")

                caminho_formatado = ""
                for i, ponto in enumerate(rota):
                    if ponto in pedidos or i == 0 or i == len(rota)-1:
                        caminho_formatado += f"[{ponto}] -> "
                    else:
                        caminho_formatado += f"{ponto} -> "
                print(f" {caminho_formatado[:-4]}")
                print("\n * Locais em [Colchetes] são as paradas de entrega e a base.")
            
            input("\nPressione ENTER para voltar...")

def rodar_menu(trie_nomes, trie_ids, trie_categorias, estante_de_receitas, hash_table, indice_ingredientes):
    while True:
        limpar_tela()
        print("=" * 55)
        print(" SISTEMA DE GESTÃO - CHEF JACQUIN ")
        print("=" * 55)
        print(f"  [ Base de dados: {len(estante_de_receitas)} receitas cadastradas ]\n")
        print(" [1] Imprimir base de dados")
        print(" [2] Modo Consulta Rápida")
        print(" [3] Modo Investigação (Hash)")
        print(" [4] Modo Chef (Guloso)")
        print(" [5] Modo Oficina de Produção (Grafos)")
        print(" [6] Modo Finanças (PD/Backtracking)")
        print(" [7] Modo Logistica (Dijkstra/Prim)")
        print(" [0] Sair do sistema")
        print("=" * 55)
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == '1':
            limpar_tela()
            print(f"--- LISTANDO TODAS AS {len(estante_de_receitas)} RECEITAS ---\n")
            for receita in estante_de_receitas:
                exibir_receita_resumida(receita)
            input("\nPressione ENTER para voltar ao menu...")
            
        elif opcao == '2':
            sub_menu_busca(trie_nomes, trie_ids, trie_categorias, indice_ingredientes)
            
        elif opcao == '3':
            sub_menu_investigacao(estante_de_receitas, hash_table)
            
        elif opcao == '4':
            sub_menu_chef(estante_de_receitas)
            
        elif opcao == '5':
            sub_menu_oficina(estante_de_receitas)

        elif opcao == '6':
            sub_menu_financas(estante_de_receitas)

        elif opcao == '7':
            sub_menu_logistica()
            
        elif opcao == '0':
            limpar_tela()
            print("Au revoir! Desligando os fogões...\n")
            break
            
        else:
            print("\n Opção inválida. Tente novamente.")
            input("Pressione ENTER para voltar...")