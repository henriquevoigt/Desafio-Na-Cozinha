from dataclasses import dataclass, field
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
    
    # P2
    dependencias: list[int] = field(default_factory=list)
    custo: float = 0.0
    valor_venda: float = 0.0
    classe: str = "Prato Principal"
    dificuldade_logistica: str = "média"