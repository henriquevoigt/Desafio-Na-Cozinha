from controllers.livro_receitas import carregar_receitas
from controllers.arvore_nomes import construir_tries_busca
from views.menu import rodar_menu 

def main():
    print("Iniciando os fogões... Carregando base de dados...\n")
 
    estante_de_receitas = carregar_receitas()

    t_nomes, t_ids, t_categorias = construir_tries_busca(estante_de_receitas)

    rodar_menu(t_nomes, t_ids, t_categorias, estante_de_receitas)

if __name__ == "__main__":
    main()