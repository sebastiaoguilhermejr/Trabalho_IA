from collections import deque
from NodeP import NodeP

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
    ##def custo_uniforme(self,inicio,fim,mapa,nx,ny):
    def custo_uniforme(self, inicio, fim, nos, grafo): #grafo
        # Origem igual a destino
        if inicio == fim:
            return [inicio]
        
        # Fila de prioridade baseada em deque + inserção ordenada
        lista = deque()
        #t_inicio = tuple(inicio)   # grid
        raiz = NodeP(None, inicio, 0, None, None, 0) # grafo
        #raiz = NodeP(None, t_inicio,0, None, None, 0)  # grid
        lista.append(raiz)
    
        # Controle de nós visitados
        visitado = {inicio: raiz}
        #visitado = {tuple(inicio): raiz}    # grid
        
        # loop de busca
        while lista:
            # remove o primeiro nó
            atual = lista.popleft()
            valor_atual = atual.v2
    
            # Chegou ao objetivo: UCS garante ótimo (custos >= 0)
            if atual.estado == fim:
                caminho = self.exibirCaminho(atual)
                return caminho, atual.v2
    
            # Gera sucessores; esperado: [(estado_suc, custo_aresta), ...]
            ind = nos.index(atual.estado)
            filhos = self.sucessores_grafo(ind, grafo, 1)
            
            # Gera sucessores a partir do grid
            #filhos = self.sucessores_grid(atual.estado,nx,ny,mapa) # grid
    
            for novo in filhos: # grafo
            #for novo in filhos: # grid
                # custo acumulado até o sucessor
                v2 = valor_atual + novo[1]
                v1 = v2 
    
                # Não visitado ou custo melhor
               # t_novo = tuple(novo[0])       # grid
                #if (t_novo not in visitado) or (v2<visitado[t_novo].v2): # grid
                if (novo[0] not in visitado) or (v2 < visitado[novo[0]].v2):
                    #filho = NodeP(atual,t_novo, v1, None, None, v2) # grid
                    filho = NodeP(atual, novo[0], v1, None, None, v2) # grafo
                    visitado[novo[0]] = filho #grafo
                    #visitado[t_novo] = filho # grid
                    self.inserir_ordenado(lista, filho)
    
        # Sem caminho
        return None
# -----------------------------------------------------------------------------
# GREEDY
# -----------------------------------------------------------------------------
    def greedy(self, inicio, fim, nos, grafo):
        # Origem igual a destino
        if inicio == fim:
            return [inicio]
        
        # Fila de prioridade baseada em deque + inserção ordenada
        lista = deque()
        
        raiz = NodeP(None, inicio, 0, None, None, 0)
    
        lista.append(raiz)
    
        # Controle de nós visitados
        visitado = {inicio: raiz}
        
        # loop de busca
        while lista:
            # remove o primeiro nó
            atual = lista.popleft()
            valor_atual = atual.v2
    
            # Se já registramos um nó melhor para este estado, este está obsoleto
            #if visitado.get(atual.estado) is not atual:
            #    continue
    
            # Chegou ao objetivo: UCS garante ótimo (custos >= 0)
            if atual.estado == fim:
                caminho = self.exibirCaminho(atual)
                return caminho, atual.v2
    
            # Gera sucessores; esperado: [(estado_suc, custo_aresta), ...]
            ind = nos.index(atual.estado)
            filhos = self.sucessores_grafo(ind, grafo, 1)
    
            for novo in filhos:
                # custo acumulado até o sucessor
                v2 = valor_atual + novo[1]
                v1 = self.heuristica_grafo(nos,novo[0],fim) 
    
                # relaxamento: nunca visto ou custo melhor
                if (novo[0] not in visitado) or (v2 < visitado[novo[0]].v2):
                    filho = NodeP(atual, novo[0], v1, None, None, v2)
                    visitado[novo[0]] = filho
                    self.inserir_ordenado(lista, filho)
    
        # Sem caminho
        return None  
# -----------------------------------------------------------------------------
# A ESTRELA
# -----------------------------------------------------------------------------
    def a_estrela(self,inicio,fim,nos,grafo,):
        # Origem igual a destino
        if inicio == fim:
            return [inicio]
        
        # Fila de prioridade baseada em deque + inserção ordenada
        lista = deque()
        
        raiz = NodeP(None, inicio, 0, None, None, 0)
    
        lista.append(raiz)
    
        # Controle de nós visitados
        visitado = {inicio: raiz}
        
        # loop de busca
        while lista:
            # remove o primeiro nó
            atual = lista.popleft()
            valor_atual = atual.v2
    
            # Chegou ao objetivo
            if atual.estado == fim:
                caminho = self.exibirCaminho(atual)
                return caminho, atual.v2
    
            # Gera sucessores; esperado: [(estado_suc, custo_aresta), ...]
            ind = nos.index(atual.estado)
            filhos = self.sucessores_grafo(ind, grafo, 1)
    
            for novo in filhos:
                # custo acumulado até o sucessor
                v2 = valor_atual + novo[1]
                v1 = v2 + self.heuristica_grafo(nos,novo[0],fim) 
    
                # relaxamento: nunca visto ou custo melhor
                if (novo[0] not in visitado) or (v2 < visitado[novo[0]].v2):
                    filho = NodeP(atual, novo[0], v1, None, None, v2)
                    visitado[novo[0]] = filho
                    self.inserir_ordenado(lista, filho)
    
        # Sem caminho
        return None
# -----------------------------------------------------------------------------
# AI ESTRELA
# -----------------------------------------------------------------------------       
    def aia_estrela(self,inicio,fim,nos,grafo):
        # Origem igual a destino
        if inicio == fim:
            return [inicio]
        
        limite = self.heuristica_grafo(nos,inicio,fim) 
        # Fila de prioridade baseada em deque + inserção ordenada
        lista = deque()
        
        # Busca iterativa
        while True:
            lim_acima = []
            
            raiz = NodeP(None, inicio, 0, None, None, 0)       
            lista.append(raiz)
        
            # Controle de nós visitados
            visitado = {inicio: raiz}

            while lista:
                # remove o primeiro nó
                atual = lista.popleft()
                valor_atual = atual.v2
                
                # Chegou ao objetivo
                if atual.estado == fim:
                    caminho = self.exibirCaminho(atual)
                    return caminho, atual.v2, limite
                
                # Gera sucessores; esperado: [(estado_suc, custo_aresta), ...]
                ind = nos.index(atual.estado)
                filhos = self.sucessores_grafo(ind, grafo, 1)
                
                for novo in filhos:
                    # custo acumulado até o sucessor
                    v2 = valor_atual + novo[1]
                    v1 = v2 + self.heuristica_grafo(nos,novo[0],fim) 
                    
                    # Verifica se está dentro do limite
                    if v1<=limite:
                        # Não visitado ou custo melhor
                        if (novo[0] not in visitado) or (v2 < visitado[novo[0]].v2):
                            filho = NodeP(atual, novo[0], v1, None, None, v2)
                            visitado[novo[0]] = filho
                            self.inserir_ordenado(lista, filho)
                    else:
                        lim_acima.append(v1)
            
            limite = sum(lim_acima)/len(lim_acima)
            lista.clear()
            visitado.clear()
            filhos.clear()
                        
            return None
