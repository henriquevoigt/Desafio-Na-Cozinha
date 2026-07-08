import heapq

def calcular_dijkstra(grafo, origem, destino):
 
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
            
            nova_distancia = dist_atual + peso

            if nova_distancia < distancias[v]:
                distancias[v] = nova_distancia
                rastreio[v] = u
                heapq.heappush(pq, (nova_distancia, v))

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