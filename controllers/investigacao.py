def validar_receita(receita, hash_table):
    if hash_table.verify(receita):
        print("\nReceita íntegra")
    else:
        print("\nReceita alterada")
    input("\nPressione ENTER para voltar...")


def investigar_por_id(estante_de_receitas, hash_table):
    recipe_id = int(input("Digite o ID da receita: "))
    for receita in estante_de_receitas:
        if receita.id == recipe_id:
            validar_receita(receita, hash_table)
            return
    print("\nReceita não encontrada")
    input("\nPressione ENTER...")

def sabotar_receita(estante_de_receitas):
    try:
        recipe_id = int(input("Digite o ID da receita para sabotar: "))
        for receita in estante_de_receitas:
            if receita.id == recipe_id:
                print(f"\n[!] Sabotando a receita: {receita.name}")
                receita.prepTimeMinutes = 9999
                receita.ingredients.append("Ketchup") 
                print("Sabotagem concluída! (O Chef Jacquin vai surtar...)")
                print("Vá validar essa receita agora para ver a Hash Table barrar a alteração.")
                input("\nPressione ENTER para voltar...")
                return
        print("\nReceita não encontrada.")
    except ValueError:
        print("\nID inválido.")
    input("\nPressione ENTER...")


def investigar_por_nome(estante_de_receitas, hash_table):
    nome = input("Digite o nome da receita: ").lower()
    for receita in estante_de_receitas:
        if receita.name.lower() == nome:
            validar_receita(receita, hash_table)
            return
    print("\nReceita não encontrada")
    input("\nPressione ENTER...")


def investigar_por_ingrediente(estante_de_receitas, hash_table):
    ingrediente = input("Digite o ingrediente: ").lower()
    encontrou = False
    for receita in estante_de_receitas:
        ingredientes = [i.lower() for i in receita.ingredients]
        if ingrediente in ingredientes:
            encontrou = True
            print(f"\n{receita.name}")
            if hash_table.verify(receita):
                print("Íntegra")
            else:
                print("Alterada")

    if not encontrou:
        print("\nNenhuma receita encontrada")

    input("\nPressione ENTER...")