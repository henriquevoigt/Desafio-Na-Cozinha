from models.hash_table import HashTable
from models.receita import Receita

receita = Receita(
    id=1,
    name="Bolo de Cenoura",
    ingredients=["cenoura", "açúcar", "farinha"],
    instructions=["Misturar", "Assar"],
    prepTimeMinutes=20,
    cookTimeMinutes=40,
    difficulty="Médio",
    cuisine="Brasileira",
    caloriesPerServing=250,
    tags=["doce"],
    rating=4.5,
    reviewCount=10,
    mealType=["sobremesa"]
)

ht = HashTable()
ht.insert(receita)

print(ht.verify(receita))  # tenq ser True

receita.ingredients = ["cenoura", "açúcar", "farinha"]
print(ht.verify(receita))  # tenq ser False se diferente do de cima