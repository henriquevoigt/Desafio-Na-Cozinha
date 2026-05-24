from controllers.livro_receitas import carregar_receitas
from controllers.arvore_nomes import construir_tries_busca
from controllers.ingredientes import construir_indice_ingredientes
from views.menu import rodar_menu 
from models.hash_table import HashTable

def main():
    print("Iniciando os fogões... Carregando base de dados...\n")
 
    estante_de_receitas = carregar_receitas()

    hash_table = HashTable()
    for receita in estante_de_receitas:
        hash_table.insert(receita)

    t_nomes, t_ids, t_categorias = construir_tries_busca(estante_de_receitas)
    
    indice_ingredientes = construir_indice_ingredientes(estante_de_receitas)

    rodar_menu(t_nomes, t_ids, t_categorias, estante_de_receitas, hash_table, indice_ingredientes)

if __name__ == "__main__":
    main()