from utils.otimizacao import knapsack_dp, backtracking_combos

def maximizar_lucro_cardapio(estante_de_receitas, orcamento_disponivel):

    capacidade_int = int(orcamento_disponivel * 10)
    
    pesos = [int(r.custo * 10) for r in estante_de_receitas]
    valores = [r.valor_venda for r in estante_de_receitas]
    
    lucro_max, indices_escolhidos = knapsack_dp(pesos, valores, capacidade_int)
    
    if not indices_escolhidos:
        return False, "Orçamento insuficiente para criar um cardápio."
        
    receitas_escolhidas = [estante_de_receitas[i] for i in indices_escolhidos]
    custo_total = sum(r.custo for r in receitas_escolhidas)
    
    return True, (lucro_max, custo_total, receitas_escolhidas)


def gerar_menu_namorados(estante_de_receitas, orcamento_maximo):
    entradas = [r for r in estante_de_receitas if r.classe == "Entrada"]
    principais = [r for r in estante_de_receitas if r.classe == "Prato Principal"]
    sobremesas = [r for r in estante_de_receitas if r.classe == "Sobremesa"]

    combos = backtracking_combos(entradas, principais, sobremesas, orcamento_maximo)
    
    if not combos:
        return False, "Nenhum combo possível com esse orçamento."
        
    return True, combos