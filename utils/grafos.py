def ordenacao_topologica_kahn(grafo, graus_entrada):
    """
    grafo: dict { id_no: [ids_vizinhos] }
    graus_entrada: dict { id_no: int }
    """
    fila = [no for no in graus_entrada if graus_entrada[no] == 0]
    ordem_topologica = []

    while fila:
        atual = fila.pop(0)
        ordem_topologica.append(atual)

        for vizinho in grafo.get(atual, []):
            graus_entrada[vizinho] -= 1
            if graus_entrada[vizinho] == 0:
                fila.append(vizinho)

    tem_ciclo = len(ordem_topologica) != len(graus_entrada)
    
    return ordem_topologica, tem_ciclo