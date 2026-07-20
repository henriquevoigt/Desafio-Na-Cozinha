from utils.grafos import ordenacao_topologica_kahn

def analisar_producao(estante_de_receitas):
    """ Resolve as Consultas 1 e 2: Sequência Correta e Erros de Dependência """
    grafo = {r.id: [] for r in estante_de_receitas}
    graus_entrada = {r.id: 0 for r in estante_de_receitas}
    dicionario_receitas = {r.id: r for r in estante_de_receitas}

    for receita in estante_de_receitas:
        for dep_id in receita.dependencias:
            grafo[dep_id].append(receita.id)
            graus_entrada[receita.id] += 1

    ordem_ids, tem_ciclo, nos_travados = ordenacao_topologica_kahn(grafo, graus_entrada)

    if tem_ciclo:
        nomes_travados = [dicionario_receitas[id_no].name for id_no in nos_travados]
        mensagem = f"ERRO CRÍTICO: Ciclo de dependência detectado!\nAs seguintes receitas causaram um paradoxo ou estão bloqueadas: {', '.join(nomes_travados)}"
        return False, mensagem
    else:
        ordem_nomes = [dicionario_receitas[id_receita].name for id_receita in ordem_ids]
        return True, ordem_nomes


def consultar_prerequisitos(estante_de_receitas, id_alvo):

    dicionario = {r.id: r for r in estante_de_receitas}
    
    if id_alvo not in dicionario:
        return False, "Receita não encontrada no banco de dados."

    alvo = dicionario[id_alvo]
    visitados = set()
    
    def rastrear(receita_id):
        for dep_id in dicionario[receita_id].dependencias:
            if dep_id not in visitados:
                visitados.add(dep_id)
                rastrear(dep_id)

    rastrear(id_alvo)
    
    if not visitados:
        return True, (alvo.name, [])
        
    nomes_deps = [dicionario[v].name for v in visitados]
    return True, (alvo.name, nomes_deps)