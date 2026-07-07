def knapsack_dp(pesos, valores, capacidade_maxima):

    n = len(pesos)

    dp = [[0 for _ in range(capacidade_maxima + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(1, capacidade_maxima + 1):
            if pesos[i-1] <= w:

                dp[i][w] = max(valores[i-1] + dp[i-1][w - pesos[i-1]], dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]

    lucro_max = dp[n][capacidade_maxima]
    w = capacidade_maxima
    indices_escolhidos = []
    
    lucro_restante = lucro_max
    for i in range(n, 0, -1):
        if lucro_restante <= 0:
            break
        if dp[i][w] != dp[i-1][w]:
            indices_escolhidos.append(i-1)
            lucro_restante -= valores[i-1]
            w -= pesos[i-1]

    return dp[n][capacidade_maxima], indices_escolhidos


def backtracking_combos(entradas, principais, sobremesas, orcamento):

    combos_validos = []
    categorias = [entradas, principais, sobremesas]

    def backtrack(nivel, combo_atual, custo_atual):
        if custo_atual > orcamento:
            return 

        if nivel == 3:
            combos_validos.append(list(combo_atual))
            return

        for prato in categorias[nivel]:
            if custo_atual + prato.custo <= orcamento:
                combo_atual.append(prato) 
                backtrack(nivel + 1, combo_atual, custo_atual + prato.custo) 
                combo_atual.pop()

    backtrack(0, [], 0.0)
 
    combos_validos.sort(key=lambda c: sum(p.valor_venda for p in c), reverse=True)
    return combos_validos