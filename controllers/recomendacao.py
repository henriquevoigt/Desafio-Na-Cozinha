def recomendar_cardapio_guloso(estante_de_receitas, tempo_maximo_minutos):
    
    receitas_ordenadas = sorted(estante_de_receitas, key=lambda r: r.prepTimeMinutes + r.cookTimeMinutes)
    
    cardapio = []
    tempo_acumulado = 0
    
    for receita in receitas_ordenadas:
        tempo_da_receita = receita.prepTimeMinutes + receita.cookTimeMinutes

        if tempo_acumulado + tempo_da_receita <= tempo_maximo_minutos:
            cardapio.append(receita)
            tempo_acumulado += tempo_da_receita
        else:
            break 
            
    return cardapio, tempo_acumulado