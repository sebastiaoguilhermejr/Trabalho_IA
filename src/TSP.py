import random
import numpy as np


class TSP:
    """Classe TSP com identificadores em português.

    Observação: o nome da classe permanece `TSP` para compatibilidade de importação,
    mas todos os atributos e métodos públicos estão em português.
    """

    def __init__(self, num_cidades: int):
        if not isinstance(num_cidades, int):
            raise TypeError("num_cidades deve ser um inteiro")
        if num_cidades < 30:
            raise ValueError("num_cidades deve ser >= 30")
        self.num_cidades = num_cidades
        self.distancias = self.gerar_matriz_distancias()

    def gerar_matriz_distancias(self):
        """Gera uma matriz de distâncias aleatória para um grafo completo."""
        matrix = np.zeros((self.num_cidades, self.num_cidades))
        for i in range(self.num_cidades):
            for j in range(i + 1, self.num_cidades):
                d = random.randint(10, 100)
                matrix[i][j] = d
                matrix[j][i] = d
        return matrix

    def calcular_comprimento_rota(self, rota):
        """Calcula o comprimento total de uma rota (fechada)."""
        total = 0
        for i in range(len(rota)):
            a = rota[i]
            b = rota[(i + 1) % len(rota)]
            total += self.distancias[a][b]
        return total

    def gerar_solucao_inicial(self):
        """Gera uma solução inicial aleatória."""
        rota = list(range(self.num_cidades))
        random.shuffle(rota)
        return rota

    def vizinho_mais_proximo(self, inicio=0):
        """Inicializa usando heurística do vizinho mais próximo."""
        if inicio < 0 or inicio >= self.num_cidades:
            raise ValueError("inicio deve ser um índice válido")
        nao_visitadas = set(range(self.num_cidades))
        rota = [inicio]
        nao_visitadas.remove(inicio)
        atual = inicio
        while nao_visitadas:
            proxima = min(nao_visitadas, key=lambda c: self.distancias[atual][c])
            rota.append(proxima)
            nao_visitadas.remove(proxima)
            atual = proxima
        return rota

    def subida_de_encosta(self, max_iteracoes=1000):
        """Busca local por troca de duas cidades (2-opt simple)."""
        rota = self.gerar_solucao_inicial()
        distancia = self.calcular_comprimento_rota(rota)
        for _ in range(max_iteracoes):
            i, j = random.sample(range(self.num_cidades), 2)
            nova = rota.copy()
            nova[i], nova[j] = nova[j], nova[i]
            nova_dist = self.calcular_comprimento_rota(nova)
            if nova_dist < distancia:
                rota, distancia = nova, nova_dist
        return rota, distancia

    def subida_de_encosta_com_tentativas(self, num_tentativas=5, max_iteracoes=1000):
        """Executa `subida_de_encosta` várias vezes com reinicializações."""
        melhor_rota = None
        melhor_dist = float('inf')
        for _ in range(num_tentativas):
            rota, dist = self.subida_de_encosta(max_iteracoes)
            if dist < melhor_dist:
                melhor_rota, melhor_dist = rota, dist
        return melhor_rota, melhor_dist

    def tempera_simulada(self, temp_inicial=1000, taxa_resfriamento=0.995, max_iteracoes=10000):
        """Implementação simples de têmpera simulada (Metropolis)."""
        rota = self.gerar_solucao_inicial()
        dist = self.calcular_comprimento_rota(rota)
        melhor_rota, melhor_dist = rota.copy(), dist
        temperatura = temp_inicial
        for _ in range(max_iteracoes):
            i, j = random.sample(range(self.num_cidades), 2)
            nova = rota.copy()
            nova[i], nova[j] = nova[j], nova[i]
            nova_dist = self.calcular_comprimento_rota(nova)
            delta = nova_dist - dist
            if delta < 0 or random.random() < np.exp(-delta / temperatura):
                rota, dist = nova, nova_dist
                if dist < melhor_dist:
                    melhor_rota, melhor_dist = rota.copy(), dist
            temperatura *= taxa_resfriamento
        return melhor_rota, melhor_dist

    def algoritmo_genetico(self, tamanho_populacao=50, geracoes=100):
        """Implementação básica de um algoritmo genético para TSP."""
        populacao = [self.gerar_solucao_inicial() for _ in range(tamanho_populacao)]

        def crossover(p1, p2):
            n = len(p1)
            a, b = sorted(random.sample(range(n), 2))
            filho = [-1] * n
            filho[a:b] = p1[a:b]
            restante = [x for x in p2 if x not in filho[a:b]]
            j = 0
            for i in range(n):
                if filho[i] == -1:
                    filho[i] = restante[j]
                    j += 1
            return filho

        for _ in range(geracoes):
            avaliacao = [(rota, self.calcular_comprimento_rota(rota)) for rota in populacao]
            avaliacao.sort(key=lambda x: x[1])
            elite = [x[0] for x in avaliacao[:tamanho_populacao // 2]]
            nova = elite.copy()
            while len(nova) < tamanho_populacao:
                p1, p2 = random.sample(elite, 2)
                filho = crossover(p1, p2)
                if random.random() < 0.1:
                    i, j = random.sample(range(self.num_cidades), 2)
                    filho[i], filho[j] = filho[j], filho[i]
                nova.append(filho)
            populacao = nova

        melhor = min(populacao, key=lambda r: self.calcular_comprimento_rota(r))
        return melhor, self.calcular_comprimento_rota(melhor)
