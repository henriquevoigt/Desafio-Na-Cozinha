from controllers.livro_receitas import carregar_receitas

def main():
    print("iniciando o sistema do chef jacquin...\n")

    estante_de_receitas = carregar_receitas()

    print(f"\nSucesso! {len(estante_de_receitas)} receitas foram carregadas na memória.\n")
    print("-" * 50)

    for receita in estante_de_receitas:
        print(f"ID: {receita.id} | Nome: {receita.name}")
        print(f"Tempo de Preparo: {receita.prepTimeMinutes} min | Dificuldade: {receita.difficulty}")
        print(f"Ingredientes principais: {receita.ingredients}") 

        print("Passos:")
        for indice, passo in enumerate(receita.instructions, start=1):
            print(f"  {indice}. {passo}")

        print("-" * 80)

if __name__ == "__main__":
    main()