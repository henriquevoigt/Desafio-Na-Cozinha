import os
import subprocess
from controllers.livro_receitas import carregar_receitas
from controllers.arvore_nomes import construir_tries_busca
from controllers.ingredientes import construir_indice_ingredientes
from views.menu import rodar_menu 
from models.hash_table import HashTable
from models.btree_disco import BTreeDisco

def limpar_tela():
    comando = "cls" if os.name == "nt" else "clear"
    subprocess.run([comando], shell=True)

def iniciar_sistema_completo():
    limpar_tela()
    print("Iniciando os fogões... Carregando base de dados...\n")
    estante_de_receitas = carregar_receitas()

    print("Sincronizando Árvore B no disco físico...")
    btree = BTreeDisco()

    for receita in estante_de_receitas:
        if not btree.buscar(receita.id):
            btree.inserir(receita.id, receita)

    hash_table = HashTable()
    for receita in estante_de_receitas:
        hash_table.insert(receita)

    t_nomes, t_ids, t_categorias = construir_tries_busca(estante_de_receitas)
    indice_ingredientes = construir_indice_ingredientes(estante_de_receitas)

    rodar_menu(t_nomes, t_ids, t_categorias, estante_de_receitas, hash_table, indice_ingredientes)

def iniciar_modo_recuperacao():
    limpar_tela()
    print("=" * 60)
    print(" MODO DE RECUPERAÇÃO - LEITURA DIRETA NO DISCO")
    print("=" * 60)
    print(" > A RAM está limpa. O arquivo JSON NÃO foi carregado.")
    print(" > As estruturas Trie e Hash Table NÃO existem na memória.\n")
    
    btree = BTreeDisco()
    
    while True:
        id_busca = input("\nDigite o ID da receita para buscar (ou '0' para sair): ")
        
        if id_busca == '0':
            break
            
        if id_busca.isdigit():
            receita = btree.buscar(int(id_busca))
            
            if receita:
                print("\n[!] RECEITA ENCONTRADA DIRETO DO DISCO:")
                print(f"[{receita.id}] {receita.name}")
                print(f"    Tempo: {receita.prepTimeMinutes}min | Dificuldade: {receita.difficulty}")
            else:
                print(f"\n[X] Receita com ID {id_busca} não foi encontrada na Árvore B.")
        else:
            print("\n[X] Por favor, digite um número inteiro válido.")

def gerenciar_boot():
    while True:
        limpar_tela()
        print("=" * 60)
        print(" BOOT DO SISTEMA - ESCOLHA O MODO DE INICIALIZAÇÃO ")
        print("=" * 60)
        print(" [1] Iniciar Sistema Completo (Carregar JSON, RAM, etc)")
        print(" [2] Prova de Isolamento: Árvore B Direto do Disco")
        print(" [0] Sair")
        print("=" * 60)
        
        opcao = input("\nEscolha uma opção de boot: ")
        
        if opcao == '1':
            iniciar_sistema_completo()
        elif opcao == '2':
            iniciar_modo_recuperacao()
        elif opcao == '0':
            limpar_tela()
            print("Desligando sistema...\n")
            break
        else:
            print("\nOpção inválida.")
            input("Pressione ENTER para tentar novamente...")