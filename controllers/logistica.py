import json
import os
from utils.rotas import calcular_dijkstra, calcular_prim

def carregar_mapa():

    caminho = "data/mapa.json"
    if not os.path.exists(caminho):
        return None, None

    with open(caminho, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    nomes_bairros = {v['id']: v['nome'] for v in dados['vertices']}

    grafo = {v['id']: [] for v in dados['vertices']}

    for aresta in dados['arestas']:
        o = aresta['origem']
        d = aresta['destino']
        p = aresta['peso']

        grafo[o].append({'destino': d, 'peso': p})
        grafo[d].append({'destino': o, 'peso': p})

    return grafo, nomes_bairros


def rotear_entrega(id_destino):
    """ Chama o Dijkstra partindo do Restaurante Jacquin (ID 0) """
    grafo, nomes = carregar_mapa()
    if not grafo:
        return False, "Erro: mapa.json não encontrado."

    if id_destino not in grafo:
        return False, "Bairro de destino não existe no mapa."

    tempo, caminho_ids = calcular_dijkstra(grafo, 0, id_destino)

    rota_nomes = [nomes[id_bairro] for id_bairro in caminho_ids]
    
    return True, (tempo, rota_nomes)


def planejar_infraestrutura():

    grafo, nomes = carregar_mapa()
    if not grafo:
        return False, "Erro: mapa.json não encontrado."

    custo_total, arestas_mst = calcular_prim(grafo, 0)

    conexoes = []
    for u, v, peso in arestas_mst:
        conexoes.append(f"{nomes[u]} <--> {nomes[v]} ({peso} min)")
        
    return True, (custo_total, conexoes)