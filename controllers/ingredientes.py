from models.receita import Receita

def construir_indice_ingredientes(todas_as_receitas: list[Receita]) -> dict:
    indice = {} 
    
    for receita in todas_as_receitas:  

        for ingrediente in receita.ingredients:
            
            ingrediente_limpo = ingrediente.lower()
            palavras = ingrediente_limpo.split(' ')

            for palavra in palavras:

                if palavra not in indice:
                    indice[palavra] = []

                if receita not in indice[palavra]:
                    indice[palavra].append(receita)
                
    return indice