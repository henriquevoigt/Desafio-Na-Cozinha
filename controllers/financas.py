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


def gerar_menu_namorados(entradas, principais, sobremesas, orcamento_max, tempo_max):
    melhor_combo = None
    maior_lucro = -1.0

    categorias = [entradas, principais, sobremesas]

    def backtrack(nivel, combo_atual, custo_atual, tempo_atual):
        nonlocal melhor_combo, maior_lucro

        if custo_atual > orcamento_max or tempo_atual > tempo_max:
            return 

        if nivel == 3:
            lucro_combo = sum((p.valor_venda - p.custo) for p in combo_atual)

            if lucro_combo > maior_lucro:
                maior_lucro = lucro_combo
                melhor_combo = list(combo_atual)
            return

        for prato in categorias[nivel]:
            tempo_prato = prato.prepTimeMinutes + prato.cookTimeMinutes
            novo_custo = custo_atual + prato.custo
            novo_tempo = tempo_atual + tempo_prato

            if novo_custo <= orcamento_max and novo_tempo <= tempo_max:
                combo_atual.append(prato) 
                backtrack(nivel + 1, combo_atual, novo_custo, novo_tempo) 
                combo_atual.pop()

    backtrack(0, [], 0.0, 0)
    
    if melhor_combo:
        return True, melhor_combo
    else:
        return False, "Nenhuma combinação atende às restrições informadas."
    
def exibir_relatorio_combo_namorados(combo):
    entrada, principal, sobremesa = combo

    valor_total = sum(p.valor_venda for p in combo)
    custo_total = sum(p.custo for p in combo)
    lucro_total = valor_total - custo_total
    tempo_total = sum(p.prepTimeMinutes + p.cookTimeMinutes for p in combo)

    avaliacao_media = sum(p.rating for p in combo if hasattr(p, 'rating')) / 3

    dificuldades = [p.difficulty for p in combo]
    if "Hard" in dificuldades:
        dificuldade_log = "alta"
    elif "Medium" in dificuldades:
        dificuldade_log = "média"
    else:
        dificuldade_log = "baixa"

    print("\nMenu Especial Dia dos Namorados:")
    print(f"Entrada: {entrada.name}")
    print(f"Prato principal: {principal.name}")
    print(f"Sobremesa: {sobremesa.name}")
    print(f"Valor total de venda: R$ {valor_total:.2f}".replace(".", ","))
    print(f"Custo estimado: R$ {custo_total:.2f}".replace(".", ","))
    print(f"Lucro estimado: R$ {lucro_total:.2f}".replace(".", ","))
    print(f"Tempo total de preparo: {tempo_total} minutos")
    print(f"Avaliação média: {avaliacao_media:.1f}")
    print(f"Dificuldade logística: {dificuldade_log}")
    print("\nJustificativa:")
    print(f"O menu foi escolhido por apresentar o maior lucro estimado (R$ {lucro_total:.2f}) dentro do orçamento rigoroso.")
    print(f"Além disso, o tempo de preparo de {tempo_total} minutos respeita as restrições impostas, "
          f"e sua dificuldade logística {dificuldade_log} permite que a equipe consiga produzi-lo em uma noite de alta demanda.")