class HashTable:
    def __init__(self):
        self.size = 10
        self.count = 0
        self.table = [[] for _ in range(self.size)]

    def gera_hash(self, recipe):
        data = recipe.name
        data += "".join(recipe.ingredients)
        data += "".join(recipe.instructions)
        data += str(recipe.prepTimeMinutes)
        data += str(recipe.cookTimeMinutes)
        hash_value = 0
        for char in data:
            hash_value = hash_value * 31 + ord(char)
        return hash_value

    def get_index(self, recipe):

        return self.gera_hash(recipe) % self.size

    def resize(self):
        old_table = self.table
        self.size *= 2
        self.table = [[] for _ in range(self.size)]
        self.count = 0
        for bucket in old_table:
            for saved_hash, recipe in bucket:
                self.insert(recipe)

    def insert(self, recipe):
        if self.count / self.size >= 1.0:
            self.resize()
        index = self.get_index(recipe)
        recipe_hash = self.gera_hash(recipe)
        self.table[index].append((recipe_hash, recipe))
        self.count += 1

    def verify(self, recipe):
        index = self.get_index(recipe)
        current_hash = self.gera_hash(recipe)
        for saved_hash, saved_recipe in self.table[index]:
            if saved_recipe.id == recipe.id:
                return saved_hash == current_hash
        return False