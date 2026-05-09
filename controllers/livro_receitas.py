import os
import urllib.request
import json

from models.receita import Receita

def garantir_db():
    
    url = "https://dummyjson.com/recipes?limit=50"
    caminho_local = "data/receitas.json"

    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists("caminho_local"):
        print("Baixando base de dados...")
        urllib.request.urlretrieve(url, caminho_local)
        print("Download concluido!")
    
