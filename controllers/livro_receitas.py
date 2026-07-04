import json
import os
from models.receita import Receita

def carregar_receitas() -> list[Receita]:
    caminho_local = "data/receitas.json"

    # excluindo requisição da API, base será 100% local
    if not os.path.exists(caminho_local):
        raise FileNotFoundError(f"Erro Crítico: O banco de dados '{caminho_local}' não foi encontrado no repositório.")

    lista = [] 

    with open(caminho_local, "r", encoding="utf-8") as arquivo:
        dados_brutos = json.load(arquivo)
        lista_de_receitas = dados_brutos["recipes"]

        for item in lista_de_receitas:
            nova_receita = Receita(
                id=item["id"],
                name=item["name"],
                ingredients=item["ingredients"],
                instructions=item["instructions"],
                prepTimeMinutes=item["prepTimeMinutes"],
                cookTimeMinutes=item["cookTimeMinutes"],
                difficulty=item["difficulty"],
                cuisine=item["cuisine"],
                caloriesPerServing=item["caloriesPerServing"],
                tags=item["tags"],
                rating=item["rating"],
                reviewCount=item["reviewCount"],
                mealType=item["mealType"],
                
                # P2
                dependencias=item("dependencias"),
                custo=item("custo"),
                valor_venda=item("valor_venda"),
                classe=item("classe"),
                dificuldade_logistica=item("dificuldade_logistica")
            )
            lista.append(nova_receita)
            
    return lista