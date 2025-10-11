from collections import deque
from NodeP import NodeP
from PQueue import PQueue

class busca(object):
#--------------------------------------------------------------------------
# SUCESSORES PARA GRAFO
#--------------------------------------------------------------------------
    def sucessores_grafo(self,ind,grafo,ordem):
        
        f = []
        for suc in grafo[ind][::ordem]:
            f.append(suc)
        return f
    

#--------------------------------------------------------------------------    
# INSERE NA LISTA MANTENDO-A ORDENADA
#--------------------------------------------------------------------------    

    def inserir_ordenado(self,lista, no):
        for i, n in enumerate(lista):
            if no.v1 < n.v1:
                lista.insert(i, no)
                break
        else:
            lista.append(no)

#--------------------------------------------------------------------------    
# EXIBE O CAMINHO ENCONTRADO NA ÁRVORE DE BUSCA
#--------------------------------------------------------------------------    
    def exibirCaminho(self,node):
        caminho = []
        while node is not None:
            caminho.append(node.estado)
            node = node.pai
        caminho.reverse()
        return caminho
#--------------------------------------------------------------------------    
# GERA H DE FORMA ALEATÓRIA
#--------------------------------------------------------------------------    
    def heuristica_grafo(self,nos,destino,n):
        i_destino = nos.index(destino)
        i_n = nos.index(n)
        h = [
            [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 4, 6, 8, 10, 12, 14, 16, 18, 20,
             22],
            [2, 0, 2, 4, 6, 8, 10, 12, 14, 16, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 6, 8, 10, 12, 14, 16, 18, 20, 22,
             24],
            [4, 2, 0, 2, 4, 6, 8, 10, 12, 14, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 8, 10, 12, 14, 16, 18, 20, 22, 24,
             26],
            [6, 4, 2, 0, 2, 4, 6, 8, 10, 12, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 10, 12, 14, 16, 18, 20, 22, 24, 26,
             28],
            [8, 6, 4, 2, 0, 2, 4, 6, 8, 10, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 12, 14, 16, 18, 20, 22, 24, 26, 28,
             30],
            [10, 8, 6, 4, 2, 0, 2, 4, 6, 8, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 14, 16, 18, 20, 22, 24, 26, 28, 30,
             32],
            [12, 10, 8, 6, 4, 2, 0, 2, 4, 6, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 16, 18, 20, 22, 24, 26, 28, 30, 32,
             34],
            [14, 12, 10, 8, 6, 4, 2, 0, 2, 4, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 18, 20, 22, 24, 26, 28, 30, 32,
             34, 36],
            [16, 14, 12, 10, 8, 6, 4, 2, 0, 2, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 20, 22, 24, 26, 28, 30, 32, 34,
             36, 38],
            [18, 16, 14, 12, 10, 8, 6, 4, 2, 0, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 22, 24, 26, 28, 30, 32, 34, 36,
             38, 40],
            [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 4, 6, 8, 10, 12, 14, 16, 18, 20,
             22],
            [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 2, 0, 2, 4, 6, 8, 10, 12, 14, 16, 6, 8, 10, 12, 14, 16, 18, 20, 22,
             24],
            [6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 4, 2, 0, 2, 4, 6, 8, 10, 12, 14, 8, 10, 12, 14, 16, 18, 20, 22, 24,
             26],
            [8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 6, 4, 2, 0, 2, 4, 6, 8, 10, 12, 10, 12, 14, 16, 18, 20, 22, 24, 26,
             28],
            [10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 8, 6, 4, 2, 0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28,
             30],
            [12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 10, 8, 6, 4, 2, 0, 2, 4, 6, 8, 14, 12, 10, 8, 6, 4, 2, 4, 6, 8],
            [14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 12, 10, 8, 6, 4, 2, 0, 2, 4, 6, 16, 14, 12, 10, 8, 6, 4, 2, 4, 6],
            [16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 14, 12, 10, 8, 6, 4, 2, 0, 2, 4, 18, 16, 14, 12, 10, 8, 6, 4, 2,
             4],
            [18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 16, 14, 12, 10, 8, 6, 4, 2, 0, 2, 20, 18, 16, 14, 12, 10, 8, 6, 4,
             2],
            [20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 18, 16, 14, 12, 10, 8, 6, 4, 2, 0, 22, 20, 18, 16, 14, 12, 10, 8,
             6, 4],
            [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 0, 2, 4, 6, 8, 10, 12, 14, 16,
             18],
            [6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 6, 8, 10, 12, 14, 12, 14, 16, 18, 20, 2, 0, 2, 4, 6, 8, 10, 12, 14,
             16],
            [8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 8, 10, 12, 14, 16, 10, 12, 14, 16, 18, 4, 2, 0, 2, 4, 6, 8, 10, 12,
             14],
            [10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 10, 12, 14, 16, 18, 8, 10, 12, 14, 16, 6, 4, 2, 0, 2, 4, 6, 8, 10,
             12],
            [12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 12, 14, 16, 18, 20, 6, 8, 10, 12, 14, 8, 6, 4, 2, 0, 2, 4, 6, 8,
             10],
            [14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 14, 16, 18, 20, 22, 4, 6, 8, 10, 12, 10, 8, 6, 4, 2, 0, 2, 4, 6,
             8],
            [16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 16, 18, 20, 22, 24, 2, 4, 6, 8, 10, 12, 10, 8, 6, 4, 2, 0, 2, 4,
             6],
            [18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 18, 20, 22, 24, 26, 4, 6, 8, 10, 12, 14, 12, 10, 8, 6, 4, 2, 0, 2,
             4],
            [20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 20, 22, 24, 26, 28, 6, 8, 10, 12, 14, 16, 14, 12, 10, 8, 6, 4, 2,
             0, 2],
            [22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 22, 24, 26, 28, 30, 8, 10, 12, 14, 16, 18, 16, 14, 12, 10, 8, 6, 4,
             2, 0]
        ]

        return h[i_destino][i_n]
# -----------------------------------------------------------------------------
# CUSTO UNIFORME
# -----------------------------------------------------------------------------

    def custo_uniforme(self, inicio, fim, nos, grafo):
        if inicio == fim:
            return [inicio]

        pq = PQueue()
        raiz = NodeP(None, inicio, 0.0, None, None, 0.0)  # v1 = g, v2 = g
        pq.push(raiz.v1, raiz)

        best_g = {inicio: 0.0}

        while pq:
            atual = pq.pop()

            if atual.v2 > best_g.get(atual.estado, float('inf')):
                continue

            if atual.estado == fim:
                return self.exibirCaminho(atual), atual.v2

            ind = nos.index(atual.estado)
            for (suc, w) in grafo[ind]:
                g2 = atual.v2 + float(w)
                if g2 < best_g.get(suc, float('inf')):
                    best_g[suc] = g2
                    filho = NodeP(atual, suc, g2, None, None, g2)  # f=g
                    pq.push(filho.v1, filho)

        return None

    # -----------------------------------------------------------------------------
# GREEDY
# -----------------------------------------------------------------------------
    def greedy(self, inicio, fim, nos, grafo):
        if inicio == fim:
            return [inicio]

        pq = PQueue()
        g0 = 0.0
        h0 = float(self.heuristica_grafo(nos, fim, inicio))
        raiz = NodeP(None, inicio, h0, None, None, g0)  # f = h
        pq.push(raiz.v1, raiz)

        best_g = {inicio: 0.0}

        while pq:
            atual = pq.pop()

            if atual.v2 > best_g.get(atual.estado, float('inf')):
                continue

            if atual.estado == fim:
                return self.exibirCaminho(atual), atual.v2

            ind = nos.index(atual.estado)
            for (suc, w) in grafo[ind]:
                g2 = atual.v2 + float(w)
                if g2 < best_g.get(suc, float('inf')):
                    best_g[suc] = g2
                    h = float(self.heuristica_grafo(nos, fim, suc))
                    filho = NodeP(atual, suc, h, None, None, g2)  # f = h
                    pq.push(filho.v1, filho)

        return None

    # -----------------------------------------------------------------------------
# A ESTRELA
# -----------------------------------------------------------------------------
    def a_estrela(self, inicio, fim, nos, grafo):
        if inicio == fim:
            return [inicio]

        pq = PQueue()
        g0 = 0.0
        h0 = float(self.heuristica_grafo(nos, fim, inicio))
        raiz = NodeP(None, inicio, g0 + h0, None, None, g0)  # f = g + h
        pq.push(raiz.v1, raiz)

        best_g = {inicio: 0.0}

        while pq:
            atual = pq.pop()

            if atual.v2 > best_g.get(atual.estado, float('inf')):
                continue

            if atual.estado == fim:
                return self.exibirCaminho(atual), atual.v2

            ind = nos.index(atual.estado)
            for (suc, w) in grafo[ind]:
                g2 = atual.v2 + float(w)
                if g2 < best_g.get(suc, float('inf')):
                    best_g[suc] = g2
                    h = float(self.heuristica_grafo(nos, fim, suc))
                    f = g2 + h
                    filho = NodeP(atual, suc, f, None, None, g2)  # f = g + h
                    pq.push(filho.v1, filho)

        return None

    # -----------------------------------------------------------------------------
# AI ESTRELA
# -----------------------------------------------------------------------------       
    def aia_estrela(self, inicio, fim, nos, grafo):

        if inicio == fim:
            return [inicio], 0.0, 0.0

        limite = float(self.heuristica_grafo(nos, fim, inicio))

        while True:
            from collections import deque
            lista = deque()
            raiz = NodeP(None, inicio, 0.0 + float(self.heuristica_grafo(nos, fim, inicio)), None, None, 0.0)  # v1=f, v2=g
            lista.append(raiz)
            visitado = {inicio: raiz}


            min_acima = float("inf")

            while lista:
                atual = lista.popleft()
                g = atual.v2
                h_atual = float(self.heuristica_grafo(nos, fim, atual.estado))
                f_atual = g + h_atual

                if f_atual > limite:
                    if f_atual < min_acima:
                        min_acima = f_atual
                    continue

                if atual.estado == fim:
                    return self.exibirCaminho(atual), g, limite

                ind = nos.index(atual.estado)
                filhos = self.sucessores_grafo(ind, grafo, 1)
                for (suc, w) in filhos:
                    g2 = g + float(w)

                    if (suc in visitado) and (g2 >= visitado[suc].v2):
                        continue

                    h2 = float(self.heuristica_grafo(nos, fim, suc))
                    f2 = g2 + h2
                    filho = NodeP(atual, suc, f2, None, None, g2)
                    visitado[suc] = filho
                    self.inserir_ordenado(lista, filho)


            if min_acima == float("inf"):
                return None

            limite = min_acima

