from typing import Optional, List, Tuple, Sequence
from math import inf
from BuscaNP import BuscaNP
from BuscaP import busca as BuscaP

class PickingSlotting(object):
    def __init__(self, nos: Sequence[int], grafo: Sequence[Sequence[tuple[int, float]]]):
        self.nos: list[int] = list(nos)
        ## Grafo ponderado
        self.grafo_p: list[list[tuple[int, float]]] =   [list(adj) for adj in grafo]
        ##Grafo não ponderado
        self.grafo_np: list[list[int]] = [[v for (v, _) in adj] for adj in self.grafo_p]
        self.buscaNP = BuscaNP()
        self.buscaP = BuscaP()

    def caminho_e_custo(self, method: str, inicio: int, fim: int, *, lim: Optional[int] = None,
                        lim_max: Optional[int] = None):
        method = method.upper().strip()
        if method == "AMPLITUDE":
            cam = self.buscaNP.amplitude(inicio, fim, self.nos, self.grafo_np)
        elif method == "PROFUNDIDADE":
            cam = self.buscaNP.profundidade(inicio, fim, self.nos, self.grafo_np)
        elif method in ("PROFUNDIDADE_LIMITADA", "PROF_LIMITADA"):
            if lim is None:
                raise ValueError("Profundidade limitada requer lim")
            cam = self.buscaNP.prof_limitada(inicio, fim, self.nos, self.grafo_np, lim)
        elif method == "APROFUNDAMENTO_ITERATIVO":
            if lim_max is None:
                raise ValueError("Aprofundamento iterativo requer lim_max")
            cam = self.buscaNP.aprof_iterativo(inicio, fim, self.nos, self.grafo_np, lim_max)
        elif method in ("BUSCA BIDIRECIONAL", "BIDIRECIONAL"):
            cam = self.buscaNP.bidirecional(inicio, fim, self.nos, self.grafo_np)
        elif method == "CUSTO_UNIFORME":
            return self.buscaP.custo_uniforme(inicio, fim, self.nos, self.grafo_p)
        elif method == "GREEDY":
            return self.buscaP.greedy(inicio, fim, self.nos, self.grafo_p)
        elif method == "A_ESTRELA":
            return self.buscaP.a_estrela(inicio, fim, self.nos, self.grafo_p)
        elif method == "AIA_ESTRELA":
            return self.buscaP.aia_estrela(inicio, fim, self.nos, self.grafo_p)
        else:
            raise ValueError(f"Método desconhecido: {method}")

        if not cam:
            return None
        return cam, len(cam) - 1

    def fechamento_metrico(self, P: list[int], *, method: str, lim: Optional[int] = None,
                           lim_max: Optional[int] = None):
        n = len(P)
        M = [[float('inf')] * n for _ in range(n)]

        for i in range(n):
            M[i][i] = 0

        for i, s in enumerate(P):
            for j, t in enumerate(P):
                if i == j:
                    continue
                result = self.caminho_e_custo(method, s, t, lim=lim, lim_max=lim_max)
                if result is not None:
                    cam, custo = result
                    M[i][j] = custo
        return M

    def rota_vizinho_mais_proximo(self, M, start_idx=0):
        n = len(M)
        if n == 0:
            return []
        nao_visitados = set(range(n))
        nao_visitados.discard(start_idx)
        ordem_idx = [start_idx]
        atual = start_idx
        while nao_visitados:
            prox = min(nao_visitados, key=lambda j: (M[atual][j], j))
            ordem_idx.append(prox)
            nao_visitados.remove(prox)
            atual = prox
        return ordem_idx

    def traduzir_rota_vizinho_mais_proximo(self, M, P, start_idx=0):
        assert len(M) == len(P)
        ordem_idx = self.rota_vizinho_mais_proximo(M, start_idx)
        return [P[i] for i in ordem_idx]

    def custo_e_rota_expandida(self, ordem_idx: list[int], P: list[int], method: str = "AMPLITUDE",
                               lim: Optional[int] = None, lim_max: Optional[int] = None,
                               fechar_ciclo: bool = False) -> tuple[list[int], float]:
        if not ordem_idx:
            return [], 0.0

        pares = list(zip(ordem_idx, ordem_idx[1:]))
        if fechar_ciclo and len(ordem_idx) > 1:
            pares.append((ordem_idx[-1], ordem_idx[0]))

        caminho_total: list[int] = []
        custo_total: float = 0.0

        for i_idx, j_idx in pares:
            s, t = P[i_idx], P[j_idx]
            result = self.caminho_e_custo(method, s, t, lim=lim, lim_max=lim_max)
            if result is None:
                return [], inf
            cam, custo = result
            if not caminho_total:
                caminho_total.extend(cam)
            else:
                caminho_total.extend(cam[1:])
            custo_total += float(custo)

        return caminho_total, custo_total

    def resolver_picking(self, doca: int, picklist: list[int], method: str, *, lim: Optional[int] = None,
                         lim_max: Optional[int] = None,
                         fechar_ciclo: bool = False) -> tuple[list[int], float]:
        P = [doca] + list(picklist)
        matriz = self.fechamento_metrico(P, method=method, lim=lim, lim_max=lim_max)

        ordem_idx = self.rota_vizinho_mais_proximo(matriz, start_idx=0)

        caminho_total, custo_total = self.custo_e_rota_expandida(ordem_idx, P, method=method, lim=lim,
                                                            lim_max=lim_max, fechar_ciclo=fechar_ciclo)
        return caminho_total, custo_total

    def rank_slots_por_distancia(self, doca: int, slots: Optional[list[int]] = None, method: str = "AMPLITUDE", *,
                                 lim: Optional[int] = None, lim_max: Optional[int] = None) -> list[tuple[int, int]]:
        if slots is None:
            slots = [n for n in self.nos if n != doca]
        else:
            slots = sorted({s for s in slots if s != doca})

        ranking = []
        for s in slots:
            cam, custo = self.caminho_e_custo(method, doca, s, lim=lim, lim_max=lim_max)
            dist = int(custo) if custo is not None else float("inf")
            ranking.append((s, dist))

        ranking.sort(key=lambda x: (x[1], x[0]))
        return ranking