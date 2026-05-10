import subprocess
import os

def limpar_tela():
    comando = "cls" if os.name == "nt" else "clear"
    subprocess.run([comando], shell=True)

def exibir_receita_resumida(receita):
    print(f"[{receita.id}] {receita.name}")
    print(f"    Tempo: {receita.prepTimeMinutes}min | Dificuldade: {receita.difficulty}")
    print(f"    Ingredientes: {receita.ingredients[:3]}...")
    print("-" * 40)

def sub_menu_busca(trie_nomes, trie_ids, trie_categorias):
    while True:
        limpar_tela()
        print("=" * 40)
        print("  MODO CONSULTA RÁPIDA")
        print("=" * 40)
        print(" [1] Buscar por ID (Trie)")
        print(" [2] Buscar por Nome (Trie)")
        print(" [3] Buscar por Ingrediente (Hash - EM BREVE)")
        print(" [4] Buscar por Categoria (Trie)")
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
            print("\n O Módulo de Ingredientes requer a Tabela Hash manual.")
            input("Pressione ENTER para voltar...")
            
        elif opcao == '0':
            break
        else:
            print("\n Opção inválida!")
            input("Pressione ENTER para voltar...")

def sub_menu_investigacao():
    while True:
        limpar_tela()
        print("=" * 40)
        print(" MODO INVESTIGAÇÃO (SABOTAGEM)")
        print("=" * 40)
        print(" Critério de validação de Hash:")
        print(" [1] Validar por ID")
        print(" [2] Validar por Nome")
        print(" [3] Validar por Ingrediente")
        print(" [0] Voltar ao Menu Principal")
        print("=" * 40)
        
        opcao = input("\nEscolha uma opção: ")
        if opcao == '0':
            break
        else:
            print("\n Tabela Hash manual em construção!")
            input("Pressione ENTER para voltar...")

def sub_menu_chef():
    while True:
        limpar_tela()
        print("=" * 40)
        print("  MODO CHEF (ALGORITMO GULOSO)")
        print("=" * 40)
        print(" Parâmetro de restrição:")
        print(" [1] Tempo de Preparo")
        print(" [2] Dificuldade")
        print(" [3] Avaliação (Rating)")
        print(" [0] Voltar ao Menu Principal")
        print("=" * 40)
        
        opcao = input("\nEscolha uma opção: ")
        if opcao == '0':
            break
        else:
            print("\n Algoritmo Guloso em construção!")
            input("Pressione ENTER para voltar...")

def rodar_menu(trie_nomes, trie_ids, trie_categorias, estante_de_receitas):
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
            sub_menu_busca(trie_nomes, trie_ids, trie_categorias)
            
        elif opcao == '3':
            sub_menu_investigacao()
            
        elif opcao == '4':
            sub_menu_chef()
            
        elif opcao == '0':
            limpar_tela()
            print("Au revoir! Desligando os fogões...\n")
            break
            
        else:
            print("\n Opção inválida. Tente novamente.")
            input("Pressione ENTER para voltar...")