def ordenacao_topologica_kahn(grafo, graus_entrada):

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
    
    # se tem ciclo, quem sobrou com grau > 0 é o culpado/travado.
    nos_travados = [no for no, grau in graus_entrada.items() if grau > 0] if tem_ciclo else []

    return ordem_topologica, tem_ciclo, nos_travados