import heapq

def calcular_dijkstra(grafo, origem, destino, bloqueios=None):
    if bloqueios is None:
        bloqueios = set()

    distancias = {v: float('inf') for v in grafo}
    distancias[origem] = 0

    pq = [(0, origem)]
    rastreio = {origem: None}

    while pq:
        dist_atual, u = heapq.heappop(pq)

        if dist_atual > distancias[u]:
            continue

        if u == destino:
            break

        for vizinho in grafo[u]:
            v = vizinho['destino']
            peso = vizinho['peso']
            
            if v in bloqueios:
                continue
            
            nova_distancia = dist_atual + peso

            if nova_distancia < distancias[v]:
                distancias[v] = nova_distancia
                rastreio[v] = u
                heapq.heappush(pq, (nova_distancia, v))

    if distancias[destino] == float('inf'):
        return float('inf'), []

    caminho = []
    atual = destino
    while atual is not None:
        caminho.append(atual)
        atual = rastreio.get(atual)
    
    caminho.reverse() 

    return distancias[destino], caminho


def calcular_prim(grafo, vertice_inicial=0):

    mst = []
    visitados = set([vertice_inicial])
    pq = []
    custo_total = 0

    for vizinho in grafo[vertice_inicial]:
        heapq.heappush(pq, (vizinho['peso'], vertice_inicial, vizinho['destino']))

    while pq and len(visitados) < len(grafo):
        peso, u, v = heapq.heappop(pq)

        if v not in visitados:
            visitados.add(v)
            mst.append((u, v, peso)) 
            custo_total += peso

            for vizinho in grafo[v]:
                if vizinho['destino'] not in visitados:
                    heapq.heappush(pq, (vizinho['peso'], v, vizinho['destino']))

    return custo_total, mst

def calcular_tsp_vizinho_mais_proximo(grafo, origem, destinos):

    rota_completa = []
    tempo_total = 0
    atual = origem
    pendentes = destinos.copy()

    while pendentes:
        mais_proximo = None
        menor_tempo = float('inf')
        melhor_caminho = []

        for destino in pendentes:
            tempo, caminho = calcular_dijkstra(grafo, atual, destino)
            if tempo < menor_tempo:
                menor_tempo = tempo
                mais_proximo = destino
                melhor_caminho = caminho

        if mais_proximo is None:
            break

        tempo_total += menor_tempo
        
        if rota_completa:
            melhor_caminho = melhor_caminho[1:]
            
        rota_completa.extend(melhor_caminho)
        atual = mais_proximo
        pendentes.remove(mais_proximo)

    tempo_volta, caminho_volta = calcular_dijkstra(grafo, atual, origem)
    tempo_total += tempo_volta
    rota_completa.extend(caminho_volta[1:])

    return tempo_total, rota_completa