from collections import deque
import random

class SimuladorCapacidadeLogistica:

    def __init__(self, cap_cozinha, cap_frota, cap_laranjal, cap_fragata):
        self.nomes_nos = {
            0: "Origem (Demanda Total)",
            1: "Cozinha (Capacidade de Produção)",
            2: "Frota (Entregadores Disponíveis)",
            3: "Região Laranjal",
            4: "Região Fragata",
            5: "Destino (Entregas Concluídas)"
        }
        self.num_nos = len(self.nomes_nos)

        self.grafo_original = [
            [0, cap_cozinha, 0, 0, 0, 0], 
            [0, 0, cap_frota, 0, 0, 0],  
            [0, 0, 0, cap_laranjal, cap_fragata, 0], 
            [0, 0, 0, 0, 0, cap_laranjal],  
            [0, 0, 0, 0, 0, cap_fragata],  
            [0, 0, 0, 0, 0, 0]    
        ]
        
        self.grafo = [linha[:] for linha in self.grafo_original]

    def _bfs(self, origem, destino, parent):
        visitado = [False] * self.num_nos
        fila = deque([origem])
        visitado[origem] = True

        while fila:
            u = fila.popleft()
            for v, capacidade_residual in enumerate(self.grafo[u]):
                if not visitado[v] and capacidade_residual > 0:
                    fila.append(v)
                    visitado[v] = True
                    parent[v] = u
                    if v == destino:
                        return True
        return False

    def calcular_fluxo_maximo_e_gargalo(self):
        origem = 0
        destino = 5
        parent = [-1] * self.num_nos
        fluxo_maximo = 0

        # Ford-Fulkerson
        while self._bfs(origem, destino, parent):
            caminho_fluxo = float("Inf")
            s = destino
            
            # busca a menor capacidade no caminho
            while s != origem:
                caminho_fluxo = min(caminho_fluxo, self.grafo[parent[s]][s])
                s = parent[s]

            fluxo_maximo += caminho_fluxo
            v = destino
            
            while v != origem:
                u = parent[v]
                self.grafo[u][v] -= caminho_fluxo
                self.grafo[v][u] += caminho_fluxo
                v = parent[v]

        visitado = [False] * self.num_nos
        fila = deque([origem])
        visitado[origem] = True
        while fila:
            u = fila.popleft()
            for v, capacidade_residual in enumerate(self.grafo[u]):
                if not visitado[v] and capacidade_residual > 0:
                    fila.append(v)
                    visitado[v] = True

        gargalos = []
        for i in range(self.num_nos):
            for j in range(self.num_nos):
                if visitado[i] and not visitado[j] and self.grafo_original[i][j] > 0:
                    gargalos.append((self.nomes_nos[i], self.nomes_nos[j]))

        return fluxo_maximo, gargalos