from dataclasses import dataclass

@dataclass
class Receita:
    id: int
    name: str
    ingredients: list[str]
    instructions: list[str]
    prepTimeMinutes: int
    cookTimeMinutes: int
    difficulty: str
    cuisine: str
    caloriesPerServing: int
    tags: list[str]
    rating: float
    reviewCount: int
    mealType: list[str]