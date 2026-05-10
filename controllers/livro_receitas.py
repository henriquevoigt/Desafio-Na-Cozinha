import os
import urllib.request
import json

from models.receita import Receita

def garantir_db():

    url = "https://dummyjson.com/recipes?limit=50"
    caminho_local = "data/receitas.json"

    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(caminho_local):
        print("Baixando base de dados...")
        requisicao = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(requisicao) as resposta, open(caminho_local, 'wb') as arquivo:
            arquivo.write(resposta.read())
        print("Download concluido!")
    
def carregar_receitas() -> list[Receita]:

    garantir_db()
    lista = [] 

    with open("data/receitas.json", "r", encoding="utf-8") as arquivo:

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
                mealType=item["mealType"]
            )

            lista.append(nova_receita)
            
    return lista