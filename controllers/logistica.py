import json
import os
from utils.rotas import calcular_dijkstra, calcular_prim, calcular_tsp_vizinho_mais_proximo

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


def rotear_entrega(id_destino, string_bloqueios=""):
    grafo, nomes = carregar_mapa()
    if not grafo:
        return False, "Erro: mapa.json não encontrado."

    if id_destino not in grafo:
        return False, "Bairro de destino não existe no mapa."

    bloqueios = set()
    if string_bloqueios.strip():
        try:
            bloqueios = {int(x.strip()) for x in string_bloqueios.split(',')}
        except ValueError:
            return False, "Formato de bloqueio inválido. Use números separados por vírgula."
        
        for b in bloqueios:
            if b not in grafo:
                return False, f"O bairro bloqueado ID {b} não existe no mapa."
            if b == 0:
                return False, "Você não pode bloquear o Restaurante (Base)!"
            if b == id_destino:
                return False, "Você não pode bloquear o destino final da entrega!"

    # calcula a rota ideal
    tempo_ideal, caminho_ideal = calcular_dijkstra(grafo, 0, id_destino)

    if not bloqueios:
        rota_nomes = [nomes[id_bairro] for id_bairro in caminho_ideal]
        return True, (tempo_ideal, rota_nomes, False)

    # calcula a rota real
    tempo_real, caminho_real = calcular_dijkstra(grafo, 0, id_destino, bloqueios)

    if tempo_real == float('inf'):
        return False, f"ROTA IMPOSSÍVEL! Os bloqueios isolaram completamente o caminho para {nomes[id_destino]}."

    # compara as rotas para descobrir se houve desvio
    houve_desvio = (caminho_ideal != caminho_real)
    
    rota_nomes = [nomes[id_bairro] for id_bairro in caminho_real]
    
    return True, (tempo_real, rota_nomes, houve_desvio)


def planejar_infraestrutura():

    grafo, nomes = carregar_mapa()
    if not grafo:
        return False, "Erro: mapa.json não encontrado."

    custo_total, arestas_mst = calcular_prim(grafo, 0)

    conexoes = []
    for u, v, peso in arestas_mst:
        conexoes.append(f"{nomes[u]} <--> {nomes[v]} ({peso} min)")
        
    return True, (custo_total, conexoes)

def rotear_multiplas_entregas(string_destinos):
    
    grafo, nomes = carregar_mapa()
    if not grafo:
        return False, "Erro: mapa.json não encontrado."

    try:
        # transforma a string "4, 15, 2" em uma lista de inteiros [4, 15, 2]
        destinos = [int(x.strip()) for x in string_destinos.split(',')]
    except ValueError:
        return False, "Formato inválido. Use números separados por vírgula."

    for d in destinos:
        if d not in grafo:
            return False, f"O bairro ID {d} não existe no mapa."
            
    if 0 in destinos:
        return False, "O restaurante (ID 0) já é a base, não precisa ser um destino."

    tempo, caminho_ids = calcular_tsp_vizinho_mais_proximo(grafo, 0, destinos)
    
    rota_nomes = [nomes[id_bairro] for id_bairro in caminho_ids]
    ordem_entregas = [nomes[d] for d in destinos]
    
    return True, (tempo, rota_nomes, ordem_entregas)