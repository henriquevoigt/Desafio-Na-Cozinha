class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.recipes = []

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, recipe):
        current = self.root
        word = word.lower()
        for char in word:
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        current.is_end = True
        current.recipes.append(recipe)

    def _collect(self, node, results):
        if node.is_end:
            results.extend(node.recipes)
        for child in node.children.values():
            self._collect(child, results)
        
    def search_prefix(self, prefix):
        current = self.root
        prefix = prefix.lower()
        for char in prefix:
            if char not in current.children:
                return[]
            current = current.children[char]
        results = []
        self._collect(current, results)
        return results