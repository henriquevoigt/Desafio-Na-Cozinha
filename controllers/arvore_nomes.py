from models.receita import Receita
from models.trie import Trie

def construir_tries_busca(todas_as_receitas: list[Receita]):
    trie_nomes = Trie()
    trie_ids = Trie()
    trie_categorias = Trie()
    
    for receita in todas_as_receitas:

        trie_nomes.insert(receita.name, receita)
        for palavra in receita.name.split():
            trie_nomes.insert(palavra, receita)

        trie_ids.insert(str(receita.id), receita)
        
        if hasattr(receita, 'cuisine'): 
            trie_categorias.insert(receita.cuisine, receita)

    return trie_nomes, trie_ids, trie_categorias