import hashlib

class HashTable:
    def __init__(self):
        self.table = {}
    
    def gera_hash(self, recipe):
        data = ""
        data += recipe.name
        data += "".join(recipe.ingredients)
        data += "".join(recipe.instructions)
        data += str(recipe.prepTimeMinutes)
        data += str(recipe.cookTimeMinutes)

        key_hash = hashlib.sha256(data.encode()).hexdigest()
        return key_hash
    
    def insert(self, recipe):
        key_hash = self.gera_hash(recipe)
        self.table[recipe.id] = key_hash

    def verify(self, recipe):
        new_hash = self.gera_hash(recipe)
        old_hash = self.table.get(recipe.id)

        return new_hash == old_hash