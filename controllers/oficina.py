from utils.grafos import ordenacao_topologica_kahn

def analisar_producao(estante_de_receitas):

    grafo = {r.id: [] for r in estante_de_receitas}
    graus_entrada = {r.id: 0 for r in estante_de_receitas}
    dicionario_receitas = {r.id: r for r in estante_de_receitas}

    for receita in estante_de_receitas:
        for dep_id in receita.dependencias:
            # se a 'receita' depende do 'dep_id', a aresta aponta: dep_id -> receita
            grafo[dep_id].append(receita.id)
            graus_entrada[receita.id] += 1

    ordem_ids, tem_ciclo = ordenacao_topologica_kahn(grafo, graus_entrada)

    if tem_ciclo:
        return False, "ERRO CRÍTICO: Ciclo de dependência detectado! O cardápio possui um paradoxo de preparo e a produção está bloqueada."
    
    else:
        ordem_nomes = [dicionario_receitas[id_receita].name for id_receita in ordem_ids]
        return True, ordem_nomes