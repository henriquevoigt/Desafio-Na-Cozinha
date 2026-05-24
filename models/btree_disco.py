import os
import pickle

class NoBTree:
    def __init__(self, id_no, folha=True):
        self.id_no = id_no
        self.folha = folha
        self.chaves = []  
        self.valores = []   
        self.filhos = []    

class BTreeDisco:
    def __init__(self, t=3):
        self.t = t  
        self.diretorio = "data/btree_nodos"
        self.meta_path = f"{self.diretorio}/meta.dat"
        self.raiz_id = 0
        self.proximo_id = 1

        if not os.path.exists(self.diretorio):
            os.makedirs(self.diretorio)

        if os.path.exists(self.meta_path):
            self._carregar_meta()
        else:
            self._salvar_meta()

            raiz = NoBTree(self.raiz_id, folha=True)
            self._salvar_no(raiz)

    def _salvar_meta(self):
        with open(self.meta_path, "wb") as f:
            pickle.dump({"raiz_id": self.raiz_id, "proximo_id": self.proximo_id}, f)

    def _carregar_meta(self):
        with open(self.meta_path, "rb") as f:
            dados = pickle.load(f)
            self.raiz_id = dados["raiz_id"]
            self.proximo_id = dados["proximo_id"]

    def _salvar_no(self, no):
        with open(f"{self.diretorio}/no_{no.id_no}.dat", "wb") as f:
            pickle.dump(no, f)

    def _carregar_no(self, id_no):
        with open(f"{self.diretorio}/no_{id_no}.dat", "rb") as f:
            return pickle.load(f)

    def buscar(self, chave):

        return self._buscar_recursivo(self.raiz_id, chave)

    def _buscar_recursivo(self, id_no, chave):

        no = self._carregar_no(id_no)
        i = 0
        
        while i < len(no.chaves) and chave > no.chaves[i]:
            i += 1

        if i < len(no.chaves) and chave == no.chaves[i]:
            return no.valores[i]
        elif no.folha:
            return None
        else:
            return self._buscar_recursivo(no.filhos[i], chave)

    def inserir(self, chave, valor):
        raiz = self._carregar_no(self.raiz_id)

        if len(raiz.chaves) == (2 * self.t) - 1:
            nova_raiz = NoBTree(self.proximo_id, folha=False)
            self.proximo_id += 1
            nova_raiz.filhos.append(self.raiz_id)

            antiga_raiz_id = self.raiz_id
            self.raiz_id = nova_raiz.id_no
            self._salvar_meta()
            self._salvar_no(nova_raiz)

            self._dividir_filho(nova_raiz, 0, antiga_raiz_id)
            self._inserir_nao_cheio(nova_raiz, chave, valor)
        else:
            self._inserir_nao_cheio(raiz, chave, valor)

    def _dividir_filho(self, no_pai, indice_filho, id_filho_cheio):
        t = self.t
        filho_cheio = self._carregar_no(id_filho_cheio)
        
        novo_no = NoBTree(self.proximo_id, folha=filho_cheio.folha)
        self.proximo_id += 1
        self._salvar_meta()

        chave_meio = filho_cheio.chaves[t - 1]
        valor_meio = filho_cheio.valores[t - 1]

        novo_no.chaves = filho_cheio.chaves[t: (2 * t) - 1]
        novo_no.valores = filho_cheio.valores[t: (2 * t) - 1]
        
        filho_cheio.chaves = filho_cheio.chaves[0: t - 1]
        filho_cheio.valores = filho_cheio.valores[0: t - 1]

        if not filho_cheio.folha:
            novo_no.filhos = filho_cheio.filhos[t: 2 * t]
            filho_cheio.filhos = filho_cheio.filhos[0: t]

        no_pai.filhos.insert(indice_filho + 1, novo_no.id_no)
        no_pai.chaves.insert(indice_filho, chave_meio)
        no_pai.valores.insert(indice_filho, valor_meio)

        self._salvar_no(filho_cheio)
        self._salvar_no(novo_no)
        self._salvar_no(no_pai)

    def _inserir_nao_cheio(self, no, chave, valor):
        i = len(no.chaves) - 1
        if no.folha:
            no.chaves.append(None)
            no.valores.append(None)
            while i >= 0 and chave < no.chaves[i]:
                no.chaves[i + 1] = no.chaves[i]
                no.valores[i + 1] = no.valores[i]
                i -= 1
            no.chaves[i + 1] = chave
            no.valores[i + 1] = valor
            self._salvar_no(no)
        else:
            while i >= 0 and chave < no.chaves[i]:
                i -= 1
            i += 1
            filho = self._carregar_no(no.filhos[i])
            if len(filho.chaves) == (2 * self.t) - 1:
                self._dividir_filho(no, i, filho.id_no)
                no = self._carregar_no(no.id_no)
                if chave > no.chaves[i]:
                    i += 1
                    
            filho_atualizado = self._carregar_no(no.filhos[i])
            self._inserir_nao_cheio(filho_atualizado, chave, valor)